![Alt text](public/ICO.png)

# 🚀 JobSon API

## 🌟 Project Overview

The JobSon API is a digital assistant 🤖 designed to automate the aggregation of job listings using SerpApi, offering a sleek RESTful interface to access and manage job data with ease. It stands out for:

- 🔄 Scheduled fetching of job listings.
- 🌐 RESTful API to access job data.
- 🔧 Scalable and maintainable architecture perfect for aggregation tasks.

## 🛠 How It Works

Leveraging a stack of powerful tools and frameworks, the JobSon API offers seamless job listings:

- **Flask**: A nimble web framework for crafting RESTful endpoints.
- **SQLAlchemy**: A robust SQL toolkit and ORM.
- **PostgreSQL**: The trusted open-source relational database.
- **APScheduler**: For timely automated tasks.
- **SerpApi**: Harnessing the power of search engines for job data.
- **Docker**: Ensuring consistent deployment environments.

## 🔧 Installation and Setup

Ensure Docker and Docker Compose are on board before diving in:

1. Clone the repository like a boss:

   ```BASH
   git clone <repository_url>
   ```

2. Step into the JobSon's universe:

   ```BASH
   cd JobSon
   ```

3. Whisper your secrets into a `.env`:

   ```BASH
   API_KEY=<your_serpapi_key>
   DATABASE_URI=postgresql://username:password@jobson-db:5432/jobson
   ```

4. Let Docker Compose weave its magic:

   ```BASH
   docker-compose up --build
   ```

5. The gateway to job wonders now awaits at: `http://localhost:3500`.

## 🎯 Usage Examples

How to wield the power of JobSon API:

### Get a Warm Hello

A simple `GET` to welcome you aboard:

```BASH
curl <http://localhost:3500>
```

### Manually Unleash the Job Fetcher

Invoking the data fetch tsunami with a `POST`:

```BASH
curl -X POST <http://localhost:3500/jobs/trigger-fetch>
```

### Behold All Job Listings

Imagine a Flask route showering you with jobs:

**Coming soon to a codebase near you!**

## 👨‍💻 Contribution Guidelines

Join the fray and contribute:

1. **Coding Stylishly**: Adhere to the PEP 8 style guide.
2. **PRs Like a Pro**: `development` is your go-to branch for PRs. 🎁
3. **Issues and Bugs**: Point them out on GitHub.
4. **Reach Out**: Major ideas? Collaborations? Hit up the maintainers!

Shine on, you crazy diamond, and may your code contributions be ever fruitful!
