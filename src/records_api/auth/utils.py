from fastapi.security import HTTPBearer
from jwt import PyJWKClient
from os import environ

bearer_scheme = HTTPBearer()

tenant_id = environ.get("ENTRA_TENANT_ID")
audience = environ.get("ENTRA_API_CLIENT_ID")
# il token deve provenire dal mio tenant
issuer = f"https://login.microsoftonline.com/{tenant_id}/v2.0"

jwks_url = (f"https://login.microsoftonline.com/{tenant_id}""/discovery/v2.0/keys")

jwks_client = PyJWKClient(jwks_url)