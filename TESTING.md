# Testing and Debugging Evidence

## Firefighter Safety Data Hub

This document summarizes the testing performed on the **Firefighter Data Hub**. The goal of testing was to confirm that the main firefighter, researcher, database, and authentication workflows operate together correctly.

---

## 1. Final Clean-Package Run Verification


| Test | Command / Check | Expected Result | Result |
| --- | --- | --- | --- |
| Container build and startup | `docker compose up --build` | Backend and researcher dashboard start successfully | **PASS** |
| Backend health endpoint | `http://localhost:8000/api/v1/health` | Returns `{"status":"ok"}` | **PASS** |
| API documentation | `http://localhost:8000/docs` | FastAPI Swagger documentation loads | **PASS** |
| Researcher dashboard | `http://localhost:5173` | React dashboard loads in browser | **PASS** |
| Flutter dependency restore | `flutter pub get` | Flutter dependencies resolve successfully | **PASS** |
| Flutter web startup | `flutter run -d chrome` | Firefighter application opens in Chrome and connects to local backend | **PASS** |

---

## 2. Backend and Database Validation

The backend was checked independently in addition to the full application startup.

| Check | Purpose | Result |
| --- | --- | --- |
| Python source compilation | Detect syntax/import-time source errors in backend application and migration files | **PASS** |
| SQLite integrity check | Confirm submitted local database is structurally valid | **PASS** |
| Existing database migration revision | Confirm database matches the latest expected schema | **PASS** |
| Fresh Alembic migration | Create a new empty SQLite database from the submitted migration history | **PASS** |
| Fresh schema creation | Confirm all required application tables are created | **PASS** |

---

## 3. Automated Frontend Validation

### React researcher dashboard

During the local-first refactor, the React application was checked using:

```bash
npm ci
npm run lint
npm run build
```

Results:

- Dependency installation: **PASS**
- Production build: **PASS**
- Linting: **PASS**, with non-blocking compiler/style warnings noted during development
- Dependency vulnerability check: **0 reported vulnerabilities** during the refactor validation

The Docker startup path also performs a clean `npm ci` inside the web container, which provides an additional clean-dependency check whenever the instructor runs:

```bash
docker compose up --build
```

### Flutter firefighter application

The Flutter project contains three widget tests in `test/widget_test.dart`:

1. A logged-out user is shown the `LoginPage`.
2. A first-time user is shown the `UserConsentPage`.
3. `MainNavigation` renders successfully when opened directly.

The validation commands are:

```bash
flutter analyze --no-fatal-infos --no-fatal-warnings
flutter test
```

During the local-first refactor:

- All three Flutter widget tests: **PASS**
- Flutter web production build: **PASS**
- Flutter analyzer: **No analyzer errors**; only legacy style/deprecation notices remained

The final clean package was additionally launched successfully with:

```bash
flutter run -d chrome
```

---

## 4. Functional Integration Testing

The application was tested as an integrated system rather than only as isolated screens. The most important workflows are listed below.

| Feature / Workflow | Test Performed | Expected Result | Result |
| --- | --- | --- | --- |
| Firefighter registration | Submit a new account and profile | User and profile are created | **PASS** |
| Email verification | Register locally and use the verification token printed by the backend | Account becomes verified | **PASS** |
| Login | Log in with a verified account | Authentication token is returned and stored | **PASS** |
| Unverified-login guard | Attempt login before verification | Login is blocked | **PASS** |
| Fire-event logging | Submit event date, address, context, and PPE-change information | Event is stored by backend | **PASS** |
| PPE tracking | Submit firefighter equipment information | PPE record is stored | **PASS** |
| Smoke sampler | Submit one submission containing multiple sample rows | Parent submission and all sample rows are stored | **PASS** |
| Location synchronization | Capture/save a location and synchronize it | Backend stores location and history can be retrieved | **PASS** |
| Researcher registration/login | Create and authenticate a researcher | Researcher dashboard access succeeds | **PASS** |
| Researcher dashboard | Open dashboard and data tables | Structured application data is displayed | **PASS** |
| Data export | Request researcher CSV-oriented data | Export response is generated successfully | **PASS** |
| Account deletion | Delete an account after related records exist | Dependent data is cleaned and account is removed | **PASS** |

These checks exercise the main path through the system:

```text
Flutter firefighter interface
        ↓
FastAPI REST API
        ↓
Local SQLite persistence
        ↓
React researcher dashboard
```

---

## 5. Important Bugs Found and Fixed

The following are representative examples that were fixed during development and local preparation.

| Problem | Cause | Fix | Verification |
| --- | --- | --- | --- |
| Authentication failed after an earlier successful request | The client could retain an outdated access token after the backend returned a replacement | Centralized token handling so new tokens are captured and stored | Multiple protected operations worked in one authenticated session |
| Frontend attempted an authentication route not provided by the backend | Frontend and backend API contracts were inconsistent | Removed/aligned the unsupported refresh behavior | Login and subsequent authenticated requests completed correctly |
| New users could be treated as already verified | Registration/default verification state was inconsistent | Corrected registration/database verification defaults | New accounts require the local verification token before login |
| Smoke sampler failed when multiple chemicals were submitted | Parent/child records were not handled safely as one multi-row operation | Store one submission with multiple sample rows transactionally | Multi-row sampler submission completed successfully |
| Location history could appear empty after synchronization | Local records could be cleared after upload without a reliable server-history fallback | Added/repaired backend history retrieval and frontend fallback behavior | Synchronized location records remained viewable |
| Account deletion failed after the user created data | Related database rows prevented deletion of the parent user | Clean dependent records before deleting the user | Account deletion succeeded after creating application data |
| Delete-account password verification was unreliable | Password verification logic did not consistently validate the supplied password against the stored hash | Corrected backend password verification | Wrong password is rejected; valid password permits deletion |
| Researcher/frontend endpoints were inconsistent during local conversion | Some React pages referenced behavior not aligned with the current backend | Updated the local API/frontend contracts | Researcher registration, login, dashboard, contact/request flows operate locally |

---

## 6. Testing Conclusion

The backend and researcher dashboard start through Docker Compose, the health and API documentation endpoints are accessible, and the Flutter firefighter interface starts in Chrome and communicates with the local backend. 
Database migration and integrity checks also passed.
