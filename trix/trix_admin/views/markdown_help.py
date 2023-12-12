from django.views.generic import TemplateView


class MarkdownHelpView(TemplateView):
    template_name = 'trix_admin/editor/markdown_help.django.html'