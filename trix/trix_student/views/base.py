from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic import TemplateView


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

    def get_context_data(self, **kwargs):
        context = super(TrixListViewBase, self).get_context_data(**kwargs)
        # Check if WCAG styles have been activated
        context['wcag'] = self.request.session.get('wcag', True)
        return context


class TrixTemplateViewBase(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(TrixTemplateViewBase, self).get_context_data(**kwargs)
        # Check if WCAG styles have been activated
        context['wcag'] = self.request.session.get('wcag', True)
        return context


def wcag_change(request):
    '''
    Turn the WCAG colours on or off.
    '''
    wcag = request.session.get("wcag", True)
    wcag = not wcag
    request.session["wcag"] = wcag
    return redirect('trix_student_dashboard')
