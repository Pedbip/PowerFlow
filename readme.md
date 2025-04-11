# PowerFlow

PowerFlow is a FastAPI-based application designed to manage users, projects, and components. It provides functionality for user authentication, project and component management, and exporting project data to Excel files.

## Features

- **User Management**: Create, update, delete, and retrieve user information.
- **Project Management**: Manage projects, including adding and removing components.
- **Component Management**: Manage components and link them to projects.
- **Authentication**: Secure user authentication using JWT tokens.
- **Export to Excel**: Export project details, including components, to an Excel file.

## Installation

### Prerequisites

- Python 3.13 or later
- Docker (optional, for containerized deployment)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/Pedbip/PowerFlow-API.git
   cd PowerFlow
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   uvicorn project_management.main:app --reload
   ```

4. Access the API documentation at:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Usage

### Authentication

- Use the `/login` endpoint to obtain a JWT token by providing a username and password.
- Include the token in the `Authorization` header as `Bearer <token>` for authenticated requests.

### User Management

- **Create User**: `POST /user/`
- **Get All Users**: `GET /user/`
- **Get User by ID**: `GET /user/{id}`
- **Update User**: `PATCH /user/{id}`
- **Delete User**: `DELETE /user/{id}`

### Project Management

- **Create Project**: `POST /project/`
- **Get All Projects**: `GET /project/`
- **Get Project by ID**: `GET /project/{id}`
- **Update Project**: `PATCH /project/{id}`
- **Delete Project**: `DELETE /project/{id}`
- **Add Component to Project**: `PATCH /project/{project_id}/add-component`
- **Remove Component from Project**: `DELETE /project/{project_id}/delete-component`

### Component Management

- **Create Component**: `POST /component/`
- **Get All Components**: `GET /component/`
- **Get Component by ID**: `GET /component/{id}`
- **Update Component**: `PATCH /component/{id}`
- **Delete Component**: `DELETE /component/{id}`

### Export to Excel

- **Export Project**: `GET /export/export/{project_id}`

The exported Excel file will include project details and a summary of components.

## Deployment with Docker

1. Build the Docker image:
   ```bash
   docker-compose build
   ```

2. Start the container:
   ```bash
   docker-compose up
   ```

3. Access the application at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Project Structure

- **`project_management/routers/`**: Contains API route definitions for users, projects, components, and authentication.
- **`project_management/utils/`**: Utility modules for database, hashing, JWT handling, and OAuth2.
- **`project_management/repository/`**: Repository modules for database operations.
- **`project_management/main.py`**: Entry point for the FastAPI application.
- **`requirements.txt`**: Python dependencies.
- **`Dockerfile`**: Docker configuration for the application.
- **`docker-compose.yml`**: Docker Compose configuration.

## Database

The application uses SQLite as the database. The database file is named `db.db` and is created automatically when the application starts.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.
