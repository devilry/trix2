from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import truncatechars
from django import forms
from django_cradmin.viewhelpers import objecttable
from django_cradmin.viewhelpers import create
from django_cradmin.viewhelpers import update
from django_cradmin.viewhelpers import delete
from django_cradmin import crapp
from crispy_forms import layout
from django_cradmin.acemarkdown.widgets import AceMarkdownWidget

from trix.trix_core import models as trix_models


class TitleColumn(objecttable.MultiActionColumn):
    modelfield = 'title'

    def get_buttons(self, assignment):
        return [
            objecttable.Button(
                label='Edit',
                url=self.reverse_appurl('edit', args=[assignment.id])),
            objecttable.Button(
                label='Delete',
                url=self.reverse_appurl('delete', args=[assignment.id]),
                buttonclass="danger"),
        ]


class TextIntroColumn(objecttable.PlainTextColumn):
    modelfield = 'text'

    def render_value(self, assignment):
        return truncatechars(assignment.text, 50)


class TagsColumn(objecttable.PlainTextColumn):
    modelfield = 'tags'

    def render_value(self, assignment):
        return ', '.join(tag.tag for tag in assignment.tags.all())


class AssignmentListView(objecttable.ObjectTableView):
    model = trix_models.Assignment
    columns = [
        TitleColumn,
        TagsColumn,
        TextIntroColumn
    ]

    def get_queryset_for_role(self, course):
        return self.model.objects.filter(tags=course.course_tag)\
            .prefetch_related('tags')

    def get_buttons(self):
        app = self.request.cradmin_app
        return [
            objecttable.Button(_('Create'), url=app.reverse_appurl('create')),
        ]


class ManyToManyTagInputField(forms.CharField):

    def prepare_value(self, value):
        if value:
            return trix_models.Tag.objects.filter(id__in=value).to_unicode()
        else:
            return ''

    def to_python(self, value):
        tags = []
        for tagstring in trix_models.Tag.split_commaseparated_tags(value):
            tag = trix_models.Tag.objects.get_or_create(tagstring)
            tags.append(tag)
        return tags


class AssignmentCreateUpdateMixin(object):
    model = trix_models.Assignment

    # def get_preview_url(self):
    #     return reverse('lokalt_company_product_preview')

    def get_field_layout(self):
        return [
            layout.Div('title', css_class="cradmin-focusfield cradmin-focusfield-lg"),
            layout.Fieldset(_('Organize'), 'tags'),
            layout.Div('text', css_class="cradmin-focusfield"),
            layout.Div('solution', css_class="cradmin-focusfield"),

        ]

    def get_form(self, *args, **kwargs):
        form = super(AssignmentCreateUpdateMixin, self).get_form(*args, **kwargs)
        form.fields['tags'] = ManyToManyTagInputField(required=False)
        form.fields['text'].widget = AceMarkdownWidget()
        form.fields['solution'].widget = AceMarkdownWidget()
        return form

    def form_saved(self, assignment):
        course = self.request.cradmin_role
        if not assignment.tags.filter(tag=course.course_tag).exists():
            assignment.tags.add(course.course_tag)


class AssignmentCreateView(AssignmentCreateUpdateMixin, create.CreateView):
    """
    View used to create new assignments.
    """


class AssignmentUpdateView(AssignmentCreateUpdateMixin, update.UpdateView):
    """
    View used to create edit existing assignments.
    """


class AssignmentDeleteView(delete.DeleteView):
    """
    View used to delete existing assignments.
    """
    model = trix_models.Assignment


class App(crapp.App):
    appurls = [
        crapp.Url(
            r'^$',
            AssignmentListView.as_view(),
            name=crapp.INDEXVIEW_NAME),
        crapp.Url(
            r'^create$',
            AssignmentCreateView.as_view(),
            name="create"),
        crapp.Url(
            r'^edit/(?P<pk>\d+)$',
            AssignmentUpdateView.as_view(),
            name="edit"),
        crapp.Url(
            r'^delete/(?P<pk>\d+)$',
            AssignmentDeleteView.as_view(),
            name="delete")
    ]
