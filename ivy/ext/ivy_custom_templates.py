# --------------------------------------------------------------------------
# This extension adds support for custom page templates.
# --------------------------------------------------------------------------

import ivy


# Register a callback on the 'page_tempates' filter.
@ivy.hooks.register('page_templates')
def custom_template_callback(template_list, page):
    if 'template' in page['node'].data:
        template_list.insert(0, page['node'].data['template'])
    return template_list
