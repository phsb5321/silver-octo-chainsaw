# tests/test_serp_api_repository.py
import pytest
import requests_mock

from app.config import Config
from app.database.models import Job
from app.repositories.serp_api_repository import SerpApiRepository

# Test data to mock the API response
mock_job_listing = {
    "title": "Software Developer",
    "company_name": "Tech Co",
    "location": "San Francisco, CA",
    "description": "Job Description",
    "detected_extensions": {
        "posted_at": "1 day ago",
        "schedule_type": "Full-time",
        "salary": "$100,000",
    },
    "extensions": [
        "Health benefits",
        "Retirement plan",
    ],
    "apply_link": {"link": "https://apply.example.com"},
    "related_links": [{"link": "https://detail.example.com"}],
    "job_id": "12345",
}


@pytest.fixture
def serp_api_repo():
    return SerpApiRepository(api_key=Config.API_KEY)


def test_fetch_job_data_successful(serp_api_repo):
    with requests_mock.Mocker() as m:
        query = "Software Engineer"
        location = "San Francisco, CA"
        m.get(Config.BASE_URL, json={"jobs_results": [mock_job_listing]})
        response = serp_api_repo.fetch_job_data(query, location)
        assert response is not None
        assert "jobs_results" in response
        assert response["jobs_results"][0]["title"] == "Software Developer"


def test_fetch_job_data_failure(serp_api_repo):
    with requests_mock.Mocker() as m:
        query = "Software Engineer"
        location = "San Francisco, CA"
        m.get(Config.BASE_URL, status_code=500)
        response = serp_api_repo.fetch_job_data(query, location)
        assert response is None


def test_extract_job_info(serp_api_repo):
    job_info = serp_api_repo.extract_job_info(mock_job_listing)
    assert isinstance(job_info, Job)
    assert job_info.job_title == "Software Developer"
    assert job_info.company_name == "Tech Co"
    assert job_info.location == "San Francisco, CA"


def test_process_job_data_successful(serp_api_repo):
    with requests_mock.Mocker() as m:
        query = "Software Engineer"
        location = "San Francisco, CA"
        m.get(Config.BASE_URL, json={"jobs_results": [mock_job_listing]})
        job_listings = serp_api_repo.process_job_data(query, location)
        assert isinstance(job_listings, list)
        assert len(job_listings) == 1
        assert isinstance(job_listings[0], Job)


def test_process_job_data_with_no_results(serp_api_repo):
    with pytest.raises(ValueError):
        with requests_mock.Mocker() as m:
            query = "Software Engineer"
            location = "San Francisco, CA"
            m.get(Config.BASE_URL, json={"jobs_results": []})
            serp_api_repo.process_job_data(query, location)


def test_process_job_data_api_failure(serp_api_repo):
    with pytest.raises(ValueError):
        with requests_mock.Mocker() as m:
            query = "Software Engineer"
            location = "San Francisco, CA"
            m.get(Config.BASE_URL, status_code=500)
            serp_api_repo.process_job_data(query, location)
