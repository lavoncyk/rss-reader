"""
"""
import datetime

from fastapi import params
from fastapi import security
import fastapi
import sqlalchemy as sa
import sqlalchemy.orm

from rss_reader import models
from rss_reader import security as rss_security
from rss_reader.api import crud
from rss_reader.api import deps
from rss_reader.api import schemas
from rss_reader.config import settings


router = fastapi.APIRouter(
    tags=["auth"],
)


@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
    db: sa.orm.Session = params.Depends(deps.get_db),
    form_data: security.OAuth2PasswordRequestForm = params.Depends(),
) -> schemas.Token:
    """
    OAuth2-compatible token login, get an access token for future requests.
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password,
    )
    if not user:
        raise fastapi.HTTPException(
            status_code=400,
            detail="Incorrect email or password",
        )
    if not user.is_active:
        raise fastapi.HTTPException(
            status_code=400,
            detail="Inactive user",
        )

    expires_in = datetime.timedelta(seconds=settings.ACCESS_TOKEN_EXP_SECONDS)
    access_token = rss_security.create_access_token(
        user.id, expiration_delta=expires_in
    )

    return schemas.Token(
        access_token=access_token,
    )


@router.post("/login/test-access-token", response_model=schemas.User)
def test_access_token(
    current_user: models.User = params.Depends(deps.get_current_user),
):
    """
    Test access token.
    """
    return current_user
