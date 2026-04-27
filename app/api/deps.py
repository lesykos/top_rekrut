from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from fastapi_plugin.fast_api_client import Auth0FastAPI
from sqlmodel import Session

from app.core.db import engine
from app.core.config import settings

auth0 = Auth0FastAPI(domain=settings.AUTH0_DOMAIN, audience=settings.AUTH0_AUDIENCE)


# A Session is what stores the objects in memory and keeps track of any
# changes needed in the data, then it uses the engine to communicate with the DB.
def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


# We create an Annotated dependency SessionDep to simplify
# the rest of the code that will use this dependency.
SessionDep = Annotated[Session, Depends(get_db)]
TokenClaimsDep = Annotated[dict, Depends(auth0.require_auth())]
TokenDep = Depends(auth0.require_auth())


# def get_current_user(session: SessionDep, token: TokenDep) -> User:
#     return user
