import os

from .providers import AMLProvider, MockAMLProvider, RealAMLProvider


def get_aml_provider() -> AMLProvider:
    api_url = os.environ.get(
        'AML_API_URL', 'https://extrnlapiendpoint.silencatech.com/'
    )
    api_access_key = os.environ.get('AML_API_ACCESS_KEY')
    api_access_id = os.environ.get('AML_API_ACCESS_ID')

    if api_access_id and api_access_key:
        return RealAMLProvider(
            api_url=api_url,
            api_access_key=api_access_key,
            api_access_id=api_access_id,
        )

    return MockAMLProvider()
