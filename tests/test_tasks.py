import os

import pytest

from app import tasks
from app.tasks import init_reports_dir, get_reports_dir, generate_report


@pytest.fixture(autouse=True)
def reset_reports_dir():
    tasks.reports_dir = None
    yield
    tasks.reports_dir = None


class TestInitReportsDir:
    def test_creates_directory(self):
        result = init_reports_dir()
        assert result is not None
        assert os.path.isdir(result)
        assert 'aml_reports_' in result

    def test_returns_same_directory_on_multiple_calls(self):
        result1 = init_reports_dir()
        result2 = init_reports_dir()
        assert result1 == result2

    def test_get_reports_dir_returns_none_before_init(self):
        assert get_reports_dir() is None

    def test_get_reports_dir_returns_path_after_init(self):
        init_reports_dir()
        assert get_reports_dir() is not None


class TestGenerateReport:
    def test_raises_error_if_not_initialized(self):
        with pytest.raises(
            RuntimeError, match='Reports directory not initialized'
        ):
            generate_report({'file_name': 'test'})

    def test_creates_pdf_file(self):
        reports_dir = init_reports_dir()
        generate_report({'file_name': 'test_report', 'key1': 'value1'})

        file_path = os.path.join(reports_dir, 'test_report.pdf')
        assert os.path.isfile(file_path)

    def test_creates_pdf_with_default_filename(self):
        reports_dir = init_reports_dir()
        generate_report({'key1': 'value1'})

        file_path = os.path.join(reports_dir, 'report.pdf.pdf')
        assert os.path.isfile(file_path)

    def test_pdf_file_not_empty(self):
        reports_dir = init_reports_dir()
        generate_report({'file_name': 'nonempty', 'data': 'test'})

        file_path = os.path.join(reports_dir, 'nonempty.pdf')
        assert os.path.getsize(file_path) > 0

    def test_creates_multiple_reports(self):
        reports_dir = init_reports_dir()
        generate_report({'file_name': 'report1', 'data': 'test1'})
        generate_report({'file_name': 'report2', 'data': 'test2'})

        assert os.path.isfile(os.path.join(reports_dir, 'report1.pdf'))
        assert os.path.isfile(os.path.join(reports_dir, 'report2.pdf'))
