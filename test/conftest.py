import pytest  # noqa: F401

def pytest_addoption(parser):
    parser.addoption("--nodb", action="store_true", help="disable db wiping")
