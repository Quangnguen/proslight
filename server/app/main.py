from fastapi import FastAPI
from server.app.api.v1.endpoints import auth
from sqlalchemy import text

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Thiết lập CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Có thể thay đổi thành danh sách các miền cụ thể nếu cần
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the E-commerce API"}

app.include_router(auth.router, prefix="/api/v1")

from server.app.db.base import SessionLocal

db = SessionLocal()
try:
    db.execute(text("SELECT 1"))
    print("Connection successful!")
except Exception as e:
    print(f"Connection failed: {e}")
finally:
    db.close()