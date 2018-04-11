# Tests of the analyzer class.

import ast

from rasterio_code_analyzer import is_w_mode_open_call, Reporter


def test_is_call():
    code = "rasterio.open('foo.tif', 'w')"
    tree = ast.parse(code)
    node = tree.body[0].value
    assert is_w_mode_open_call(node)


def test_report_read_usage_error():
    """Report read from an object opened in 'w' mode"""

    code = """
with rasterio.open('/tmp/foo.tif', 'w') as dataset:
    dataset.read()
"""

    finder = Reporter()
    finder.analyze(code)
    report = finder.report()
    assert len(report) == 1
    record = report.pop()
    assert record["name"] == "dataset"


def test_report_read_usage_error2():
    """Report read from an object opened in 'w' mode"""

    code = """
dataset = rasterio.open('/tmp/foo.tif', 'w')
dataset.read()
"""

    finder = Reporter()
    finder.analyze(code)
    report = finder.report()
    assert len(report) == 1
    record = report.pop()
    assert record["name"] == "dataset"


def test_report_read_usage_error3():
    """Report read from an object opened in 'w' mode"""

    code = """
rasterio.open('/tmp/foo.tif', 'w').read()
"""

    finder = Reporter()
    finder.analyze(code)
    report = finder.report()
    assert len(report) == 1
    record = report.pop()
    assert record["name"] is None


def test_report_no_read_usage_error():
    """Default read mode is not reported"""

    code = """
with rasterio.open('/tmp/dataset.tif') as dataset:
    x = dataset.read()
"""

    finder = Reporter()
    finder.analyze(code)
    report = finder.report()
    assert len(report) == 0
