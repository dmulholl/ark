# ------------------------------------------------------------------------------
# This extension prints a simple stats report at the end of each build run.
# ------------------------------------------------------------------------------

import ivy
import datetime


@ivy.events.register('exit_build')
def print_stats():
    report = datetime.datetime.now().strftime("[%H:%M:%S]")
    report += f"   ·   Rendered: {ivy.site.rendered():5d}"
    report += f"   ·   Written: {ivy.site.written():5d}"
    report += f"   ·   Time: {ivy.site.runtime():6.2f} sec"
    report = report.replace('·', '\u001B[90m·\u001B[0m')
    ivy.utils.safeprint(report)
