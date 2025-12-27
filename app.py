
import os
from flask import Flask
from extensions import db, csrf

def create_app():
    app = Flask(__name__)

    # --- Secrets ---
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")

    # --- Database URL (Railway Postgres) ---
    db_url = os.getenv("DATABASE_URL")

    if not db_url:
        # Local dev fallback to SQLite if DATABASE_URL is not present
        db_url = "sqlite:///data.db"

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # --- Extensions ---
    db.init_app(app)
    csrf.init_app(app)

    # --- Blueprints / Routes ---
    from routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    # --- Ensure tables exist on boot (Postgres starts empty) ---
    # Running inside app context ensures it works under Gunicorn workers too
    with app.app_context():
        from models import Task  # ensure models are registered
        db.create_all()

    return app


# WSGI object for Gunicorn
app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
