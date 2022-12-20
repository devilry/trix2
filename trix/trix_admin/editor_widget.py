import json

from xml.sax.saxutils import quoteattr

from django.utils.translation import pgettext
from django import forms


class DevilryMarkdownWidget(forms.widgets.Textarea):
    template_name = 'trix_admin/editor/devilry_markdown_editor.django.html'

    def __init__(self, *args, label='', request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.label = label or pgettext('trix markdown widget', 'Comment text')

    @property
    def preview_enabled(self):
        return False

    def get_context(self, name, value, attrs):
        value = value or ''
        context = super().get_context(name, value, attrs)
        context['attributes'] = ' '.join(
            f'{key}={quoteattr(value)}'
            for key, value in {
                'name': name,
                'value': value,
                'placeholder': pgettext(
                    'Trix markdown widget',
                    'Write your comment here'
                ),
                'labelText': self.label,
                'helpText': pgettext(
                    'trix markdown widget',
                    'Write a comment in markdown format. Use <strong>**text here**</strong>'
                    ' for bold and <em>*text here*</em> for italic.'
                ),
                'markdownGuideLinkText': pgettext(
                    'Trix markdown widget',
                    'Here you can get an overview of the supported Markdown.'),
                'markdownGuideLinkUrl': '/markdown-help',
                'markdownPreviewConfig': json.dumps({
                    'editorActiveButtonText': pgettext(
                        'Trix markdown widget',
                        'Write'),
                    'previewActiveButtonText': pgettext(
                        'Trix markdown widget',
                        'Preview'),
                    'previewApiErrorMessage': pgettext(
                        'Trix markdown widget',
                        'Something went wrong.'
                    ),
                    'previewApiFetchingMessage': pgettext(
                        'Trix markdown widget',
                        'Preparing preview'
                    ),
                    'enabled': self.preview_enabled
                }),
                'toolbarConfig': json.dumps({
                    'heading': {
                        'tooltip': pgettext(
                            'Trix markdown widget toolbar tooltip text',
                            'Heading')
                    },
                    'bold': {
                        'placeholderText': pgettext(
                            'Trix markdown widget toolbar placeholder text',
                            'Add text here'),
                        'tooltip': pgettext(
                            'Trix markdown widget toolbar tooltip text',
                            'Bold')
                    },
                    'italic': {
                        'placeholderText': pgettext(
                            'Trix markdown widget toolbar placeholder text',
                            'Add text here'),
                        'tooltip': pgettext(
                            'Trix markdown widget toolbar tooltip text',
                            'Italic')
                    },
                    'link': {
                        'placeholderText': pgettext(
                            'Trix markdown widget toolbar placeholder text',
                            'Add text here'),
                        'tooltip': pgettext(
                            'Trix markdown widget toolbar tooltip text',
                            'Link')
                    },
                    'codeInline': {
                        'tooltip': pgettext(
                            'Trix markdown widget toolbar tooltip text',
                            'Code')
                    },
                    'codeBlock': {
                        'placeholderText': pgettext(
                            'Trix markdown widget toolbar placeholder text',
                            'Programminglanguage'),
                        'tooltip': pgettext(
                            'Trix markdown widget toolbar tooltip text',
                            'Code-block')
                    },
                    'unorderedList': {
                        'tooltip': pgettext(
                            'Trix markdown widget toolbar tooltip text',
                            'Bulleted list')
                    },
                    'orderedList': {
                        'tooltip': pgettext(
                            'Trix markdown widget toolbar tooltip text',
                            'Numbered list')
                    }
                })
            }.items()
        )
        return context


class DevilryMarkdownNoPreviewWidget(DevilryMarkdownWidget):
    @property
    def preview_enabled(self):
        return False
