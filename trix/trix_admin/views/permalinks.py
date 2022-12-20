from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import truncatechars
from cradmin_legacy.viewhelpers import objecttable
from cradmin_legacy.viewhelpers import create
from cradmin_legacy.viewhelpers import update
from cradmin_legacy.viewhelpers import delete
from cradmin_legacy import crapp
from crispy_forms import layout

from trix.trix_core import models as trix_models
from trix.trix_admin import formfields


class PermalinkQuerysetForRoleMixin(object):
    def get_queryset_for_role(self, course):
        return self.model.objects.filter(course=course)\
            .prefetch_related('tags')


class TitleColumn(objecttable.MultiActionColumn):
    modelfield = 'title'

    def get_buttons(self, permalink):
        return [
            objecttable.Button(
                label=_('Edit'),
                url=self.reverse_appurl('edit', args=[permalink.id])),
            objecttable.Button(
                label=_('View'),
                url=reverse('trix_student_permalink', args=[permalink.id])),
            objecttable.Button(
                label=_('Delete'),
                url=self.reverse_appurl('delete', args=[permalink.id]),
                buttonclass="btn btn-sm btn-danger"),
        ]


class DescriptionIntroColumn(objecttable.PlainTextColumn):
    modelfield = 'description'

    def render_value(self, permalink):
        return truncatechars(permalink.description, 50)


class TagsColumn(objecttable.PlainTextColumn):
    modelfield = 'tags'

    def is_sortable(self):
        return False

    def render_value(self, permalink):
        return ', '.join(tag.tag for tag in permalink.tags.all())


class PermalinkListView(PermalinkQuerysetForRoleMixin, objecttable.ObjectTableView):
    model = trix_models.Permalink
    columns = [
        TitleColumn,
        TagsColumn,
        DescriptionIntroColumn
    ]
    searchfields = [
        'title',
        'tags__tag',
        'description',
    ]

    def get_buttons(self):
        app = self.request.cradmin_app
        return [
            objecttable.Button(label=_('Create'), url=app.reverse_appurl('create')),
        ]


class PermalinkCreateUpdateMixin(object):
    model = trix_models.Permalink
    roleid_field = 'course'

    def get_field_layout(self):
        return [
            layout.Div('title', css_class="trix-focusfield"),
            # layout.Fieldset(_('Organize'), 'tags'),
            layout.Div('tags', css_class="trix-focusfield"),
            layout.Div('description', css_class="trix-focusfield"),
        ]

    def get_form(self, *args, **kwargs):
        form = super(PermalinkCreateUpdateMixin, self).get_form(*args, **kwargs)
        form.fields['tags'] = formfields.ManyToManyTagInputField(required=False)
        return form

    def save_object(self, form, commit=True):
        permalink = super(PermalinkCreateUpdateMixin, self).save_object(form, commit=commit)
        if commit:
            # Replace the tags with the new tags
            permalink.tags.clear()
            for tag in form.cleaned_data['tags']:
                permalink.tags.add(tag)
        return permalink

    def form_saved(self, permalink):
        course = self.request.cradmin_role
        if not permalink.tags.filter(tag=course.course_tag).exists():
            permalink.tags.add(course.course_tag)


class PermalinkCreateView(PermalinkCreateUpdateMixin, create.CreateView):
    """
    View used to create new permalinks.
    """


class PermalinkUpdateView(PermalinkQuerysetForRoleMixin,
                          PermalinkCreateUpdateMixin,
                          update.UpdateView):
    """
    View used to create edit existing permalinks.
    """


class PermalinkDeleteView(PermalinkQuerysetForRoleMixin, delete.DeleteView):
    """
    View used to delete existing permalinks.
    """
    model = trix_models.Permalink
    template_name = "trix_admin/delete.django.html"


class App(crapp.App):
    appurls = [
        crapp.Url(
            r'^$',
            PermalinkListView.as_view(),
            name=crapp.INDEXVIEW_NAME),
        crapp.Url(
            r'^create$',
            PermalinkCreateView.as_view(),
            name="create"),
        crapp.Url(
            r'^edit/(?P<pk>\d+)$',
            PermalinkUpdateView.as_view(),
            name="edit"),
        crapp.Url(
            r'^delete/(?P<pk>\d+)$',
            PermalinkDeleteView.as_view(),
            name="delete")
    ]
