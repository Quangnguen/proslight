from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from server.app.schemas import user as user_schema
from server.app.core.security import verify_password, create_access_token
from server.app.db.models import user as user_model
from server.app.dependencies.auth import get_current_user
from server.app.db.base import get_db

router = APIRouter()


@router.post("/admin/login", response_model=user_schema.Token)
async def login(
        #OAuth2PasswordRequestForm: Đây là form yêu cầu chứa username (email) và password, tự động xử lý thông qua FastAPI.
        form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(user_model.User).filter(user_model.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password"
        )

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

