from django import forms

from trix.trix_core import models as trix_models


class ManyToManyTagInputField(forms.CharField):

    def prepare_value(self, value):
        if value:
            if isinstance(value, str):
                tags = self.to_python(value)
                return ', '.join([tag.tag for tag in tags])
            else:
                return ', '.join(tag.tag for tag in value)
        else:
            return ''

    def to_python(self, value):
        tags = []
        for tagstring in trix_models.Tag.split_commaseparated_tags(value):
            tag, created = trix_models.Tag.objects.get_or_create(tag=tagstring,
                                                                 defaults={'category': ''})
            tags.append(tag)
        return tags
