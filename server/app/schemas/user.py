from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

#Dữ liệu yêu cầu khi người dùng đăng nhập.
class UserLogin(BaseModel):
    email: str
    password: str

# Token trả về khi đăng nhập thành công
class Token(BaseModel):
    access_token: str
    token_type: str

#Lưu trữ thông tin người dùng sau khi giải mã token
class TokenData(BaseModel):
    email: str | None = None
