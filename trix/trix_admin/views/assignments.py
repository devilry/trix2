# from django.core.urlresolvers import reverse
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
from crispy_forms import layout
from django_cradmin.acemarkdown.widgets import AceMarkdownWidget

from trix.trix_core import models as trix_models
from trix.trix_core import multiassignment_serialize
from trix.trix_admin import formfields


class TitleColumn(objecttable.MultiActionColumn):
    modelfield = 'title'

    def get_buttons(self, assignment):
        return [
            objecttable.Button(
                label=_('Edit'),
                url=self.reverse_appurl('edit', args=[assignment.id])),
            objecttable.Button(
                label=_('Delete'),
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


class AssignmentQuerysetForRoleMixin(object):
    def get_queryset_for_role(self, course):
        return self.model.objects.filter(tags=course.course_tag)\
            .prefetch_related('tags')


class AssignmentListView(AssignmentQuerysetForRoleMixin, objecttable.ObjectTableView):
    model = trix_models.Assignment
    columns = [
        TitleColumn,
        TagsColumn,
        TextIntroColumn
    ]

    def get_buttons(self):
        app = self.request.cradmin_app
        return [
            objecttable.Button(_('Create'), url=app.reverse_appurl('create')),
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

    def form_valid(self, form):
        course = self.request.cradmin_role
        multiassignment_serialize.Deserializer(
            serialized_assignments=form.cleaned_data['data'],
            course_tag=course.course_tag.tag).sync()
        # print
        # print
        # print '='*70
        # print
        # from pprint import pprint
        # pprint(form.cleaned_data)
        # print
        # print '='*70
        # print
        # print
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
            layout.Div('data', css_class="cradmin-focusfield"),
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
