import os

from django.conf import settings
from django.template.loader import render_to_string


def partials_list(request):
    """ Get list of partial templates to use with angularJS,
        and render it to html

    """
    partial_template_files = []
    for template_dir in (settings.TEMPLATE_DIRS):
        for dir, dirnames, filenames in os.walk(template_dir):
            if not dir.endswith("partials"):
                continue
            for filename in filenames:
                if (not filename.startswith("_")):
                    partial_template_files.append((
                        filename,
                        os.path.join(dir, filename)
                    ))

    # load templates and render html
    partials = {}
    for partial_name, partial_path in partial_template_files:
        rendered = render_to_string(partial_path)
        partials[partial_name] = rendered

    return {'partials': partials}
