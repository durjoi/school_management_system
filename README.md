# Student Management System

This is a simple web application developed with Flask, which provides basic CRUD (Create, Read, Update, and Delete) operations for managing student records. 

## Capabilities

[x] Authentication & Authorization for Teacher <br>
[x] Teacher CRUD <br>
[x] Subjects CRUD <br>
[x] Classes CRUD <br>
[x] Students CRUD <br>
[x] Dashboard Reporting <br>
[x] Data backup in cloud location through Rabbitmq <br> <br>

## Tools and Technologies
- Python3.9
- Flask
- Mongodb
- Rabbitmq
- Rabbitmq Shovel
- Docker
- Docker compose 

## Core Components

- **App:** A Flask application for running CRUD operations on the student records.
- **Local MongoDB:** A MongoDB instance running locally in a Docker container
- **Cloud MongoDB:** A MongoDB instance running in a Docker container acting like remote mongodb
- **Local RabbitMQ:** A rabbitmq instance running locally in a Docker container
- **Cloud RabbitMQ:** A rabbitmq instance running in a Docker container and acting like remote rabbitmq
- **Shovel:** Shovel is configured inside local rabbitmq to connect with cloud rabbitmq
- **Collector:** A Python script for listening to the cloud RabbitMQ and storing the data to cloud MongoDB.

## Folder Structure

- `app/`: Contains the Flask application code.
  - `app.py`: The main application file.
  - `module`: Storing application modules
  - `templates`: Html template directory
  - `static`: Static file directory
  - `guard`: Flask route guard
  - `seeder.py`: Database seeder for dummy data
  - `rabbitmq.py`: Rabbitmq connection settings
  - `settings.py`: Storing mongodb connection
  - `Dockerfile`: Dockerfile for building the Flask application Docker image.
- `collector/`: Contains the collector code.
  - `app.py`: The collector application code.
  - `Dockerfile`: Dockerfile for building the collector Docker image.
- `docker-compose.yml`: Docker Compose configuration file for running the entire system.
- `advanced.config`: Configuration file for local Rabbitmq container to setup Shovel configuration at startup.
- `docker-entrypoint-initdb.d`: Configuration file for mongodb to create database at startup

## Running Instructions

1. Clone the Git repository: 
    ```
    git clone git@github.com:durjoi/school_management_system.git
    ```
2. Navigate to the project directory: 
   ```
   cd school_management_system
   ```
3. Copy `.env.example` to `.env`:
   _Don't change anything inside .env to run this project properly_ 
   ```
   cp .env.example .env
   ```
   
4. Build the Docker images: 
   ```
   docker-compose build
   ```
5. Start the containers: 
   ```
   docker-compose up
   ```

   _Note: Please wait for some time while the containers are being created. During the initial setup, some errors may appear, but they will be automatically resolved after a few moments._

6. Run seeder to populate dummy data
   ```
    docker exec -it smsystem /bin/sh
    python3 seeder.py
   ```
   This will seed a admin user to login in the system for the first time
   - Email: admin@admin.com
   - Password: password

The application will be accessible at [http://localhost:8050](http://localhost:8050).

## Connection information
- `Local MongoDB`: "mongodb://admin:password@mongodb1:8011/smsystem"
- `Cloud MongoDB`: "mongodb://admin:password@mongodb1:8012/smsystem"
- `Local Rabbitmq`: [http://127.0.0.1:15672](http://127.0.0.1:15672) visit this link on browser
- `Cloud Rabbitmq`: [http://127.0.0.1:15673](http://127.0.0.1:15673) visit this link on browser

Credentials for both rabbitmq are 
- username: guest  
- password: guest

## Permissions & Access

- Teacher can add/update/delete Student, Class, Marks
- Admin can add/update/delete Student, Class, Marks
- Everyone can see the dashboard
