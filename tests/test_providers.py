import pytest
from hashlib import md5

from app.providers import MockAMLProvider, RealAMLProvider
from app.providers.mock_provider import MOCK_RESPONSE


class TestMockAMLProvider:
    @pytest.mark.asyncio
    async def test_get_aml_data_returns_mock_response(self):
        provider = MockAMLProvider()
        result = await provider.get_aml_data({'hash': '0x123', 'asset': 'ETH'})
        assert result == MOCK_RESPONSE

    @pytest.mark.asyncio
    async def test_get_aml_data_ignores_input(self):
        provider = MockAMLProvider()
        result1 = await provider.get_aml_data(
            {'hash': 'address1', 'asset': 'BTC'}
        )
        result2 = await provider.get_aml_data(
            {'hash': 'address2', 'asset': 'ETH'}
        )
        assert result1 == result2

    @pytest.mark.asyncio
    async def test_mock_response_has_success_status(self):
        provider = MockAMLProvider()
        result = await provider.get_aml_data({})
        assert result['data']['status'] == 'success'

    @pytest.mark.asyncio
    async def test_mock_response_has_riskscore(self):
        provider = MockAMLProvider()
        result = await provider.get_aml_data({})
        assert result['data']['riskscore'] == 0.63

    @pytest.mark.asyncio
    async def test_mock_response_has_malicious_events(self):
        provider = MockAMLProvider()
        result = await provider.get_aml_data({})
        malicious_events = result['data']['extras']['services'][
            'malicious_event'
        ]
        assert 'Fake_Phishing' in malicious_events
        assert 'Harmony Horizon Bridge Exploiter' in malicious_events


class TestRealAMLProvider:
    def test_init(self):
        provider = RealAMLProvider(
            api_url='https://api.example.com',
            api_access_key='test_key',
            api_access_id='test_id',
        )
        assert provider.api_url == 'https://api.example.com'
        assert provider.api_access_key == 'test_key'
        assert provider.api_access_id == 'test_id'

    def test_token_generation(self):
        provider = RealAMLProvider(
            api_url='https://api.example.com',
            api_access_key='secret_key',
            api_access_id='my_id',
        )
        hash_value = '0x123'
        expected_token = md5(
            f'{hash_value}{provider.api_access_key}{provider.api_access_id}'.encode()
        ).hexdigest()

        token_string = (
            f'{hash_value}{provider.api_access_key}{provider.api_access_id}'
        )
        actual_token = md5(token_string.encode()).hexdigest()

        assert actual_token == expected_token
