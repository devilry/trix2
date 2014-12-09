from django.template import defaultfilters
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import truncatechars
from django import forms
from django import http
from django_cradmin.viewhelpers import objecttable
from django_cradmin.viewhelpers import create
from django_cradmin.viewhelpers import update
from django_cradmin.viewhelpers import delete
from django_cradmin.viewhelpers import multiselect
from django_cradmin import crispylayouts
from django_cradmin import crapp
from django.core.urlresolvers import reverse
from crispy_forms import layout
from django_cradmin.acemarkdown.widgets import AceMarkdownWidget

from trix.trix_core import models as trix_models
from trix.trix_core import multiassignment_serialize
from trix.trix_admin import formfields


class TitleColumn(objecttable.MultiActionColumn):
    modelfield = 'title'

    def get_buttons(self, assignment):
        buttons = [
            objecttable.Button(
                label=_('Edit'),
                url=self.reverse_appurl('edit', args=[assignment.id])),
            objecttable.Button(
                label=_('Delete'),
                url=self.reverse_appurl('delete', args=[assignment.id]),
                buttonclass="danger"),
        ]

        course = self.view.request.cradmin_role
        tags = set([tag.tag for tag in assignment.tags.all()])
        if course.active_period.tag in tags:
            tags.remove(course.course_tag.tag)
            tags.remove(course.active_period.tag)
            view_url = u'{}?tags={}'.format(
                reverse('trix_student_course', kwargs={'course_id': course.id}),
                u','.join(tags))
            buttons.insert(1, objecttable.Button(
                label=_('View'),
                url=view_url))
        return buttons


class TextIntroColumn(objecttable.PlainTextColumn):
    modelfield = 'text'

    def render_value(self, assignment):
        return truncatechars(assignment.text, 50)


class LastUpdateDatetimeColumn(objecttable.PlainTextColumn):
    modelfield = 'lastupdate_datetime'

    def render_value(self, obj):
        return defaultfilters.date(obj.lastupdate_datetime, 'SHORT_DATETIME_FORMAT')


class TagsColumn(objecttable.PlainTextColumn):
    modelfield = 'tags'

    def is_sortable(self):
        return False

    def render_value(self, assignment):
        return ', '.join(tag.tag for tag in assignment.tags.all())


class AssignmentQuerysetForRoleMixin(object):
    def get_queryset_for_role(self, course):
        return self.model.objects.filter(tags=course.course_tag)\
            .prefetch_related('tags')


class AssignmentListView(AssignmentQuerysetForRoleMixin, objecttable.ObjectTableView):
    model = trix_models.Assignment
    columns = [
        TitleColumn,
        TagsColumn,
        TextIntroColumn,
        LastUpdateDatetimeColumn
    ]
    searchfields = [
        'title',
        'tags__tag',
        'text',
        'solution',
    ]

    def get_buttons(self):
        app = self.request.cradmin_app
        course = self.request.cradmin_role
        return [
            objecttable.Button(_('Create'), url=app.reverse_appurl('create')),
            objecttable.Button(
                _('Show on website'),
                url=reverse('trix_student_course', kwargs={'course_id': course.id})),
        ]

    def get_multiselect_actions(self):
        app = self.request.cradmin_app
        return [
            objecttable.MultiSelectAction(
                label=_('Edit'),
                url=app.reverse_appurl('multiedit')
            ),
        ]


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
        form.fields['tags'] = formfields.ManyToManyTagInputField(required=False)
        form.fields['text'].widget = AceMarkdownWidget()
        form.fields['solution'].widget = AceMarkdownWidget()
        return form

    def save_object(self, form):
        assignment = super(AssignmentCreateUpdateMixin, self).save_object(form)
        # Replace the tags with the new tags
        assignment.tags.clear()
        for tag in form.cleaned_data['tags']:
            assignment.tags.add(tag)
        return assignment

    def form_saved(self, assignment):
        course = self.request.cradmin_role
        if not assignment.tags.filter(tag=course.course_tag).exists():
            assignment.tags.add(course.course_tag)


class AssignmentCreateView(AssignmentCreateUpdateMixin, create.CreateView):
    """
    View used to create new assignments.
    """


class AssignmentUpdateView(AssignmentQuerysetForRoleMixin, AssignmentCreateUpdateMixin, update.UpdateView):
    """
    View used to edit existing assignments.
    """


class AssignmentMultiEditForm(forms.Form):
    data = forms.CharField(
        required=True,
        label=_('Assignment YAML'),
        widget=forms.Textarea)


class AssignmentMultiEditView(AssignmentQuerysetForRoleMixin, multiselect.MultiSelectFormView):
    """
    View used to edit multiple assignments.
    Supports both updating and creating assignments.
    """
    form_class = AssignmentMultiEditForm
    model = trix_models.Assignment
    template_name = 'trix_admin/assignments/multiedit.django.html'

    def form_valid(self, form):
        course = self.request.cradmin_role
        try:
            multiassignment_serialize.Deserializer(
                serialized_assignments=form.cleaned_data['data'],
                course_tag=course.course_tag.tag).sync()
        except multiassignment_serialize.DeserializerValidationErrors as e:
            return self.render_to_response(self.get_context_data(
                form=form,
                deserializer_validationerrors=e.errors))
        except multiassignment_serialize.DeserializerError as e:
            return self.render_to_response(self.get_context_data(
                form=form,
                deserializererror=e))
        return http.HttpResponseRedirect(self.request.cradmin_app.reverse_appindexurl())

    def get_initial(self):
        return {
            'data': multiassignment_serialize.serialize(self.selected_objects)
        }

    def get_buttons(self):
        return [
            crispylayouts.PrimarySubmit('submit-save', _('Save'))
        ]

    def get_field_layout(self):
        return [
            layout.Div('data', css_class="cradmin-focusfield cradmin-focusfield-screenheight"),
        ]


class AssignmentDeleteView(AssignmentQuerysetForRoleMixin, delete.DeleteView):
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
            r'^multiedit$',
            AssignmentMultiEditView.as_view(),
            name="multiedit"),
        crapp.Url(
            r'^delete/(?P<pk>\d+)$',
            AssignmentDeleteView.as_view(),
            name="delete")
    ]
