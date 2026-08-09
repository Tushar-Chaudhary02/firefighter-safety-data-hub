# Public Demo Deployment

The normal evaluator workflow remains local and uses `compose.yaml`. This file describes the optional **public course demo** deployment.

## Recommended host: Render

The repository includes:

- `Dockerfile.render` — builds the React dashboard and FastAPI backend into one web service.
- `render.yaml` — Render Blueprint configuration.
- `Backend/app/scripts/seed_demo.py` — creates synthetic demonstration data only when `DEMO_SEED=true`.

The public demo intentionally uses a temporary SQLite database. The hosting provider may recreate it when the free service restarts, so the startup command runs migrations and recreates synthetic demo data automatically. The local Docker version keeps its normal persistent volume and is unaffected.

## Demo account

After deployment, the dashboard can be opened at the Render URL and logged into with:

```text
Email: demo.researcher@example.com
Password: DemoResearch123!
```

These are demonstration-only credentials for synthetic data and are not used by the local application unless `DEMO_SEED=true` is explicitly enabled.

## Deploy from GitHub/GitLab

1. Push the final project folder to a GitHub or GitLab repository.
2. Sign in to Render.
3. Choose **New > Blueprint**.
4. Connect the repository containing `render.yaml`.
5. Render detects the Blueprint and creates the `firefighter-safety-data-hub-demo` web service.
6. Wait for the build and health check to complete.
7. Open the generated `https://...onrender.com` address.
8. Verify:
   - `/` opens the researcher dashboard.
   - `/api/v1/health` returns `{"status":"ok"}`.
   - `/docs` opens FastAPI documentation.
   - The demo researcher credentials above can log in and display synthetic records.

## Important free-demo behavior

The public demo is for course evaluation, not production use. The free web-service filesystem is ephemeral, so records created by visitors can disappear when the service restarts. The included startup seed recreates the demonstration records after a restart.

The local evaluator package does not have this limitation because `docker compose` stores application data in the `local_app_data` Docker volume.
