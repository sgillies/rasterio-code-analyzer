# Tests of the analyzer class.

from rasterio_code_analyzer import Analyst


def test_find_read_usage_error():

    code = """
with rasterio.open('/tmp/foo.tif', 'w') as foo:
    x = foo.read()
"""

    finder = Analyst()
    finder.analyze(code)
    report = finder.report()
    assert len(report) == 1
    record = report.pop()
    assert record["name"] == "foo"
