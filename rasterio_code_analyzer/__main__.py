import sys

from rasterio_code_analyzer import Reporter


finder = Reporter()
code = sys.stdin.read()
finder.analyze(code)
print(finder.report())
