from vonage.camara_auth import CamaraAuth
from util import *

import responses


@responses.activate
def test_oidc_request(camara_auth: CamaraAuth):
    stub(
        responses.POST,
        'https://api-eu.vonage.com/oauth2/bc-authorize',
        fixture_path='camara_auth/oidc_request.json',
    )

    response = camara_auth.make_oidc_request(
        number='447700900000',
        scope='dpv:FraudPreventionAndDetection#check-sim-swap',
    )

    assert response['auth_req_id'] == 'arid/8b0d35f3-4627-487c-a776-aegtdsf4rsd2'
    assert response['expires_in'] == 300
    assert response['interval'] == 0


@responses.activate
def test_request_camara_access_token(camara_auth: CamaraAuth):
    stub(
        responses.POST,
        'https://api-eu.vonage.com/oauth2/token',
        fixture_path='camara_auth/token_request.json',
    )

    oidc_response = {
        'auth_req_id': 'arid/8b0d35f3-4627-487c-a776-aegtdsf4rsd2',
        'expires_in': 300,
        'interval': 0,
    }
    response = camara_auth.request_camara_token(oidc_response)

    assert (
        response
        == 'eyJhbGciOiJSUzI1NiIsImprdSI6Imh0dHBzOi8vYW51YmlzLWNlcnRzLWMxLWV1dzEucHJvZC52MS52b25hZ2VuZXR3b3Jrcy5uZXQvandrcyIsImtpZCI6IkNOPVZvbmFnZSAxdmFwaWd3IEludGVybmFsIENBOjoxOTUxODQ2ODA3NDg1NTYwNjYzODY3MTM0NjE2MjU2MTU5MjU2NDkiLCJ0eXAiOiJKV1QiLCJ4NXUiOiJodHRwczovL2FudWJpcy1jZXJ0cy1jMS1ldXcxLnByb2QudjEudm9uYWdlbmV0d29ya3MubmV0L3YxL2NlcnRzLzA4NjliNDMyZTEzZmIyMzcwZTk2ZGI4YmUxMDc4MjJkIn0.eyJwcmluY2lwYWwiOnsiYXBpS2V5IjoiNGI1MmMwMGUiLCJhcHBsaWNhdGlvbklkIjoiMmJlZTViZWQtNmZlZS00ZjM2LTkxNmQtNWUzYjRjZDI1MjQzIiwibWFzdGVyQWNjb3VudElkIjoiNGI1MmMwMGUiLCJjYXBhYmlsaXRpZXMiOlsibmV0d29yay1hcGktZmVhdHVyZXMiXSwiZXh0cmFDb25maWciOnsiY2FtYXJhU3RhdGUiOiJmb0ZyQndnOFNmeGMydnd2S1o5Y3UrMlgrT0s1K2FvOWhJTTVGUGZMQ1dOeUlMTHR3WmY1dFRKbDdUc1p4QnY4QWx3aHM2bFNWcGVvVkhoWngvM3hUenFRWVkwcHpIZE5XL085ZEdRN1RKOE9sU1lDdTFYYXFEcnNFbEF4WEJVcUpGdnZTTkp5a1A5ZDBYWVN4ajZFd0F6UUFsNGluQjE1c3VMRFNsKy82U1FDa29Udnpld0tvcFRZb0F5MVg2dDJVWXdEVWFDNjZuOS9kVWxIemN3V0NGK3QwOGNReGxZVUxKZyt3T0hwV2xvWGx1MGc3REx0SCtHd0pvRGJoYnMyT2hVY3BobGZqajBpeHQ1OTRsSG5sQ1NYNkZrMmhvWEhKUW01S3JtOVBKSmttK0xTRjVsRTd3NUxtWTRvYTFXSGpkY0dwV1VsQlNQY000YnprOGU0bVE9PSJ9fSwiZmVkZXJhdGVkQXNzZXJ0aW9ucyI6e30sImF1ZCI6ImFwaS1ldS52b25hZ2UuY29tIiwiZXhwIjoxNzE3MDkyODY4LCJqdGkiOiJmNDZhYTViOC1hODA2LTRjMzctODQyMS02OGYwMzJjNDlhMWYiLCJpYXQiOjE3MTcwOTE5NzAsImlzcyI6IlZJQU0tSUFQIiwibmJmIjoxNzE3MDkxOTU1fQ.iLUbyDPR1HGLKh29fy6fqK65Q1O7mjWOletAEPJD4eu7gb0E85EL4M9R7ckJq5lIvgedQt3vBheTaON9_u-VYjMqo8ulPoEoGUDHbOzNbs4MmCW0_CRdDPGyxnUhvcbuJhPgnEHxmfHjJBljncUnk-Z7XCgyNajBNXeQQnHkRF_6NMngxJ-qjjhqbYL0VsF_JS7-TXxixNL0KAFl0SeN2DjkfwRBCclP-69CTExDjyOvouAcchqi-6ZYj_tXPCrTADuzUrQrW8C5nHp2-XjWJSFKzyvi48n8V1U6KseV-eYzBzvy7bJf0tRMX7G6gctTYq3DxdC_eXvXlnp1zx16mg'
    )
