"""Seed a small, synthetic dataset for the public course demo.

This script is intentionally idempotent. It only creates the demo records when
DEMO_SEED=true and when the demo researcher does not already exist.
"""
from __future__ import annotations

import os
from datetime import datetime, timezone

from app.core.security import hash_password
from app.db.session import SessionLocal
# Import the complete SQLAlchemy model registry before the first query.
# UserModel contains string-based relationships (for example, "LocationEntry"),
# and standalone scripts do not automatically import every API router/model the
# way the FastAPI application does. Registering all mapped classes here prevents
# SQLAlchemy mapper-resolution errors during demo seeding.
from app.db import base_class  # noqa: F401
from app.models.LogEventModel import LogEventModel
from app.models.PpeModel import PpeModel
from app.models.SmokeSamplerModel import SmokeSamplerSampleModel, SmokeSamplerSubmissionModel
from app.models.locationModel import LocationEntryModel
from app.models.userModel import UserModel
from app.models.userProfileModel import UserProfileModel
from app.models.userResearcherModel import UserResearcherModel

DEMO_RESEARCHER_EMAIL = os.getenv("DEMO_RESEARCHER_EMAIL", "demo.researcher@example.com")
DEMO_RESEARCHER_PASSWORD = os.getenv("DEMO_RESEARCHER_PASSWORD", "DemoResearch123!")


def seed_demo() -> None:
    if os.getenv("DEMO_SEED", "false").lower() not in {"1", "true", "yes", "on"}:
        print("Demo seed disabled; skipping sample data.")
        return

    db = SessionLocal()
    try:
        existing = (
            db.query(UserResearcherModel)
            .filter(UserResearcherModel.university_email == DEMO_RESEARCHER_EMAIL)
            .first()
        )
        if existing:
            print("Demo data already present; skipping seed.")
            return

        researcher = UserResearcherModel(
            first_name="Demo",
            last_name="Researcher",
            university_email=DEMO_RESEARCHER_EMAIL,
            personal_email=None,
            password_hash=hash_password(DEMO_RESEARCHER_PASSWORD),
            phonenumber=None,
            role="researcher",
            is_active=True,
        )
        db.add(researcher)

        firefighter_1 = UserModel(
            email="demo.firefighter1@example.com",
            password_hash=hash_password("DemoFirefighter123!"),
            phoneNumber=None,
            role="firefighter",
            is_email_verified=True,
            email_verified_at=datetime.now(timezone.utc),
        )
        firefighter_2 = UserModel(
            email="demo.firefighter2@example.com",
            password_hash=hash_password("DemoFirefighter123!"),
            phoneNumber=None,
            role="firefighter",
            is_email_verified=True,
            email_verified_at=datetime.now(timezone.utc),
        )
        chief = UserModel(
            email="demo.chief@example.com",
            password_hash=hash_password("DemoChief123!"),
            phoneNumber=None,
            role="chief",
            is_email_verified=True,
            email_verified_at=datetime.now(timezone.utc),
        )
        db.add_all([firefighter_1, firefighter_2, chief])
        db.flush()

        db.add_all(
            [
                UserProfileModel(
                    user_id=firefighter_1.id,
                    full_name="Demo Firefighter One",
                    gender=None,
                    race=None,
                    ethnicity=None,
                    year_of_birth=1990,
                    height_cm=178.0,
                    weight_kg=82.0,
                    dominant_hand="Right",
                    years_of_experience="6",
                    firefighter_status="Active",
                    type_of_firefighter="Career",
                    firefighter_station_name="Demo Station 1",
                    city="Ames",
                    state="Iowa",
                ),
                UserProfileModel(
                    user_id=firefighter_2.id,
                    full_name="Demo Firefighter Two",
                    gender=None,
                    race=None,
                    ethnicity=None,
                    year_of_birth=1988,
                    height_cm=170.0,
                    weight_kg=75.0,
                    dominant_hand="Left",
                    years_of_experience="9",
                    firefighter_status="Active",
                    type_of_firefighter="Career",
                    firefighter_station_name="Demo Station 2",
                    city="Ames",
                    state="Iowa",
                ),
                UserProfileModel(
                    user_id=chief.id,
                    full_name="Demo Fire Chief",
                    gender=None,
                    race=None,
                    ethnicity=None,
                    year_of_birth=1980,
                    height_cm=182.0,
                    weight_kg=88.0,
                    dominant_hand="Right",
                    years_of_experience="18",
                    firefighter_status="Active",
                    type_of_firefighter="Chief",
                    firefighter_station_name="Demo Station 1",
                    city="Ames",
                    state="Iowa",
                ),
            ]
        )

        event_1 = LogEventModel(
            user_id=firefighter_1.id,
            event_date=datetime(2026, 7, 15, 14, 30, tzinfo=timezone.utc),
            event_address="100 Demo Avenue, Ames, IA",
            is_same_ppe=True,
        )
        event_2 = LogEventModel(
            user_id=firefighter_2.id,
            event_date=datetime(2026, 7, 18, 9, 10, tzinfo=timezone.utc),
            event_address="250 Training Road, Ames, IA",
            is_same_ppe=False,
        )
        db.add_all([event_1, event_2])
        db.flush()

        db.add_all(
            [
                PpeModel(
                    user_id=firefighter_1.id,
                    event_id=event_1.event_id,
                    helmet_id="H-1001",
                    hood_id="HD-1001",
                    face_mask_id="FM-1001",
                    scba_id="SCBA-1001",
                    glove_id="G-1001",
                    boot_id="B-1001",
                    bunker_coat_id="BC-1001",
                    bunker_pants_id="BP-1001",
                    is_ppe_updated=False,
                ),
                PpeModel(
                    user_id=firefighter_2.id,
                    event_id=event_2.event_id,
                    helmet_id="H-2001",
                    hood_id="HD-2001",
                    face_mask_id="FM-2001",
                    scba_id="SCBA-2001",
                    glove_id="G-2001",
                    boot_id="B-2001",
                    bunker_coat_id="BC-2001",
                    bunker_pants_id="BP-2001",
                    is_ppe_updated=True,
                ),
            ]
        )

        sampler = SmokeSamplerSubmissionModel(user_id=firefighter_1.id)
        db.add(sampler)
        db.flush()
        db.add_all(
            [
                SmokeSamplerSampleModel(
                    submission_id=sampler.submission_id,
                    chemical_name="Benzene",
                    percentage_proportion=36.5,
                ),
                SmokeSamplerSampleModel(
                    submission_id=sampler.submission_id,
                    chemical_name="Toluene",
                    percentage_proportion=21.0,
                ),
                SmokeSamplerSampleModel(
                    submission_id=sampler.submission_id,
                    chemical_name="Naphthalene",
                    percentage_proportion=12.5,
                ),
            ]
        )

        db.add_all(
            [
                LocationEntryModel(
                    user_id=firefighter_1.id,
                    latitude=42.0308,
                    longitude=-93.6319,
                    locationTimestamp=datetime(2026, 7, 15, 14, 32, tzinfo=timezone.utc),
                    accuracy=6.0,
                    altitude=290.0,
                ),
                LocationEntryModel(
                    user_id=firefighter_2.id,
                    latitude=42.0347,
                    longitude=-93.6200,
                    locationTimestamp=datetime(2026, 7, 18, 9, 14, tzinfo=timezone.utc),
                    accuracy=8.0,
                    altitude=288.0,
                ),
            ]
        )

        db.commit()
        print(f"Seeded public demo data. Researcher login: {DEMO_RESEARCHER_EMAIL}")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_demo()
