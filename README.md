# Short messages service API backend

## Introduction
API backend is developed with FastAPI framework on Python 3.11.

Postgresql is used to store data. Alembic is used to create and support database structure. SqlAlchemy 2.0 is used to provide CRUD operations for data stored in database.

Source code is covered by unit tests, which are developed using pytest.

Docker and Docker Compose are used for the API backend deployment. 

## Deployment

### 1. Common information
There are 2 different deployment environments inside this repo configured with docker compose.

Each environment contains 3 separate servces:
* DB Service is launched on the standard postgresql port 5432. Standard postgresql image is used.
* API service is launched on the port 5000. API documentation can be accessible by address `http://localhost:5000/docs`.
* Nginx service is launched on the port 80 and used to process static files (VueJS web application). Web application can be accessible by address `http://localhost`.

#### 1. Presentation environment (file _docker-compose_test.yml_)
This environment contains tools to test and launch API backend and also check source code with linters.

Also this environment can be used to present API service with some test data:
1. Open running container
2. Open terminal for the API service docker container
3. Run command `python fixtures.py` to generate test data in the database.

#### 2. Production environment (file _docker-compose.yml_)
This environment contains tools and file to launch app only.

### 2. How to deploy an API backend
1. Clone this repo.
2. Rename _.envexample_ file to _.env_.
3. Copy _.env_ file to _environment\test_ и _environment\prod_ folders.
4. Edit both file with actual data to configure presentation and production environment
5. Launch docker compose command:
   
   5.1. **Presentation environment**
   `docker compose -p tweets_test -f docker-compose_test.yml up -d --build`
   
   5.2 **Production environment**
   `docker compose -p tweets -f docker-compose.yml up -d --build`
