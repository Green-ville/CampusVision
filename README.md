# 👁️ CampusVision
### Facial Recognition Student Attendance System

Python · Flask · OpenCV · dlib · PostgreSQL · Docker

---

## Project Structure

```
campus-vision/
├── run.py                        # ← START HERE: launches the app
├── .env                          # environment variables
├── requirements.txt              # pip dependencies
├── Dockerfile
├── docker-compose.yml
├── app/
│   ├── __init__.py               # Flask app factory
│   ├── models.py                 # Database models (Student, Course, AttendanceRecord)
│   ├── routes/
│   │   ├── main.py               # Serves frontend (/)
│   │   ├── students.py           # /api/students
│   │   ├── attendance.py         # /api/attendance
│   │   ├── recognition.py        # /api/recognition
│   │   └── reports.py            # /api/reports
│   ├── utils/
│   │   └── face_engine.py        # Face encoding & recognition engine
│   ├── templates/
│   │   └── index.html            # Frontend UI
│   └── static/
│       └── uploads/              # Student photos stored here
└── scripts/
    ├── seed_db.py                # Populate DB with sample data
    └── live_capture.py           # Standalone webcam script
```

---

## Option A — Run with Docker (Recommended)

```bash
docker-compose up --build
```
Open http://localhost:5000

---

## Option B — Run Locally

### 1. Install dependencies
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

pip install cmake
pip install -r requirements.txt
```

### 2. Set up PostgreSQL
Create a database named `campusvision_db` and update `.env` with your credentials.

### 3. Run database migrations
```bash
flask db init
flask db migrate -m "initial"
flask db upgrade
```

### 4. Seed sample data (optional)
```bash
python scripts/seed_db.py
```

### 5. Start the app
```bash
python run.py
```
Open http://localhost:5000

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/students/` | List all students |
| POST | `/api/students/register` | Register new student + face |
| POST | `/api/recognition/scan` | Recognize face in image |
| GET | `/api/attendance/today` | Today's attendance summary |
| POST | `/api/attendance/mark` | Manually mark attendance |
| GET | `/api/reports/summary` | Overall KPIs |
| GET | `/api/reports/by-course` | Per-course stats |
| GET | `/api/reports/by-student` | Per-student breakdown |

---

## Live Webcam Script
```bash
python scripts/live_capture.py --course CS301 --url http://localhost:5000
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `dlib` won't install | Run `pip install cmake` first |
| Database connection error | Check `.env` DATABASE_URL matches your PostgreSQL setup |
| No face detected | Use a clear, well-lit frontal photo |
| Port 5000 in use | Change port in `run.py` and `docker-compose.yml` |
