from django.views.generic import ListView
from django.shortcuts import redirect


class TrixListViewBase(ListView):
    '''
    This forms the basis for all other list views and is used to apply sitewide (limited to user
    sites) context.
    '''
    def get_context_data(self, **kwargs):
        context = super(TrixListViewBase, self).get_context_data(**kwargs)
        # Check if WCAG styles have been activated
        context['wcag'] = self.request.session.get('wcag', False)
        return context


def wcag_change(request):
    '''
    Turn the WCAG colours on or off.
    '''
    wcag = request.session.get("wcag", False)
    wcag = not wcag
    request.session["wcag"] = wcag
    return redirect('trix_student_dashboard')
