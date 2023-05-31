import uuid

import pytest
import requests


@pytest.mark.nhsd_apim_authorization({"access": "patient", "level": "P9", "login_form": {"username": "9912003071"}})
def test_kvm_miss(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    headers = {"Interaction-ID": str(uuid.uuid4())}
    headers.update(nhsd_apim_auth_headers)

    resp = requests.get(f"{nhsd_apim_proxy_url}", headers=headers)

    assert resp.status_code == 404
