# --------------------------------------------------------------------------
# This extension adds support for user-defined node classes. Classes can
# be added as a comma-separated list via a 'classes' attribute.
# --------------------------------------------------------------------------

import ivy


# Register a callback on the 'page_classes' filter.
@ivy.hooks.register('page_classes')
def custom_classes_callback(classes, page):
    if 'classes' in page['node'].data:
        for item in str(page['node'].data['classes']).split(','):
            classes.append(item.strip())
    return classes
