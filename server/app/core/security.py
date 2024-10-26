from datetime import datetime, timedelta
from jose import JWTError, jwt
import hashlib
from server.app.core.config import settings
from server.app.schemas.user import TokenData

# Mã hóa mật khẩu bằng MD5
def get_password_hash(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()

# Kiểm tra mật khẩu nhập vào với mật khẩu đã mã hóa
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return get_password_hash(plain_password) == hashed_password

# Tạo access token với JWT
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# Xác thực JWT token, giải mã và trả về email người dùng
def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return TokenData(email=email)
    except JWTError:
        raise credentials_exception
