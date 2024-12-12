# Quiz Application

This is a simple quiz application built with **Flask** for the backend API and **Vue.js** for the frontend. The application supports user authentication, quiz participation, and stores results in a SQLite database. It also allows administrators to rebuild the database and fetch quiz information.

![Quiz Home](https://image.noelshack.com/fichiers/2024/50/4/1734012195-capture-d-cran-2024-12-12-145948.png)

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: Vue.js
- **Database**: SQLite
- **Containerization**: Docker (for both backend and frontend)
- **Authentication**: JWT (JSON Web Tokens)

## Features

### Backend (Flask)

- **/quiz-info**: Get quiz information including total question count and participant scores.
- **/rebuild-db**: Rebuild the database (admin-only).
- **/login**: Login to receive a JWT token for admin access.

### Frontend (Vue.js)

- **Admin Login**: Access the admin panel if logged in.
- **Navigation**: Navbar with dynamic login/logout state.
- **Responsive UI**: The UI adjusts based on whether the user is logged in.

## Project Setup

To run this project, you need **Docker** installed on your machine. The project is containerized using Docker, which simplifies the setup and deployment process.

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/quiz-app.git
cd quiz-app
```

### 2. Build and Run the Project with Docker Compose

Make sure Docker is running, then execute the following command to build and start the services:

```bash
docker-compose up --build
```

This will:

- Build the **quiz-api** and **quiz-ui** containers.
- Run the API on port `5000`.
- Serve the frontend UI on port `8080`.

### 3. Access the Application

- **Backend API**: The API will be available at [http://localhost:5000](http://localhost:5000).
- **Frontend UI**: The UI will be available at [http://localhost:8080](http://localhost:8080).

**The Admin password is "AdminQuiz2024"**

## Fill the database and test the application

Postman collections were collected in order to add questions into the database and fully test the application.

Add questions : https://warped-spaceship-158675.postman.co/workspace/test~9c61be90-5b53-48c5-98fd-392e087186d3/collection/31758061-de99c671-2ff3-49fe-9456-9c930dc382b0?action=share&creator=31758061&active-environment=31758061-a968e4d1-2aba-4fff-a3dc-08f048706318

Test application : https://warped-spaceship-158675.postman.co/workspace/test~9c61be90-5b53-48c5-98fd-392e087186d3/collection/31758061-a5e86d20-0c0c-422a-b887-4766b3276c7e?action=share&creator=31758061&active-environment=31758061-a968e4d1-2aba-4fff-a3dc-08f048706318

## Endpoints

### /quiz-info

**GET** Request: Fetches the quiz information such as the total number of questions and the list of participants and their scores.

Example response:

```json
{
  "size": 10,
  "scores": [
    {
      "playerName": "John Doe",
      "score": 85,
      "date": "12/12/2024 14:30:00"
    },
    {
      "playerName": "Jane Smith",
      "score": 90,
      "date": "12/12/2024 15:00:00"
    }
  ]
}
```

### /rebuild-db

**POST** Request: Rebuilds the database. Requires an `Authorization` header with a valid JWT token.

### /login

**POST** Request: Authenticates the user and returns a JWT token if the password matches.

Example request body:

```json
{
  "password": "yourpassword"
}
```

## Development

### Backend

1. Install dependencies for the backend:

```bash
pip install -r requirements.txt
```

2. Run the Flask app:

```bash
python app.py
```

### Frontend

1. Install dependencies for the frontend:

```bash
npm install
```

2. Run the Vue.js development server:

```bash
npm run serve
```

This will start the development server on [http://localhost:8080](http://localhost:8080).

## Docker Configuration

The project uses **Docker** to containerize the application. The `Dockerfile` for the backend (`quiz-api`) and frontend (`quiz-ui`) ensures that all dependencies are installed and the application is ready to run in any environment.

- **quiz-api Dockerfile**: Builds the Flask API, installs SQLite, and runs the application using Gunicorn.
- **quiz-ui Dockerfile**: Builds the Vue.js application and serves it using Nginx.

## Contributing

Feel free to open issues or submit pull requests to improve the project.

## License

This project is licensed under the MIT License.
