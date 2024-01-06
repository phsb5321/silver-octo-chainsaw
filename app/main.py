# app/main.py
"""Main application script."""

import atexit
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_restx import Api, Resource

from app.config import Config
from app.repositories.job_model_repository import JobRepository
from app.repositories.serp_api_repository import SerpApiRepository

app = Flask(__name__)
api = Api(app, version="1.0", title="JobSon API", description="A simple Job API")

ns = api.namespace("jobs", description="Job operations")


# Function to fetch and store job data
def fetch_and_store_job_data():
    """Function to fetch and store job data."""
    # Instantiate the repository
    serp_repository = SerpApiRepository(api_key=Config.API_KEY)
    # Example search parameters
    search_query = "Software Engineer"
    search_location = "San Francisco, CA"
    # Fetch and process job data
    job_listings = serp_repository.process_job_data(search_query, search_location)
    # Instantiate the job repository and save job listings
    job_repo = JobRepository()
    job_repo.add_jobs(job_listings)
    print(f"Job data fetched and stored successfully at {datetime.now()}")


scheduler = BackgroundScheduler()
scheduler.add_job(fetch_and_store_job_data, "cron", hour=0, minute=0, day="*/2")
scheduler.start()

atexit.register(lambda: scheduler.shutdown())


@ns.route("/")
class HelloWorld(Resource):
    def get(self):
        """Return a greeting"""
        return {"message": "The JobSon service is up and running!"}


@ns.route("/trigger-fetch")
class TriggerFetch(Resource):
    def post(self):
        """Manually trigger the fetching and storing of job data"""
        try:
            fetch_and_store_job_data()
            return {"message": "Job data fetch initiated successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3500)
