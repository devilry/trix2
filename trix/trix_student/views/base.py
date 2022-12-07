from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import redirect
from django.views.generic import ListView


class TrixListViewBase(ListView):
    '''
    This forms the basis for all other list views and is used to apply sitewide (limited to user
    sites) context.
    '''

    def get(self, request, **kwargs):
        # Fix out of bounds pagination
        page = request.GET.get('page')
        if page:
            paginator = Paginator(self.get_queryset(), self.paginate_by)
            try:
                paginator.page(page)
            except (PageNotAnInteger, EmptyPage):
                return redirect(request.path)
        return super(TrixListViewBase, self).get(request, **kwargs)
