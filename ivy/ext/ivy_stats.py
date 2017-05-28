# --------------------------------------------------------------------------
# This extension prints a simple stats report at the end of each build run.
# --------------------------------------------------------------------------

from ivy import hooks, site


# Register a callback on the 'exit_build' event hook.
@hooks.register('exit_build')
def print_stats():

    # The site module maintains a count of the number of pages that have been
    # rendered into html and written to disk.
    rendered, written = site.rendered(), site.written()

    # The runtime() function gives the application's running time in seconds.
    time = site.runtime()
    average = time / rendered if rendered else 0

    # Print stats.
    report =  "Rendered: %5d  ·  Written: %5d  ·  "
    report += "Time: %5.2f sec  ·  Avg: %.4f sec/page"
    print(report % (rendered, written, time, average))
