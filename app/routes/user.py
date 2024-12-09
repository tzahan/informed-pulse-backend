from fastapi import APIRouter, Depends, HTTPException
from app.models import UserCreate, PreferencesUpdate, InteractionRequest
from app.services.personalized_recommender import PersonalizedRecommender
from app.db import db
import requests

from app.security import get_current_user, get_password_hash, get_api_key

router = APIRouter()

# user Signup
@router.post("/register", status_code=201)
def register_user(user: UserCreate):
    existing_user = db.user_data.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_dict = {
        "name": user.name,
        "email": user.email,
        "hashed_password": get_password_hash(user.password),
        "date_of_birth": user.date_of_birth.isoformat(),  # Store as ISO string
        "preferences": user.preferences,
        "interaction_list": []  # Initially empty
    }
    db.user_data.insert_one(user_dict)
    return {"message": "User registered successfully"}

# get user data
@router.get("/")
def get_user_details(current_user: dict = Depends(get_current_user)):
    return {
        "name": current_user["name"],
        "email": current_user["email"],
        "preferences": current_user["preferences"],
    }

@router.get("/preferences")
def get_preferences(current_user: dict = Depends(get_current_user)):
    #sreturn current_user
    return {"email": current_user["email"], "preferences": current_user["preferences"]}

@router.put("/preferences")
def update_preferences(preferences: PreferencesUpdate, current_user: dict = Depends(get_current_user)):
    db.user_data.update_one(
        {"email": current_user["email"]},
        {"$set": {"preferences": preferences.preferences}}
    )
    return {"message": "Preferences updated successfully"}


@router.post("/add-interaction")
def add_interaction(request: InteractionRequest, current_user: dict = Depends(get_current_user)):
    """
    Add a news ID to the user's interaction list.
    """
    news_id = request.news_id
    if not news_id:
        raise HTTPException(status_code=400, detail="News ID is required")

    result = db.user_data.update_one(
        {"email": current_user["email"]},
        {"$addToSet": {"interaction_list": news_id}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to update interaction list")

    return {"message": f"News ID {news_id} added to interaction list"}

'''
# Call micreoservice recommender api
@router.get("/news", summary="Get personalized news recommendations")
def get_personalized_news(limit: int = 20, current_user: dict = Depends(get_current_user)):
    """
    Retrieves personalized news articles based on the user's preferences.
    """
    if not current_user.get("preferences"):
        raise HTTPException(status_code=400, detail="User has no preferences set")

    recommender_api_url = "http://127.0.0.1:8000/recommendations"
    preferences = " ".join(current_user["preferences"])  # Convert preferences list to a comma-separated string
    # print(preferences)
    try:
        # Call the recommender API
        response = requests.get(
            recommender_api_url,
            params={"preferences": preferences, "limit": limit},
            # json={"preferences": current_user["preferences"], "limit": limit},
            timeout=10  # Timeout to avoid hanging
        )
        response.raise_for_status()
        return response.json()  # Assuming the recommender API returns JSON

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Recommender API error: {str(e)}")
    '''


@router.delete("/delete/{email}")
def delete_user_by_email(email: str):#, current_user: dict = Depends(get_current_user)):
    """
    Admin can delete a user by email.
    """
    #if not current_user.get("is_admin", False):
    #    raise HTTPException(status_code=403, detail="Permission denied")

    result = db.user_data.delete_one({"email": email})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": f"User with email {email} deleted successfully"}


@router.get("/recommendations")
def get_recommendations(limit: int = 10, current_user: dict = Depends(get_current_user)):
    """
    Fetch personalized recommendations for the authenticated user.
    """
    # Fetch user data from the database
    user = db.user_data.find_one({"email": current_user["email"]})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    embedding_model = "models/text-embedding-004"
    recommender = PersonalizedRecommender(get_api_key(), embedding_model)

    preferences = " ".join(current_user["preferences"])  # Convert preferences list to a comma-separated string
    #preferences = user.get("preferences", [])
    interaction_data = user.get("interaction_list", [])

    #print(preferences)
    # Call the recommender system
    recommendations = recommender.recommend(preferences, interaction_data, limit)

    return {"recommendations": recommendations}

