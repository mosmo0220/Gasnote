"""Token Refresh crud opperation on Database"""
from sqlalchemy.orm import Session

import models.orm_models as models
import models.models as schemas

def get_token_refresh_rate(db: Session, user_id: int) -> schemas.RefreshToken:
    """Request to db to access token refresh rate"""
    result = db.query(models.TokenRefresh).filter(models.TokenRefresh.user_id == user_id).first()
    if result is None:
        return None
    return_token_refresh = schemas.RefreshToken(user_id=result.user_id, id=result.id,
                                                refresh_count=result.refresh_count)
    return return_token_refresh

def create_token_count(db: Session, refresh_token: schemas.RefreshTokenCreate):
    """Request to db to create token counter"""
    # pylint: disable=E1123
    result = models.TokenRefresh(user_id=refresh_token.user_id, refresh_count=0)
    db.add(result)
    db.commit()
    db.refresh(result)

    return_token_refresh = schemas.RefreshToken(user_id=result.user_id, id=result.id,
                                                refresh_count=result.refresh_count)
    return return_token_refresh

def update_token_count(db: Session, user_id: int, count: int):
    """Request to db to update token counter"""
    token_refresh = db.query(models.TokenRefresh).filter(models.TokenRefresh.user_id
                                                         == user_id).first()
    if token_refresh is None:
        return "Token counter is not created"
    if count is not None:
        token_refresh.refresh_count = count

    print(token_refresh.refresh_count)

    db.add(token_refresh)
    db.commit()
    return None
