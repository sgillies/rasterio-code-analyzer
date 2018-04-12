# Tests of the analyzer class.

import ast
from io import StringIO
import sys

from rasterio_code_analyzer import is_w_mode_open_call, main, Reporter


def test_is_call():
    code = "rasterio.open('foo.tif', 'w')"
    tree = ast.parse(code)
    node = tree.body[0].value
    assert is_w_mode_open_call(node)


def test_report_read_usage_error():
    """Report deprecated usage, with context manager"""

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
    """Report deprecated usage, no context manager"""

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
    """Report deprecated usage, chained"""

    code = """
rasterio.open('/tmp/foo.tif', 'w').read()
"""

    finder = Reporter()
    finder.analyze(code)
    report = finder.report()
    assert len(report) == 1
    record = report.pop()
    assert record["name"] is None


def test_report_read_usage_error_func():
    """Report deprecated usage in a function"""

    code = """
def func(path):
    with rasterio.open(path, 'w') as dst:
        dst.read()
"""

    finder = Reporter()
    finder.analyze(code)
    report = finder.report()
    assert len(report) == 1
    record = report.pop()
    assert record["name"] == "dst"


def test_report_read_usage_error_class():
    """Report deprecated usage in a class"""

    code = """
class C(object):
    def __init__(self, path):
        with rasterio.open(path, 'w') as dst:
            dst.read()
"""

    finder = Reporter()
    finder.analyze(code)
    report = finder.report()
    assert len(report) == 1
    record = report.pop()
    assert record["name"] == "dst"


def test_report_read_usage_error_lambda():
    """Report deprecated usage in a lambda expr"""

    code = """
lambda path: rasterio.open(path, 'w').read()
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


def test_main(tmpdir, monkeypatch):
    """Main function works"""
    tmpdir.join("test.py").write("rasterio.open('foo.tif', 'w').read()")
    monkeypatch.setattr(sys, "argv", ["main", str(tmpdir.join("test.py"))])
    stdout = StringIO()
    monkeypatch.setattr(sys, "stdout", stdout)
    main()
    assert "is called on line 1 and column 0" in stdout.getvalue()
