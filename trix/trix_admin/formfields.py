from django import forms

from trix.trix_core import models as trix_models


class ManyToManyTagInputField(forms.CharField):

    def prepare_value(self, value):
        if value:
            return trix_models.Tag.objects.filter(id__in=value).to_unicode()
        else:
            return ''

    def to_python(self, value):
        tags = []
        for tagstring in trix_models.Tag.split_commaseparated_tags(value):
            tag = trix_models.Tag.objects.get_or_create(tagstring)
            tags.append(tag)
        return tags
