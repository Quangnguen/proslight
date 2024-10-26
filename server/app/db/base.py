from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker
from server.app.core.config import settings

# Tạo engine từ URL của cơ sở dữ liệu mà không có 'connect_args'
engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Thử kết nối đến cơ sở dữ liệu và in ra thông điệp thành công hoặc lỗi
try:
    with engine.connect() as connection:
        print("Connect thành công!")
        # In danh sách các bảng trong cơ sở dữ liệu
        metadata = MetaData()
        metadata.reflect(bind=engine)
        print("Các bảng trong cơ sở dữ liệu:", metadata.tables.keys())
except Exception as e:
    print(f"Connect thất bại: {e}")

# Hàm get_db để lấy phiên bản session từ cơ sở dữ liệu
def get_db():
    db = SessionLocal()
    print(db)
    try:
        yield db
    finally:
        db.close()

