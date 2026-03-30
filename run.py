import os
from dotenv import load_dotenv
load_dotenv()  # Load .env file before anything else

import time
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import inspect
from app import create_app, db
from app.models import Student, Course, AttendanceRecord, User
from app.routes.auth import auth_bp
from flask_jwt_extended import JWTManager


def ensure_db():
    if os.getenv("FLASK_ENV") == "production":
        return # Render/Cloud providers manage the DB creation for you

    url = os.getenv("DATABASE_URL", "postgresql://postgres:12345678@localhost:5433/campusvision_db")
    url = url.replace("postgresql://", "")
    credentials, rest = url.split("@")
    user, password = credentials.split(":", 1)  # limit split to 1 to handle passwords with ":"
    host_port, dbname = rest.split("/")
    host, port = host_port.split(":") if ":" in host_port else (host_port, "5432")

    for attempt in range(10):
        try:
            conn = psycopg2.connect(host=host, port=port, user=user, password=password, database="postgres")
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{dbname}'")
            if not cur.fetchone():
                cur.execute(f"CREATE DATABASE {dbname}")
                print(f"Created database '{dbname}'.")
            cur.close()
            conn.close()
            return
        except Exception as e:
            print(f"Waiting for database... ({attempt + 1}/10): {e}")
            time.sleep(3)

    # Fix: raise after all retries fail instead of silently continuing
    raise RuntimeError("Could not connect to the database after 10 attempts. Check your DATABASE_URL and PostgreSQL status.")


app = create_app()
# JWT Configuration
app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key-123")
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
jwt = JWTManager(app)

# Ensure Auth Blueprint is registered if not done in factory
if "auth" not in app.blueprints:
    app.register_blueprint(auth_bp, url_prefix="/api/auth")


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "Student": Student, "Course": Course, "AttendanceRecord": AttendanceRecord}


if __name__ == "__main__":
    # Fix: ensure_db() only runs when the script is executed directly
    ensure_db()

    # Fix: merged into a single app context block; inspect imported at top of file
    with app.app_context():
        db.create_all()
        # Create default admin if missing
        if not User.query.filter_by(username="Denzel").first():
            admin = User(username="Denzel", role="admin")
            admin.set_password("Denzel2010")
            db.session.add(admin)
            db.session.commit()
            print("Default admin created: Denzel / Denzel2010")
        # Create shared lecturer account if missing
        if not User.query.filter_by(username="admin").first():
            lecturer = User(username="admin", role="lecturer")
            lecturer.set_password("admin123")
            db.session.add(lecturer)
            db.session.commit()
            print("Shared lecturer account created: admin / admin123")
        print("Tables ready.")

    # Fix: debug mode read from environment instead of hardcoded True
    debug_mode = os.getenv("FLASK_ENV", "production") != "production"
    port = int(os.getenv("PORT", 5000))
    app.run(debug=debug_mode, host="0.0.0.0", port=port)