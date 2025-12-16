import pytest
from pydantic import ValidationError

from app.schemas import CheckAddressRequest, CheckAddressResponse


class TestCheckAddressRequest:
    def test_valid_request_btc(self):
        request = CheckAddressRequest(
            address='1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa', currency='BTC'
        )
        assert request.address == '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa'
        assert request.currency == 'BTC'

    def test_valid_request_eth(self):
        request = CheckAddressRequest(
            address='0xf2e8e0761df9acda6d6b67a219ce41e522647e26',
            currency='ETH',
        )
        assert request.currency == 'ETH'

    def test_valid_request_usdt(self):
        request = CheckAddressRequest(
            address='TN2Y5Qzf8RdVH7KJYCQZ7gP2bLmNdVzq2L', currency='USDT'
        )
        assert request.currency == 'USDT'

    def test_invalid_currency(self):
        with pytest.raises(ValidationError) as exc_info:
            CheckAddressRequest(address='abc123', currency='DOGE')
        assert 'currency' in str(exc_info.value)

    def test_address_max_length(self):
        with pytest.raises(ValidationError) as exc_info:
            CheckAddressRequest(address='a' * 65, currency='BTC')
        assert 'address' in str(exc_info.value)

    def test_address_at_max_length(self):
        request = CheckAddressRequest(address='a' * 64, currency='BTC')
        assert len(request.address) == 64


class TestCheckAddressResponse:
    def test_pending_response(self):
        response = CheckAddressResponse(status='pending')
        assert response.status == 'pending'
        assert response.risk_score is None
        assert response.risk_level is None
        assert response.categories is None
        assert response.pdf_url is None

    def test_success_response(self):
        response = CheckAddressResponse(
            status='success',
            risk_score=0.63,
            risk_level='medium',
            categories=['Fake_Phishing'],
            pdf_url='/report/ETH0x123',
        )
        assert response.status == 'success'
        assert response.risk_score == 0.63
        assert response.risk_level == 'medium'
        assert response.categories == ['Fake_Phishing']
        assert response.pdf_url == '/report/ETH0x123'

    def test_success_response_with_none_values(self):
        response = CheckAddressResponse(
            status='success',
            risk_score=0.5,
        )
        assert response.status == 'success'
        assert response.risk_score == 0.5
        assert response.risk_level is None
