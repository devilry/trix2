import trix


def template_variables(request):
    template_variables_dict = {
        'TRIX_VERSION': trix.__version__
    }
    return template_variables_dict
