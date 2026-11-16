# fastapi utils
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from fastapi import HTTPException, Depends
# jwt utils
import jwt
from jwt import PyJWKClient
from jwt.exceptions import PyJWKClientConnectionError,PyJWKClientError
# other utils
from os import environ
from typing import Annotated
from dotenv import load_dotenv
import logging

bearer_scheme = HTTPBearer()

# carico env variables
load_dotenv()

tenant_id = environ.get("ENTRA_TENANT_ID")
audience = environ.get("ENTRA_API_CLIENT_ID")
# il token deve provenire dal mio tenant
issuer = f"https://login.microsoftonline.com/{tenant_id}/v2.0"
# URL per le chiavi JWKS
jwks_url = f"https://login.microsoftonline.com/{tenant_id}""/discovery/v2.0/keys"
# client per le chiavi per recuperare le chiavi JWKS
jwks_client = PyJWKClient(jwks_url)

logger = logging.getLogger(__name__)

# validate token function
def validate_token(credentials: Annotated[HTTPAuthorizationCredentials,Depends(bearer_scheme)]):
    token = credentials.credentials
    try:
        # legge il key-id e cerca la chiave pubblica corrispondente 
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        # decodifica il token
        #exp = expiration, nbf = not before, iss = issuer, aud = audience, tid = tenant id, ver = version
        claims = jwt.decode(token, signing_key.key,algorithms=["RS256"], audience=audience, issuer=issuer,options={"require":["exp","nbf","iss","aud","tid","ver"]}) 
        if claims["tid"] != tenant_id or claims["ver"] != "2.0":
            raise jwt.InvalidTokenError("Invalid tenant or version")

    except PyJWKClientConnectionError as exc:
        # errore connessione jwks per ottenere la chiave pubblica
        logger.error("Failed to get signing key")
        raise HTTPException(status_code=503, detail="Authentication service unavailable") from exc
    # errore token non valido
    except (jwt.InvalidTokenError, PyJWKClientError) as exc:
        raise HTTPException(
            status_code=401,
            detail="Invalid access token",
            headers={"WWW-Authenticate": "Bearer"}
        ) from exc
    return claims
        