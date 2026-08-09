# AI-Use Log

## Firefighter Safety Data Hub

I used **ChatGPT** and **OpenAI Codex** as coding assistants while developing, debugging, refactoring, testing, and documenting this project. I reviewed the suggested changes and tested the affected workflows before keeping them in the final application.

**Prompt note:** I have selected these prompts from the project conversations. Very long prompts have been shortened and minor spelling and grammar have been cleaned up. I tried to keep the original technical request in the prompts as it is.

## AI Tools Used

- **ChatGPT:** planning, FastAPI/API development guidance, database/migration guidance, Flutter integration, authentication, debugging, testing, cleanup, and documentation.
- **OpenAI Codex:** repository analysis, local-first refactoring, Docker setup, dependency/configuration fixes, cleanup planning, and verification.

## Selected Prompt Log

| # | Tool / Stage | Selected prompt or task | AI contribution | My verification |
|---|---|---|---|---|
| 1 | ChatGPT — Planning | **“Help me understand the Firefighter Safety Data Hub requirements and organize the implementation. I need the backend structure, database models, authentication, firefighter data-entry APIs, Flutter integration, and researcher-facing data access organized step by step.”** | Helped divide the application into FastAPI routers, request/response models, SQLAlchemy models, migration files, authentication utilities, and frontend services. | I compared the structure with the project requirements and implemented the pieces one by one. |
| 2 | ChatGPT — Backend/API | **“I want schemas/storage for `/api/v1/data-transfer/ppe`, `/api/v1/data-transfer/logevent`, and `/api/v1/smokeSampler/`. Give me the code and explain the changes step by step.”** | Helped connect request DTOs, API endpoints, database models, and persistence for fire events, PPE, and smoke-sampler data. | I submitted test records and confirmed that the backend stored and returned the expected information. |
| 3 | ChatGPT — Integration debugging | **“Flutter is calling `/api/v1/auth/refresh` and getting a 404. Help me find the mismatch between the frontend authentication flow and the backend and fix it.”** | Helped trace the frontend/backend contract mismatch and make authentication-response handling consistent. | I repeated authenticated requests and confirmed that the workflow is no longer failed because of the missing or mismatched request. |
| 4 | ChatGPT — Verification debugging | **“For a new signup it should be `is_email_verified = false` and `email_verified_at = null`. Mine is becoming true. Help me find what is wrong in the registration logic or database defaults.”** | Helped inspect the registration path and verification state so a new account must be verified before normal login. | I registered fresh test accounts and checked the state before and after verification. |
| 5 | ChatGPT — Account management | **“This is my `auth.py`. Tell me what I need to change for fixing delete-account password verification.”** | Reviewed the deletion flow and helped correct password verification before account removal. | I tested incorrect and correct passwords and confirmed deletion only proceeded after valid verification. |
| 6 | ChatGPT — Database/debugging | **“I need to delete a test user and the user’s related data as well. Help me make sure account deletion does not fail when profile, event, PPE, sampler, or location records already exist.”** | Helped identify dependent rows and the safe cleanup order before deleting the user. | I created dependent test data and confirmed the complete account deletion workflow succeeded. |
| 7 | ChatGPT — Authentication debugging | **“One authenticated submission works, but later protected requests fail. Help me find why the token becomes stale and make the Flutter app keep the latest token returned by the backend.”** | Helped centralize token handling so updated access tokens were stored and reused by later modules. | I performed several protected operations in the same session and confirmed that later requests should continued to authenticate. |
| 8 | ChatGPT — Smoke-sampler debugging | **“A smoke-sampler submission can contain multiple chemical samples. The single-row case works, but multiple rows fail. Help me fix the backend so one submission can save all samples correctly.”** | Helped model the operation as one parent submission with multiple child rows and transactional insert/rollback behavior. | I tested both one-sample and multi-sample submissions and confirmed all expected rows were created together. |
| 9 | ChatGPT — Location debugging | **“Location upload succeeds, but history can appear empty after the local records are synchronized. Help me make the app retrieve and display the latest saved location records correctly.”** | Helped separate local buffering from stored history and use a latest-history retrieval path after synchronization. | I captured, synchronized, and opened location history to confirm saved records remained visible. |
| 10 | Codex — Repository audit | **“Analyze this entire project folder, but do not modify, move, or delete anything yet. Explain the project structure, identify what is required to run, categorize files as KEEP / KEEP FOR SUBMISSION / OPTIONAL / REMOVE, identify sensitive information, and give me the cleanup plan first.”** | I checked the repository and separated source code from environments, caches, build output, duplicates, machine-specific files, and sensitive material. It also flagged uncertain files that should not be deleted blindly. | I reviewed the proposed categories before allowing cleanup and retained files required by imports, migrations, and Flutter platform builds. |
| 11 | Codex — Local-first refactor | **“Make this app run locally so that anyone can build it on their local system and test-run it.”** | Changed the normal evaluation path to SQLite, local file storage, console verification messages, local API addressing, and Docker Compose for the backend and researcher dashboard. It also repaired configuration needed for clean local builds. | I followed the resulting local setup and confirmed that the application could run without manually configuring multiple external services. |
| 12 | ChatGPT — Final cleanup/testing | **“Remove the files that are not required, but make sure not to remove anything needed for app functionality. Preserve the local database. Then build and run the final app using the same Docker and Flutter commands the professor will use.”** | Performed conservative cleanup, retained source/migrations/lock files/platform scaffolding/local data, removed generated or private artifacts, checked application configuration, and prepared the professor-facing README. | I extracted the cleaned project into a fresh location and successfully ran the exact documented Docker and Flutter workflow. |

## Examples of AI-Assisted Debugging

The most useful AI assistance came from issues that crossed more than one part of the application. Examples included:

- frontend authentication requests not matching backend routes;
- successful writes being interpreted incorrectly by the Flutter service;
- incorrect verification state for new accounts;
- stale authentication tokens causing later requests to fail;
- multi-row smoke-sampler inserts failing even when a single sample worked;
- location history appearing empty after synchronization;
- account deletion failing because related records existed; and
- account deletion needing correct password verification.

For these issues, I used AI to narrow the likely cause and propose changes, then I again executed the actual workflow before accepting the fix.

## Final Verification

The final local project was tested from a clean copy using the same commands that are provided to the instructor.

### Backend + Researcher Dashboard

```bash
docker compose up --build
```

Checked:

- Researcher dashboard: `http://localhost:5173`
- Backend health: `http://localhost:8000/api/v1/health`
- FastAPI documentation: `http://localhost:8000/docs`

### Flutter Firefighter Application

```bash
cd Frontend/mobile_app/firefighter_safety_data_hub
flutter pub get
flutter run -d chrome
```

## My Responsibility

AI was used as an assistant rather than as a substitute for understanding the code. My workflow was to provide the requirement and error. I reviewed the proposed change, applied only changes that matched the codebase. Then, I re ran the affected feature, and kept the change only after it worked as expected.
