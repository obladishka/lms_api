# LMS API Service

A RESTful API service for Learning Management System (LMS) built with DRF and PostgreSQL.

## Features

- User authentication (JWT)
- Course management
- Lesson management
- User management (automatic blocking of inactive users)
- Payment service
- Courses subscription feature (be aware of all updates of a course you're interested at)
- API documentation with Swagger

## Installation

1. Clone the repository:
```commandline
git clone https://github.com/obladishka/lms_api.git
```
2. Set your environment variables:
Fill in '.env.sample' file. Don't forget to rename the file to .env!
3. Start the container:
```commandline
docker-compose up
```
4. Congratulations! The project is set up successfully! To enjoy all the features go to http://localhost:8000/users/register
and create a user account.

## API Documentation

After starting the container, access the API documentation at:

Swagger UI: http://localhost:8000/api/schema/
Redoc UI: http://localhost:8000/api/docs/