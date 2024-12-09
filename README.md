
# Informed Pulse Backend API  

Informed Pulse a news analysis service. This backend API provides functionalities such as user registration, login, personalized news recommendations and user interaction tracking. The system integrates with external APIs and MongoDB for efficient data management and processing.  

## Features  
- **User Management**: Register, login and manage users.  
- **Personalized Recommendations**: Provides news recommendations based on user preferences and interaction data.  
- **User Interactions**: Tracks user interactions with articles to refine recommendations.  
- **RESTful API**: Well-structured and scalable API built using FastAPI.  
- **MongoDB Integration**: Efficient storage and retrieval of user and news data.  

## Tech Stack  
- **Backend Framework**: FastAPI  
- **Database**: MongoDB  
- **Authentication**: JWT-based authentication  
- **External APIs**: Google Cloud Embedding API, Gemini API  
- **Containerization**: Docker  

## Installation  

### Prerequisites  
- Python 3.9+  
- MongoDB instance (local or cloud)  
- Docker (optional for containerized deployment)  

### Steps  
1. Clone the repository:  
   ```bash  
   git clone https://github.com/tzahan/informed-pulse-backend.git  
   cd informed-pulse-backend  
   ```  

2. Create a virtual environment and activate it:  
   ```bash  
   python -m venv venv  
   source venv/bin/activate  # On Windows: venv\Scripts\activate  
   ```  

3. Install dependencies:  
   ```bash  
   pip install -r requirements.txt  
   ```  

4. Set up environment variables in a `.env` file:  
   ```env  
   JWT_SECRET_KEY=your-secret-key
   MONGO_USERNAME=your_mongoDB_username>
   MONGO_PASSWORD=your_mongoDB_password>
   GENAI_API_KEY=your-google-cloud-api-key 
   ```  

5. Start the FastAPI server:  
   ```bash  
   uvicorn main:app --host 0.0.0.0 --port 8000  
   ```  

6. Access the API documentation at `http://localhost:8000/docs`.  

### Run with Docker  
1. Build the Docker image:  
   ```bash  
   docker build -t informed-pulse-backend .  
   ```  
2. Run the container:  
   ```bash  
   docker run -d -p 8000:8000 --env-file .env informed-pulse-backend  
   ```  

## Folder Structure  

```plaintext  
informed-pulse-backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Entry point for the app
│   ├── models.py            # Pydantic models and schemas
│   ├── routes/              # Folder for API routes
│   │   ├── user.py          # User-related endpoints
│   │   ├── auth.py          # Authentication-related endpoints
│   ├── db.py                # Database connection
│   ├── core/                # Core configurations
│   │   ├── config.py        # Application settings
│   ├── services/            # Folder for API routes
│   │   ├── fetch_news.py    # MongoDB news fetcher 
│   │   ├── personalized_recommender.py  # Recommendation logic
│   ├── security.py          # Security and authentication logic
├── Dockerfile               # Docker setup
├── requirements.txt         # Dependencies
├── .env                     # Environment variables
├── README.md
```  