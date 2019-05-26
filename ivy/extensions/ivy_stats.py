# ------------------------------------------------------------------------------
# This extension prints a count of pages rendered and pages written to disk at
# the end of each build run.
# ------------------------------------------------------------------------------

from ivy import hooks, site, utils


# Register a callback on the 'exit_build' event hook.
@hooks.register('exit_build')
def print_stats():

    # The site module maintains a count of the number of pages that have been
    # rendered into html and written to disk.
    rendered, written = site.rendered(), site.written()

    # The runtime() function gives the application's runtime in seconds.
    time = site.runtime()
    average = time / rendered if rendered else 0

    # Assemble the stats report.
    report =  "Rendered: %5d  ·  Written: %5d  ·  "
    report += "Time: %5.2f sec  ·  Avg: %.4f sec/page"

    # Make the dots grey before printing.
    report = report.replace('·', '\u001B[90m·\u001B[0m')
    utils.safeprint(report % (rendered, written, time, average))
