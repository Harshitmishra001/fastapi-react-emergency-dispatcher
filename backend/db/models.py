from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime, timezone

from backend.config.settings import settings

Base = declarative_base()

class DBReport(Base):
    __tablename__ = "reports"
    report_id = Column(String, primary_key=True, index=True)
    source_channel = Column(String, index=True)
    raw_text = Column(String)
    submitted_at = Column(DateTime)
    reporter_contact = Column(String, nullable=True) # Should be encrypted at rest in prod

class DBVerifiedNeed(Base):
    __tablename__ = "verified_needs"
    need_id = Column(String, primary_key=True, index=True)
    source_report_ids = Column(String) # JSON or comma-separated
    location_text = Column(String)
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)
    need_type = Column(String, index=True)
    quantity_estimate = Column(Integer)
    urgency = Column(String)
    verification_confidence = Column(Float)
    requires_human_review = Column(Boolean, default=False)
    duplicate_of = Column(String, nullable=True)

class DBResource(Base):
    __tablename__ = "resources"
    resource_id = Column(String, primary_key=True, index=True)
    resource_type = Column(String, index=True)
    quantity_available = Column(Integer)
    lat = Column(Float)
    lon = Column(Float)
    status = Column(String) # "available", "reserved", "dispatched"

class DBAllocation(Base):
    __tablename__ = "allocations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    plan_id = Column(String, index=True)
    need_id = Column(String, ForeignKey("verified_needs.need_id"))
    resource_id = Column(String, ForeignKey("resources.resource_id"))
    quantity_allocated = Column(Integer)
    distance_km = Column(Float)
    allocation_method = Column(String)

class DBDispatchPlan(Base):
    __tablename__ = "dispatch_plans"
    plan_id = Column(String, primary_key=True, index=True)
    generated_at = Column(DateTime)
    narrative = Column(String)
    coverage_pct = Column(Float, nullable=True)
    critical_unmet_count = Column(Integer, nullable=True)
    fairness_score = Column(Float, nullable=True)
    passed = Column(Boolean, default=False)
    rationale = Column(String, nullable=True)

# We use the main database URL for simplicity in dev, though the spec
# mentions privilege separation between ingestion and dispatch.
# In a real deployed setup, we would configure separate engines with separate roles.
engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
