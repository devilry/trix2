import collections
import yaml
import itertools
from django import forms
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from trix.trix_core import models as coremodels
from trix.trix_core.tagutils import bulk_update_assignment_tags


class MarkdownString(object):
    """
    Used to mark unicode strings as Markdown for the YAML serializer.

    This is just so we can dump them using the literal-scalar style.

    """

    def __init__(self, unicode_object):
        self.unicode_object = unicode_object

    def __str__(self):
        return self.unicode_object

    @staticmethod
    def representer(dumper, data):
        """
        YAML representer for MarkdownString.

        We represent MarkdownString as a ``!!str``-tag (I.E.: ``tag:yaml.org,2002:str``),
        with the `literal-scalar style <http://www.yaml.org/spec/1.2/spec.html#id2795688>`_.
        """
        return dumper.represent_scalar('tag:yaml.org,2002:str', data.unicode_object, style='|')


yaml.SafeDumper.add_representer(MarkdownString, MarkdownString.representer)


class YamlMapOrderedDict(collections.OrderedDict):
    """
    A subclass of ``collections.OrderedDict`` that we have
    a registered yaml f
    """

    @staticmethod
    def representer(dumper, data):
        """
        YAML representer for YamlMapOrderedDict.
        """
        value = []
        for item_key, item_value in list(data.items()):
            node_key = dumper.represent_data(item_key)
            node_value = dumper.represent_data(item_value)
            value.append((node_key, node_value))
        return yaml.nodes.MappingNode('tag:yaml.org,2002:map', value)


yaml.SafeDumper.add_representer(YamlMapOrderedDict, YamlMapOrderedDict.representer)


def serialize(assignments):
    """
    Serialize an iterable of assignments.

    Params:
        assignments (iterable): Iterable of :class:`trix.trix_core.models.Assignment` objects
    """
    serializable_assignments = []
    for assignment in assignments:
        serializable_assignment = YamlMapOrderedDict([
            ('id', assignment.id),
            ('title', assignment.title),
            ('tags', [tag.tag for tag in assignment.tags.all()]),
            ('hidden', assignment.hidden),
            ('text', MarkdownString(assignment.text)),
        ])
        if assignment.solution:
            serializable_assignment['solution'] = MarkdownString(assignment.solution)
        serializable_assignments.append(serializable_assignment)
    return yaml.safe_dump_all(serializable_assignments, allow_unicode=True)


class DeserializerError(Exception):
    """
    Raised by :class:`.Deserializer` on errors.
    """


class DeserializerDuplicateIdError(DeserializerError):
    """
    Raised by :class:`.Deserializer` when multiple assignments
    with the same ID is encountered.
    """


class DeserializerNotFoundError(DeserializerError):
    """
    Raised by :class:`.Deserializer` when we encounter IDs
    that does not have a corresponding Assignment stored in
    the database.
    """


class DeserializerSingleValidationError(DeserializerError):
    """
    Used to store info about a ``django.core.exceptions.ValidationError``
    and the data causing the error when we validate in :class:`.Deserializer`.
    We collect the validation errors as objects of this class, and raise a
    :exc:`.DeserializerValidationErrors` containing a list of all the
    DeserializerSingleValidationError objects.
    """

    def __init__(self, errordict, data):
        self.errordict = errordict
        self.data = data

    def __str__(self):
        assignmentdict = {'id': self.data.get('id'), 'title': self.data.get('title')}
        return '{!r}: {!r}'.format(assignmentdict, self.errordict)


class DeserializerValidationErrors(DeserializerError):
    """
    See :exc:`DeserializerSingleValidationError`.
    """

    def __init__(self, errors):
        """
        Parameters:
            errors: List of :class:`.DeserializerSingleValidationError`.
        """
        self.errors = errors

    def __str__(self):
        strerrors = [str(error) for error in self.errors]
        return str(strerrors)


class ListField(forms.Field):
    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        return value or []

    def validate(self, value):
        super(ListField, self).validate(value)
        if not isinstance(value, list):
            raise ValidationError(_('Invalid value. Must be a list.'), code='invalid')
        for item in value:
            if not isinstance(item, str):
                raise ValidationError(_('Invalid value in list. Must be a list of strings.'),
                                      code='invalid')


