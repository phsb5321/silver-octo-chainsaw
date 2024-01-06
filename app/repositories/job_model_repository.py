# app/job_repository.py
"""Repository module for interacting with the Job data model."""

from contextlib import contextmanager
from typing import List

from psycopg2 import IntegrityError

from ..database.database_manager import Base, SessionLocal, engine
from ..database.models import Job

# Ensure db tables are created
Base.metadata.create_all(bind=engine)


@contextmanager
def get_session():
    """Provide a transactional scope around a series of operations."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


class JobRepository:
    """A repository for interfacing with the jobs database."""

    @staticmethod
    def add_job(job: Job) -> None:
        """
        Adds a job record to the database.

        :param job: A Job object containing job information.
        """
        with get_session() as db_session:
            db_session.add(job)

    @staticmethod
    def get_job_by_id(job_id: str) -> Job:
        """
        Retrieves a job from the database by its job_id.

        :param job_id: The job ID to search for in the database.
        :returns: The Job object if found, otherwise None.
        """
        with get_session() as db_session:
            return db_session.query(Job).filter_by(job_id=job_id).first()

    @staticmethod
    def add_jobs(jobs: List[Job], session=None) -> None:
        """
        Adds multiple job records to the database. Skips the jobs that
        are already in the database (based on job_id).

        :param jobs: A list of Job objects.
        :param session: Optional database session for testability.
        """
        if session is None:
            session = SessionLocal()  # Create a new session if one wasn't provided

        try:
            for job in jobs:
                if not session.query(Job).filter_by(job_id=job.job_id).first():
                    session.add(job)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            # In production, log the error for further assessment.
            print(f"An IntegrityError occurred: {e}")
        finally:
            session.close()

    @staticmethod
    def get_all_jobs() -> List[Job]:
        """
        Retrieves all jobs from the database.

        :returns: A list of Job objects.
        """
        with get_session() as db_session:
            return db_session.query(Job).all()

    @staticmethod
    def delete_all_jobs() -> None:
        """Deletes all jobs from the database."""
        with get_session() as db_session:
            db_session.query(Job).delete()

    @staticmethod
    def delete_job_by_id(job_id: str) -> None:
        """
        Deletes a job from the database by its job_id.

        :param job_id: The job ID to search for in the database.
        """
        with get_session() as db_session:
            db_session.query(Job).filter_by(job_id=job_id).delete()

    @staticmethod
    def update_job(job_id: str, job_data: dict) -> None:
        """
        Updates a job in the database by its job_id.

        :param job_id: The job ID to search for in the database.
        :param job_data: A dictionary containing new job information.
        """
        with get_session() as db_session:
            job = db_session.query(Job).filter_by(job_id=job_id).first()
            for key, value in job_data.items():
                setattr(job, key, value)
