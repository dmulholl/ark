# --------------------------------------------------------------------------
# This extension adds support for user-defined node classes. Classes can
# be added as a comma-separated list via a 'classes' attribute.
# --------------------------------------------------------------------------

import ivy


# Register a callback on the 'page_classes' filter.
@ivy.hooks.register('page_classes')
def custom_classes_callback(class_list, page):
    if 'classes' in page['node']:
        for item in str(page['node']['classes']).split(','):
            class_list.append(item.strip())
    return class_list
