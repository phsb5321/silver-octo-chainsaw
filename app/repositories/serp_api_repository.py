# app/repositories/serp_api_repository.py
"""Repository module for fetching data from Serp API."""

from typing import List, Optional

import requests

from ..config import Config
from ..database.models import Job


class SerpApiRepository:
    """A repository for fetching and processing job data from Serp API."""

    def __init__(
        self,
        api_key: str,
        base_url: str = Config.BASE_URL,
    ):
        """
        Initializes the SerpApiRepository with necessary configuration.
        """
        self.api_key = api_key
        self.base_url = base_url

    def fetch_job_data(self, query: str, location: str) -> Optional[dict]:
        """Fetches job data from the API for a given query and location."""
        params = {
            "engine": "google_jobs",
            "q": query,
            "location": location,
            "api_key": self.api_key,
        }
        response = requests.get(self.base_url, params=params)
        if response.ok:
            return response.json()
        return None

    @staticmethod
    def extract_job_info(job: dict) -> Job:
        """Extracts and returns relevant information from a job posting as a Job model instance."""
        extensions = job.get("detected_extensions", {})
        job_info = {
            "job_title": job.get("title", ""),
            "company_name": job.get("company_name", ""),
            "location": job.get("location", "").strip(),
            "description": job.get("description", ""),
            "date_posted": extensions.get("posted_at", ""),
            "job_type": extensions.get("schedule_type", ""),
            "salary": extensions.get("salary", ""),
            "benefits": ", ".join(job.get("extensions", [])),
            "application_link": job.get("apply_link", {}).get("link", ""),
            "related_links": ", ".join(
                link.get("link", "") for link in job.get("related_links", [])
            ),
            "job_id": job.get("job_id", ""),
        }
        return Job(**job_info)

    def process_job_data(self, query: str, location: str) -> List[Job]:
        """Processes job data by fetching and converting to Job model instances."""
        job_data = self.fetch_job_data(query, location)
        if not job_data or "jobs_results" not in job_data:
            raise ValueError("No data or invalid API key")

        job_listings = [self.extract_job_info(job) for job in job_data["jobs_results"]]

        return job_listings
