
from app import app, db
from models import Task  # import every model you want tables for

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("✅ data.db created (or already exists)")
