import pytest


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Allows tests docstrings to be printed instead of the test function names when pytest
    is invoked, at least, with `-v` parameter (verbosity).
    """
    outcome = yield
    report = outcome.get_result()

    test_fn = item.obj
    docstring = getattr(test_fn, "__doc__")
    if docstring:
        report.nodeid = docstring
