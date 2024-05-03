from tempfile import TemporaryDirectory
import pytest

from gradle.project import Project


@pytest.fixture
def tempdir():
    with TemporaryDirectory() as tempdir:
        yield tempdir


@pytest.fixture
def project(tempdir):
    yield Project.init(tempdir)
