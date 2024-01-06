# app/models.py
from sqlalchemy import Column, Integer, String

from .database_manager import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String, index=True)
    company_name = Column(String, index=True)
    location = Column(String)
    description = Column(String)
    date_posted = Column(String)
    job_type = Column(String)
    salary = Column(String)
    benefits = Column(String)
    application_link = Column(String)
    related_links = Column(String)
    job_id = Column(String, unique=True)

    def __str__(self):
        return self.job_title

    def serialize(self):
        return {
            "id": self.id,
            "job_title": self.job_title,
            "company_name": self.company_name,
            "location": self.location,
            "description": self.description,
            "date_posted": self.date_posted,
            "job_type": self.job_type,
            "salary": self.salary,
            "benefits": self.benefits,
            "application_link": self.application_link,
            "related_links": self.related_links,
            "job_id": self.job_id,
        }
