from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect

from trix.trix_core.models import Course, Tag
from trix.trix_course.views import base

class EditActivePeriodView(base.TrixCourseBaseView):
    model = Course
    template_name = "trix_course/edit_course_active_period.django.html"
    paginate_by = 20

    def get(self, request, **kwargs):
        course = get_object_or_404(Course, id=kwargs['course_id'])
        if request.user.is_course_owner(course):
            return super(EditActivePeriodView, self).get(request, **kwargs)
        else:
            raise PermissionDenied

    def get_queryset(self):
        search = self.request.GET.get('q', '').strip()
        periods = Tag.objects.filter(category='p').order_by('-id')
        if search:
            periods = periods.filter(tag__icontains=search)
        return periods

    def post(self, request, *args, **kwargs):
        course = get_object_or_404(Course, id=kwargs['course_id'])
        if not request.user.is_course_owner(course):
            raise PermissionDenied

        posted = request.POST.get('active_period', '').strip()

        if posted == '':
            if course.active_period is not None:
                course.active_period = None
                course.save()
                messages.success(request, "Active period cleared.")
            else:
                messages.info(request, "Active period unchanged.")
            return redirect(request.path)
        else:
            try:
                tag_pk = int(posted)
            except (TypeError, ValueError):
                messages.error(request, "Invalid period selected.")
                return redirect(request.path)

            tag = get_object_or_404(Tag, pk=tag_pk, category='p')

            if course.active_period_id != tag.pk:
                course.active_period = tag
                course.save()
                messages.success(request, "Active period updated.")
            else:
                messages.info(request, "Active period unchanged.")

        qs = ''
        current_page = request.GET.get('page')
        if current_page:
            qs = '?page=%s' % current_page
        return redirect(request.path + qs)

    def get_context_data(self, **kwargs):
        context = super(EditActivePeriodView, self).get_context_data(**kwargs)
        context['course'] = get_object_or_404(Course, id=self.kwargs['course_id'])
        periods_qs = self.get_queryset()
        paginator = Paginator(periods_qs, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['periods_page'] = page_obj
        context['periods'] = page_obj.object_list
        context['page_obj'] = page_obj
        context['paginator'] = paginator
        context['q'] = self.request.GET.get('q', '')
        return context
