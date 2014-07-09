from django.views.generic import TemplateView

from django_cradmin import crapp
from django_cradmin.viewhelpers import objecttable

from trix.trix_core import models as trix_models

# class PermalinkListView(objecttable.ObjectTableView):
#     model = trix_models.Permalink
#     columns = [
#         TitleColumn,
#         TagsColumn,
#         DescriptionIntroColumn
#     ]

#     def get_queryset_for_role(self, course):
#         return self.model.objects.filter(course=course)

class StatisticsChartView(TemplateView):
    template_name = 'trix_admin/statistics.django.html'

class TitleColumn(objecttable.SingleActionColumn):
    modelfield = 'tag'

    def get_actionurl(self, obj):
        return self.reverse_appurl('view')

class StatisticsView(objecttable.ObjectTableView):
    model = trix_models.Tag
  
    columns = [
        TitleColumn,
    ]

    def get_queryset_for_role(self, course):
        return self.model.objects.all()


class App(crapp.App):
    appurls = [
        crapp.Url(r'^$',
            StatisticsView.as_view(),
            name=crapp.INDEXVIEW_NAME),
        crapp.Url(r'^view$',
            StatisticsChartView.as_view(),
            name='view'),
    ]