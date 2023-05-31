"""
See
https://github.com/NHSDigital/pytest-nhsd-apim/blob/main/tests/test_examples.py
for more ideas on how to test the authorization of your API.
"""
import pytest
import requests
from os import getenv
# from example_loader import load_example


@pytest.mark.smoketest
def test_ping(nhsd_apim_proxy_url):
    resp = requests.get(f"{nhsd_apim_proxy_url}/_ping")
    assert resp.status_code == 200


@pytest.mark.smoketest
def test_wait_for_ping(nhsd_apim_proxy_url):
    retries = 0
    resp = requests.get(f"{nhsd_apim_proxy_url}/_ping")
    deployed_commitId = resp.json().get("commitId")

    while (deployed_commitId != getenv('SOURCE_COMMIT_ID')
           and retries <= 30
           and resp.status_code == 200):
        resp = requests.get(f"{nhsd_apim_proxy_url}/_ping")
        deployed_commitId = resp.json().get("commitId")
        retries += 1

    if resp.status_code != 200:
        pytest.fail(f"Status code {resp.status_code}, expecting 200")
    elif retries >= 30:
        pytest.fail("Timeout Error - max retries")

    assert deployed_commitId == getenv('SOURCE_COMMIT_ID')


@pytest.mark.smoketest
def test_status(nhsd_apim_proxy_url, status_endpoint_auth_headers):
    resp = requests.get(
        f"{nhsd_apim_proxy_url}/_status", headers=status_endpoint_auth_headers
    )
    assert resp.status_code == 200
    # Make some additional assertions about your status response here!


@pytest.mark.smoketest
def test_wait_for_status(nhsd_apim_proxy_url, status_endpoint_auth_headers):
    retries = 0
    resp = requests.get(f"{nhsd_apim_proxy_url}/_status", headers=status_endpoint_auth_headers)
    deployed_commitId = resp.json().get("commitId")

    while (deployed_commitId != getenv('SOURCE_COMMIT_ID')
           and retries <= 30
           and resp.status_code == 200
           and resp.json().get("version")):
        resp = requests.get(f"{nhsd_apim_proxy_url}/_status", headers=status_endpoint_auth_headers)
        deployed_commitId = resp.json().get("commitId")
        retries += 1

    if resp.status_code != 200:
        pytest.fail(f"Status code {resp.status_code}, expecting 200")
    elif retries >= 30:
        pytest.fail("Timeout Error - max retries")
    elif not resp.json().get("version"):
        pytest.fail("version not found")

    assert deployed_commitId == getenv('SOURCE_COMMIT_ID')


@pytest.mark.auth
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level0"})
def test_app_level0(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    resp = requests.get(f"{nhsd_apim_proxy_url}", headers=nhsd_apim_auth_headers)
    assert resp.status_code == 401  # unauthorized


@pytest.mark.nhsd_apim_authorization(
    {
        "access": "patient",
        "level": "P9",
        "login_form": {"username": "P9"},
    }
)
def test_nhs_login_p9(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    resp = requests.get(f"{nhsd_apim_proxy_url}", headers=nhsd_apim_auth_headers)
    assert resp.status_code == 200


@pytest.mark.auth
@pytest.mark.integration
@pytest.mark.nhsd_apim_authorization(
    {
        "access": "patient",
        "level": "P9",
        "login_form": {"username": "9000000009"}
    }
)
def test_prism_returns_external_file(nhsd_apim_proxy_url, nhsd_apim_auth_headers):

    headers = {
        "accept": "application/fhir+json",
        "X-Correlation-ID": "11C46F5F-CDEF-4865-94B2-0EE0EDCC26DA",
        "X-Request-ID": "60E0B220-8136-4CA5-AE46-1D97EF59D068",
    }
    headers.update(nhsd_apim_auth_headers)

    resp = requests.get(
        f"{nhsd_apim_proxy_url}/Patient/9000000009/Appointment",
        headers=headers
    )
    print(nhsd_apim_proxy_url, "PROXY URL")
    print(nhsd_apim_auth_headers, "HEADERS")
    print(resp.text)
    # expected_response = load_example("gp-connect-appointments-management-fhir.yaml")
    # assert resp.json() == expected_response.get("value")
