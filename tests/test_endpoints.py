import pytest
from fastapi.testclient import TestClient

from main import app
from app.tasks import init_reports_dir, generate_report, get_reports_dir


@pytest.fixture(autouse=True)
def setup_reports_dir():
    init_reports_dir()
    yield


class TestCheckAddressEndpoint:
    def test_check_address_success(self):
        with TestClient(app) as client:
            response = client.post(
                '/check-address',
                json={
                    'address': '0xf2e8e0761df9acda6d6b67a219ce41e522647e26',
                    'currency': 'ETH',
                },
            )
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'success'
        assert data['risk_score'] == 0.63
        assert 'Fake_Phishing' in data['categories']
        assert (
            data['pdf_url']
            == '/report/ETH0xf2e8e0761df9acda6d6b67a219ce41e522647e26'
        )

    def test_check_address_invalid_currency(self):
        with TestClient(app) as client:
            response = client.post(
                '/check-address',
                json={'address': 'abc123', 'currency': 'INVALID'},
            )
        assert response.status_code == 422

    def test_check_address_missing_address(self):
        with TestClient(app) as client:
            response = client.post(
                '/check-address',
                json={'currency': 'BTC'},
            )
        assert response.status_code == 422

    def test_check_address_missing_currency(self):
        with TestClient(app) as client:
            response = client.post(
                '/check-address',
                json={'address': 'abc123'},
            )
        assert response.status_code == 422

    def test_check_address_address_too_long(self):
        with TestClient(app) as client:
            response = client.post(
                '/check-address',
                json={'address': 'a' * 65, 'currency': 'BTC'},
            )
        assert response.status_code == 422


class TestReportEndpoint:
    def test_get_report_not_found(self):
        with TestClient(app) as client:
            response = client.get('/report/nonexistent')
        assert response.status_code == 404
        assert response.json()['detail'] == 'Report not found'

    def test_get_report_invalid_filename_special_chars(self):
        with TestClient(app) as client:
            response = client.get('/report/test@file')
        assert response.status_code == 422

    def test_get_report_invalid_filename_underscore(self):
        with TestClient(app) as client:
            response = client.get('/report/test_file')
        assert response.status_code == 422

    def test_get_report_invalid_filename_hyphen(self):
        with TestClient(app) as client:
            response = client.get('/report/test-file')
        assert response.status_code == 422

    def test_get_report_success(self):
        generate_report(
            {'file_name': 'testreport', 'address': '0x123', 'risk_score': 0.5}
        )

        with TestClient(app) as client:
            response = client.get('/report/testreport')
        assert response.status_code == 200
        assert response.headers['content-type'] == 'application/pdf'

    def test_get_report_valid_alphanumeric(self):
        generate_report({'file_name': 'ABC123xyz', 'test': 'data'})

        with TestClient(app) as client:
            response = client.get('/report/ABC123xyz')
        assert response.status_code == 200
