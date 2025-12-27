import os
from flask import Flask
from extensions import db, csrf

def create_app():
    app = Flask(__name__)

    # --- Secrets & CSRF ---
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "change-me")  # Set in Railway Variables

    # --- Database config ---
    # Prefer DATABASE_URL from Railway. Falls back to SQLite for local dev.
    
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///data.db"   # local dev fallback)

    # If you stay with SQLite on Railway, make it absolute and writable:
    # db_url = os.getenv("DATABASE_URL", "sqlite:////app/data.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Init extensions
    db.init_app(app)
    csrf.init_app(app)

    # Register blueprints / routes after app + db are ready
    from routes import bp as routes_bp  
    app.register_blueprint(routes_bp)

    # Ensure tables exist (for simple apps that do not use Alembic yet)
    @app.before_first_request
    def _create_tables_if_missing():
        # Import models so SQLAlchemy knows about them
        from models import Task  # noqa: F401
        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    # Railway expects listening on 0.0.0.0
    app.run(host="0.0.0.0", port=port, debug=True)
