# Firefighter Safety Data Hub

A full-stack application for collecting, organizing, and reviewing firefighter exposure-related information.

The project provides a **Flutter application for firefighter data entry**, a **FastAPI backend**, and a **React researcher dashboard**. The submission version is designed to run locally with minimal setup using **Docker Compose, SQLite, and local storage**. No AWS account or cloud credentials are required.

## Public Demo

The hosted demo exposes **both application interfaces from the same Render service**:

- **Flutter firefighter app:** <https://firefighter-safety-data-hub-demo.onrender.com/firefighter/>
- **React researcher dashboard:** <https://firefighter-safety-data-hub-demo.onrender.com/>
- **FastAPI documentation:** <https://firefighter-safety-data-hub-demo.onrender.com/docs>

**Demo firefighter account:**

```text
Email: demo.firefighter1@example.com
Password: DemoFirefighter123!
```

**Demo researcher account:**

```text
Email: demo.researcher@example.com
Password: DemoResearch123!
```
**Note: I am using Render's Free instance, it will automatically spin down after about 15 minutes without traffic and wake back up when someone visits the URL. The first visit after sleeping can therefore take around a minute.**

---

## 1. Project Purpose

Firefighters may need to record information from fire events, personal protective equipment (PPE), passive smoke samplers, and location history. When these records are kept in separate forms, notes, or spreadsheets, it becomes difficult to connect the information and prepare it for later review or research.

The **Firefighter Safety Data Hub** provides one structured system for this workflow. Firefighters can enter exposure-related information through the Flutter application, the FastAPI backend validates and stores the records, and researchers can review or export structured data through the React dashboard.

The current project is a proof-of-concept intended for software demonstration and research-oriented data collection.

---

## 2. Main Features

### Firefighter application

- **Account registration, verification, and login**
- **Fire event logging** with date, address, event context, and PPE-related information
- **PPE tracking** for firefighter equipment records
- **Smoke sampler data entry**, including multiple chemical samples in one submission
- **Location history capture and synchronization**
- **Password management, consent, privacy, and account-deletion workflows**

### Researcher dashboard

- **Researcher registration and authentication**
- **Dashboard summaries** of collected data
- **Firefighter/user data review**
- **Fire event, PPE, and smoke-sampler tables**
- **CSV export** for supported datasets
- **Researcher account and password-management workflows**

### Backend

- REST APIs built with **FastAPI**
- Request validation with **Pydantic**
- Data persistence with **SQLAlchemy** and **SQLite**
- Database schema management with **Alembic**
- Token-based authentication and password hashing
- Local console-based verification messages for evaluation
- Local file storage for the default setup
- Interactive API documentation through FastAPI/OpenAPI

---

## 3. Technology Stack

| Layer | Technology |
| --- | --- |
| Firefighter client | Flutter / Dart |
| Researcher dashboard | React, TypeScript, Vite |
| Backend API | Python, FastAPI |
| ORM / database access | SQLAlchemy |
| Local database | SQLite |
| Database migrations | Alembic |
| Authentication | JWT-based authentication and password hashing |
| Local application startup | Docker Compose |
| API documentation | FastAPI / OpenAPI / Swagger UI |

### Local evaluation architecture

```text
                   Firefighter
                  Flutter App
                       |
                       | REST API
                       v
              +------------------+
              | FastAPI Backend  |
              +---------+--------+
                        |
                        v
                 SQLite Database
                        ^
                        |
                       REST API
                        |
              +---------+---------+
              | React Researcher  |
              |    Dashboard      |
              +-------------------+
```

Docker Compose starts the **FastAPI backend and React dashboard**. The Flutter application is started separately so it can run in Chrome or another supported Flutter target.

---

## 4. Quick Start

### Prerequisites

Install:

1. **Docker Desktop** (or Docker Engine with Docker Compose)
2. **Flutter SDK with web support**
3. **Google Chrome**

No AWS account, PostgreSQL installation, Node.js installation, Python environment, or cloud credentials are required for the default evaluation setup.

### Step 1 — Start the backend and researcher dashboard

Open a terminal in the project root — the folder containing `compose.yaml` — and run:

```bash
docker compose up --build
```

Wait for the containers to finish starting.

Then open:

- **Researcher dashboard:** <http://localhost:5173>
- **Backend health check:** <http://localhost:8000/api/v1/health>
- **FastAPI API documentation:** <http://localhost:8000/docs>

A successful health check returns:

```json
{"status":"ok"}
```

### Step 2 — Start the Flutter firefighter application

Keep Docker running. Open a **second terminal** from the project root and run:

```bash
cd Frontend/mobile_app/firefighter_safety_data_hub
flutter pub get
flutter run -d chrome
```

The Flutter web application automatically connects to the local backend at:

```text
http://127.0.0.1:8000
```

