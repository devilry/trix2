import markdown
from django.utils.safestring import mark_safe


def assignment_markdown(inputmarkdown):
    """
    The Mardown parser used for assignment text and solutions.
    """
    md = markdown.Markdown(
        output_format='html5',
        extensions=[
            'markdown.extensions.codehilite',  # Syntax hilite code
            'markdown.extensions.fenced_code',  # Support github style code blocks
            'markdown.extensions.nl2br',  # Support github style newline handling
            'markdown.extensions.sane_lists',  # Break into new ul/ol tag when the next line starts
                                               # with another class of list indicator
            'markdown.extensions.smart_strong',  # Do not let hello_world create an <em>,
            'markdown.extensions.def_list',  # Support definition lists
            'markdown.extensions.tables',  # Support tables
        ])
    return mark_safe(md.convert(inputmarkdown))
