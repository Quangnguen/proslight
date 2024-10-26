from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from typing import Type
from sqlalchemy.orm import Session
from server.app.core.security import verify_access_token
from server.app.db.models.user import User
from server.app.schemas.user import TokenData
from server.app.db.base import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


#get_current_user: Lấy người dùng hiện tại từ token và kiểm tra tính hợp lệ của token. Nếu token không hợp lệ, sẽ trả về lỗi 401.
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Type[User]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data: TokenData = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user