No `.env` changes or API URL edits are required for the default Chrome setup.

---

## 5. How to Use the Application

### Firefighter workflow

1. Start the Flutter application.
2. Register a firefighter account.
3. Retrieve the verification token from the Docker/backend terminal output.
4. Enter the token in the Flutter verification screen.
5. Log in.
6. Use the application to enter fire-event, PPE, smoke-sampler, or location information.

### Local email verification

For local evaluation, the project uses **console email mode** instead of a real email service.

When an account is registered, the verification message/token is printed in the terminal running:

```bash
docker compose up --build
```

Copy that token and paste it into the Flutter verification screen.

### Researcher workflow

1. Open <http://localhost:5173>.
2. Create or log in to a researcher account.
3. Open the researcher dashboard.
4. Review available firefighter, event, PPE, and smoke-sampler information.
5. Use the available CSV export controls to download supported datasets.

Local researcher password-reset links are also printed to the backend/Docker output instead of being sent through a real email provider.

---

## 6. Project Structure

```text
Firefighter_Safety_Data_Hub/
|
|-- Backend/
|   |-- app/                         FastAPI application
|   |-- alembic/                     Database migrations
|   |-- Dockerfile                   Backend container definition
|   |-- requirements.txt             Python dependencies
|   |-- .env.example                 Safe local configuration example
|   `-- firefighter_local.db         Retained local development database
|
|-- Frontend/
|   |-- mobile_app/
|   |   `-- firefighter_safety_data_hub/   Flutter firefighter application
|   |
|   `-- web_app/
|       `-- fire-fighter-data-exposure-hub/ React researcher dashboard
|
|-- compose.yaml                     Docker startup configuration
|-- README.md                        Project documentation
`-- .gitignore                       Generated/private file exclusions
```

---

## 7. Local Data and Persistence

The Docker setup uses a persistent Docker volume named:

```text
local_app_data
```

The volume stores the Docker-side SQLite database and local uploaded files. Data therefore remains available after stopping and restarting the containers.

The repository also intentionally retains:

```text
Backend/firefighter_local.db
```

This is the local database copy used by the optional native-backend workflow. The standard Docker workflow uses its own persistent volume for easier cross-platform evaluation.

---

## 8. Stop or Reset the Application

To stop the application, press **Ctrl+C** in the Docker terminal and run:

```bash
docker compose down
```

This keeps the Docker data volume.

To intentionally remove local Docker data and start from a fresh database:

```bash
docker compose down --volumes
```

Use `--volumes` only when you want to delete the current local test data.

---

## 9. Optional Testing and Validation

These commands are **not required to run the project**. They are useful for development or source validation.

### React dashboard

```bash
cd Frontend/web_app/fire-fighter-data-exposure-hub
npm ci
npm run lint
npm run build
```

### Flutter application

```bash
cd Frontend/mobile_app/firefighter_safety_data_hub
flutter analyze --no-fatal-infos --no-fatal-warnings
flutter test
```

### Backend health check

After Docker starts:

```text
http://localhost:8000/api/v1/health
```

Expected response:

```json
{"status":"ok"}
```

More detailed testing and debugging evidence will be documented separately in the project submission materials.

---

## 10. Other Flutter Targets

The backend URL is selected automatically for common local targets:

- **Chrome / iOS simulator / macOS / Linux / Windows:** `http://127.0.0.1:8000`
- **Android emulator:** `http://10.0.2.2:8000`

For a physical phone, provide the development computer's LAN address:

```bash
flutter run --dart-define=API_BASE_URL=http://192.168.1.10:8000
```

Replace `192.168.1.10` with the computer's actual LAN IP. The phone and computer must be on the same network, and the computer must allow connections to port `8000`.

---

## 11. Local Configuration

The default evaluation setup uses:

| Setting | Default |
| --- | --- |
| Database | SQLite |
| Email delivery | Console output |
| File storage | Local filesystem |
| Backend port | `8000` |
| Researcher dashboard port | `5173` |
| Cloud credentials | Not required |

Safe local configuration templates are provided using `.env.example` files. Private `.env` files, cloud credentials, machine-specific settings, generated build folders, and signing keys are intentionally excluded from the submission.

---

## 12. AI-Assisted Development

AI coding tools were used as development assistants for planning, implementation guidance, debugging, code review, local-environment refactoring, testing support, and documentation improvement. The final code and workflows were reviewed and tested rather than being accepted without verification.

A separate **AI-use log** in the final submission will summarize the major prompts/tasks performed with ChatGPT and Codex and how the resulting changes were verified.

---

## 13. Submission Items

The final course submission is intended to include:

- Project source code / repository or ZIP
- Runnable public or shareable demo URL
- This `README.md`
- `AI_USE_LOG.md`
- `REFLECTION.md`
- Testing/debugging evidence
