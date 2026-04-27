from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.core.db import engine


# A Session is what stores the objects in memory and keeps track of any
# changes needed in the data, then it uses the engine to communicate with the DB.
def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


# We create an Annotated dependency SessionDep to simplify
# the rest of the code that will use this dependency.
SessionDep = Annotated[Session, Depends(get_db)]
# TokenDep = Annotated[str, Depends(reusable_oauth2)]

# def get_current_user(session: SessionDep, token: TokenDep) -> User:
#     return user
