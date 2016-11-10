# --------------------------------------------------------------------------
# This plugin generates a customizable string of page-navigation links for
# index pages.
#
# The links can be accessed in templates as:
#
#     {{ paging.navlinks }}
#
# Default settings can be overridden by including a 'paging' dictionary in
# the site's configuration file containing one or more of the following
# options:
#
#     paging = {
#         'first': 'First',  # text for link to first page
#         'last': 'Last',    # text for link to last page
#         'prev': 'Prev',    # text for link to previous page
#         'next': 'Next',    # text for link to next page
#         'delta': 2,        # number of neighbouring pages to include
#         'multiples': 2,    # number of larger/smaller multiples to include
#         'multiple': 10,    # multiplication factor
#     }
# --------------------------------------------------------------------------

from ivy import hooks, site


# We register a callback on the 'render_page' event hook to generate our
# string of page navigation links and add it to the page object.
@hooks.register('render_page')
def add_paging_links(page):
    if page['flags']['is_paged']:
        page['paging']['navlinks'] = generate_paging_links(
            page['node'],
            page['paging']['page'],
            page['paging']['total']
        )


# Generate a string of index navigation links.
def generate_paging_links(node, page_number, total_pages):

    # Default settings can be overridden in the site's configuration file.
    data = {
        'first': 'First',
        'last': 'Last',
        'prev': 'Prev',
        'next': 'Next',
        'delta': 2,
        'multiples': 2,
        'multiple': 10,
    }
    data.update(site.config.get('paging', {}))

    # Start and end points for the sequence of numbered links.
    start = page_number - data['delta']
    end = page_number + data['delta']

    if start < 1:
        start = 1
        end = 1 + 2 * data['delta']

    if end > total_pages:
        start = total_pages - 2 * data['delta']
        end = total_pages

    if start < 1:
        start = 1

    out = []

    # First page link.
    if start > 1:
        out.append("<a class='first' href='%s'>%s</a>" % (
            node.paged_url(1, total_pages),
            data['first']
        ))

    # Previous page link.
    if page_number > 1:
        out.append("<a class='prev' href='%s'>%s</a>" % (
            node.paged_url(page_number - 1, total_pages),
            data['prev']
        ))

    # Smaller multiple links.
    if data['multiples']:
        multiples = list(range(data['multiple'], start, data['multiple']))
        for multiple in multiples[-data['multiples']:]:
            out.append("<a class='pagenum multiple' href='%s'>%s</a>" % (
                node.paged_url(multiple, total_pages), multiple
            ))

    # Sequence of numbered page links.
    for i in range(start, end + 1):
        if i == page_number:
            out.append("<span class='pagenum current'>%s</span>" % i)
        else:
            out.append("<a class='pagenum' href='%s'>%s</a>" % (
                node.paged_url(i, total_pages), i
            ))

    # Larger multiple links.
    if data['multiples']:
        lowest = (int(end / data['multiple']) + 1) * data['multiple']
        multiples = list(range(lowest, total_pages, data['multiple']))
        for multiple in multiples[:data['multiples']]:
            out.append("<a class='pagenum multiple' href='%s'>%s</a>" % (
                node.paged_url(multiple, total_pages), multiple
            ))

    # Next page link.
    if page_number < total_pages:
        out.append("<a class='next' href='%s'>%s</a>" % (
            node.paged_url(page_number + 1, total_pages),
            data['next']
        ))

    # Last page link.
    if end < total_pages:
        out.append("<a class='last' href='%s'>%s</a>" % (
            node.paged_url(total_pages, total_pages),
            data['last']
        ))

    return ''.join(out)