class AssignmentDataForm(forms.ModelForm):
    tags = ListField(required=False)

    class Meta:
        model = coremodels.Assignment
        fields = ['title', 'text', 'solution']


class Deserializer(object):
    """
    Deserialize assignments serialized using :func:`.serialize`.

    If a deserialized assignment has an ``id``, we assume it already exists
    in the database. If it does not have an ``id``, we assume that the user
    wants to create a new assignment.
    """

    def __init__(self, serialized_assignments, course_tag):
        """
        Parameters:
            serialized_assignments: Assignments as serialized by :func:`serialize`.
            course_tag: A tag to add even if it is not on the given assignments.
                Only assignments with this tag already in the database is allowed
                to be updated.
        """
        self._deserialize(serialized_assignments)
        self.course_tag = course_tag

    def _deserialize(self, serialized_assignments):
        self.deserialized_assignments_with_id = {}
        self.deserialized_assignments_without_id = []
        for assignmentdict in yaml.safe_load_all(serialized_assignments):
            if 'id' in assignmentdict:
                if assignmentdict['id'] in self.deserialized_assignments_with_id:
                    raise DeserializerDuplicateIdError(
                        _('More than one assignment with "id=%(id)s".') %
                        {'id': assignmentdict['id']})
                else:
                    self.deserialized_assignments_with_id[assignmentdict['id']] = assignmentdict
            else:
                self.deserialized_assignments_without_id.append(assignmentdict)

    def _get_existing_assignments(self):
        existing_assignments = coremodels.Assignment.objects\
            .filter(
                id__in=list(self.deserialized_assignments_with_id.keys()),
                tags__tag=self.course_tag)
        if len(existing_assignments) != len(self.deserialized_assignments_with_id):
            raise DeserializerNotFoundError(
                _('One or more of the given IDs was not found among the assignments '
                  'accessible by "%(course_tag)s".') % {'course_tag': self.course_tag})
        return existing_assignments

    def _validate_assignment(self, assignment, data, assignments_by_tag):
        """
        Validate the given data, apply it to the given assignment, and
        return the list of tags (list of strings).

        Does not save the assignment.
        """
        form = AssignmentDataForm(data)
        if form.is_valid():
            assignment.title = form.cleaned_data['title']
            assignment.text = form.cleaned_data['text']
            assignment.solution = form.cleaned_data['solution']
            tags = form.cleaned_data['tags']

            # Add the assignment to assignments_by_tag
            # - used below to bulk create the tags
            for tag in tags:
                if tag != self.course_tag:  # We skip the course_tag - we add all assignments to it
                    if tag not in assignments_by_tag:
                        assignments_by_tag[tag] = []
                    assignments_by_tag[tag].append(assignment)
            if self.course_tag not in assignments_by_tag:
                assignments_by_tag[self.course_tag] = []
            assignments_by_tag[self.course_tag].append(assignment)
        else:
            raise DeserializerSingleValidationError(
                errordict=form.errors, data=data)

    def _validate_existing_assignments(self, assignments_by_tag):
        validationerrors = []
        existing_assignments = self._get_existing_assignments()
        for assignment in existing_assignments:
            data = self.deserialized_assignments_with_id[assignment.id]
            try:
                self._validate_assignment(assignment, data, assignments_by_tag)
            except DeserializerSingleValidationError as e:
                validationerrors.append(e)
        if validationerrors:
            raise DeserializerValidationErrors(validationerrors)
        return existing_assignments

    def _validate_new_assignments(self, assignments_by_tag):
        validationerrors = []
        new_assignments = []
        for data in self.deserialized_assignments_without_id:
            assignment = coremodels.Assignment()
            try:
                self._validate_assignment(assignment, data, assignments_by_tag)
            except DeserializerSingleValidationError as e:
                validationerrors.append(e)
            new_assignments.append(assignment)
        if validationerrors:
            raise DeserializerValidationErrors(validationerrors)
        return new_assignments

    @transaction.atomic
    def sync(self):
        assignments_by_tag = {}
        existing_assignments = self._validate_existing_assignments(assignments_by_tag)
        new_assignments = self._validate_new_assignments(assignments_by_tag)
        for assignment in itertools.chain(existing_assignments, new_assignments):
            assignment.full_clean()
            assignment.save()
        bulk_update_assignment_tags(assignments_by_tag, existing_assignments)
