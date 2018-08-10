from django.conf import settings


def add_custom_template(dir):
    template = getattr(settings, 'TEMPLATES', None)
    if template is None:
        return
    template[0]['DIRS'].append(dir)
