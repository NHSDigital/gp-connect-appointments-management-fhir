import pytest
import requests


@pytest.mark.smoketest
@pytest.mark.auth
@pytest.mark.integration
@pytest.mark.user_restricted_separate_nhs_login
@pytest.mark.nhsd_apim_authorization({"access": "patient", "level": "P9", "login_form": {"username": "9449305552"}})
def test_mock_receiver_slot_path(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    headers = {
        "X-Request-ID": "60E0B220-8136-4CA5-AE46-1D97EF59D068",
    }
    params = {
        'start': 'ge2020-05-09',
        'end': 'le2020-05-10',
        'status': 'free',
        '_include': 'Slot:schedule'
    }
    headers.update(nhsd_apim_auth_headers)

    headers.update(nhsd_apim_auth_headers)
    resp = requests.get(
        f"{nhsd_apim_proxy_url}/Slot",
        headers=headers,
        params=params
    )
    assert resp.status_code == 200
