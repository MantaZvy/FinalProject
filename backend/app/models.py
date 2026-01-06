from typing import Optional
from datetime import date, datetime
import uuid

from sqlalchemy import ARRAY, Date, DateTime, Double, ForeignKeyConstraint, PrimaryKeyConstraint, String, Text, Uuid, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class JobDescriptions(Base):
    __tablename__ = 'job_descriptions'
    __table_args__ = (
        PrimaryKeyConstraint('job_id', name='job_descriptions_pkey'),
    )

    job_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('uuid_generate_v4()'))
    title: Mapped[Optional[str]] = mapped_column(Text)
    company: Mapped[Optional[str]] = mapped_column(Text)
    description: Mapped[Optional[str]] = mapped_column(Text)
    skills_required: Mapped[Optional[list[str]]] = mapped_column(ARRAY(Text()))
    keywords: Mapped[Optional[list[str]]] = mapped_column(ARRAY(Text()))
    source: Mapped[Optional[str]] = mapped_column(String(50))
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=text("now()"))
    applications: Mapped[list['Applications']] = relationship('Applications', back_populates='job')
    match_scores: Mapped[list['MatchScores']] = relationship('MatchScores', back_populates='job')


class JobSeeker(Base):
    __tablename__ = 'job_seeker'
    __table_args__ = (
        PrimaryKeyConstraint('user_id', name='job_seeker_pkey'),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('uuid_generate_v4()'))
    profile_summary: Mapped[Optional[str]] = mapped_column(Text)
    skills: Mapped[Optional[list[str]]] = mapped_column(ARRAY(Text()))
    education: Mapped[Optional[dict]] = mapped_column(JSONB)
    experience: Mapped[Optional[dict]] = mapped_column(JSONB)
    certifications: Mapped[Optional[list[str]]] = mapped_column(ARRAY(Text()))
    keywords: Mapped[Optional[list[str]]] = mapped_column(ARRAY(Text()))
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=text("now()"))

    applications: Mapped[list['Applications']] = relationship('Applications', back_populates='user')
    documents: Mapped[list['Documents']] = relationship('Documents', back_populates='user')
    match_scores: Mapped[list['MatchScores']] = relationship('MatchScores', back_populates='user')


class NlpLogs(Base):
    __tablename__ = 'nlp_logs'
    __table_args__ = (
        PrimaryKeyConstraint('run_id', name='nlp_logs_pkey'),
    )

    run_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('uuid_generate_v4()'))
    model_name: Mapped[Optional[str]] = mapped_column(Text)
    bleu_score: Mapped[Optional[float]] = mapped_column(Double(53))
    perplexity: Mapped[Optional[float]] = mapped_column(Double(53))
    accuracy: Mapped[Optional[float]] = mapped_column(Double(53))
    notes: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=text("now()"))


class Applications(Base):
    __tablename__ = 'applications'
    __table_args__ = (
        ForeignKeyConstraint(['job_id'], ['job_descriptions.job_id'], name='applications_job_id_fkey'),
        ForeignKeyConstraint(['user_id'], ['job_seeker.user_id'], ondelete='CASCADE', name='applications_user_id_fkey'),
        PrimaryKeyConstraint('application_id', name='applications_pkey')
    )

    application_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('uuid_generate_v4()'))
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    job_title: Mapped[Optional[str]] = mapped_column(Text)
    company: Mapped[Optional[str]] = mapped_column(Text)
    job_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    platform: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[Optional[str]] = mapped_column(String(50))
    salary_range: Mapped[Optional[str]] = mapped_column(Text)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    applied_date: Mapped[Optional[date]] = mapped_column(Date)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=text("now()"))
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=text("now()"))

    job: Mapped[Optional['JobDescriptions']] = relationship('JobDescriptions', back_populates='applications')
    user: Mapped[Optional['JobSeeker']] = relationship('JobSeeker', back_populates='applications')
    calendar_events: Mapped[list['CalendarEvents']] = relationship('CalendarEvents', back_populates='application')
    email_events: Mapped[list['EmailEvents']] = relationship('EmailEvents', back_populates='application')
    match_scores: Mapped[list['MatchScores']] = relationship('MatchScores', back_populates='application')


class Documents(Base):
    __tablename__ = 'documents'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['job_seeker.user_id'], ondelete='CASCADE', name='documents_user_id_fkey'),
        PrimaryKeyConstraint('document_id', name='documents_pkey')
    )

    document_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('uuid_generate_v4()'))
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    doc_type: Mapped[Optional[str]] = mapped_column(String(50))
    content: Mapped[Optional[str]] = mapped_column(Text)
    file_path: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=text("now()"))

    user: Mapped[Optional['JobSeeker']] = relationship('JobSeeker', back_populates='documents')


class CalendarEvents(Base):
    __tablename__ = 'calendar_events'
    __table_args__ = (
        ForeignKeyConstraint(['application_id'], ['applications.application_id'], ondelete='CASCADE', name='calendar_events_application_id_fkey'),
        PrimaryKeyConstraint('event_id', name='calendar_events_pkey')
    )

    event_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('uuid_generate_v4()'))
    application_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    event_title: Mapped[Optional[str]] = mapped_column(Text)
    event_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=text("now()"))
    google_event_id: Mapped[Optional[str]] = mapped_column(Text)

    application: Mapped[Optional['Applications']] = relationship('Applications', back_populates='calendar_events')


class EmailEvents(Base):
    __tablename__ = 'email_events'
    __table_args__ = (
        ForeignKeyConstraint(['application_id'], ['applications.application_id'], ondelete='CASCADE', name='email_events_application_id_fkey'),
        PrimaryKeyConstraint('email_id', name='email_events_pkey')
    )

    email_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('uuid_generate_v4()'))
    application_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    sender: Mapped[Optional[str]] = mapped_column(Text)
    subject: Mapped[Optional[str]] = mapped_column(Text)
    snippet: Mapped[Optional[str]] = mapped_column(Text)
    detected_status: Mapped[Optional[str]] = mapped_column(String(50))
    received_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    processed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=text("now()"))

    application: Mapped[Optional['Applications']] = relationship('Applications', back_populates='email_events')


class MatchScores(Base):
    __tablename__ = 'match_scores'
    __table_args__ = (
        ForeignKeyConstraint(['application_id'], ['applications.application_id'], ondelete='CASCADE', name='match_scores_application_id_fkey'),
        ForeignKeyConstraint(['job_id'], ['job_descriptions.job_id'], ondelete='SET NULL', name='match_scores_job_id_fkey'),
        ForeignKeyConstraint(['user_id'], ['job_seeker.user_id'], ondelete='CASCADE', name='match_scores_user_id_fkey'),
        PrimaryKeyConstraint('score_id', name='match_scores_pkey')
    )

    score_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('uuid_generate_v4()'))
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    application_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    job_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    similarity_score: Mapped[Optional[float]] = mapped_column(Double(53))
    regression_prediction: Mapped[Optional[float]] = mapped_column(Double(53))
    model_used: Mapped[Optional[str]] = mapped_column(String(100))
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=text("now()"))

    application: Mapped[Optional['Applications']] = relationship('Applications', back_populates='match_scores')
    job: Mapped[Optional['JobDescriptions']] = relationship('JobDescriptions', back_populates='match_scores')
    user: Mapped[Optional['JobSeeker']] = relationship('JobSeeker', back_populates='match_scores')

