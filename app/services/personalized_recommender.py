
import google.generativeai as genai

from typing import List, Dict
import numpy as np
from app.services.fetch_news import NewsFetcher

class PersonalizedRecommender:
    def __init__(self, genai_api_key: str, model: str):
        # Constructor to initialize the recommender system.
        genai.configure(api_key=genai_api_key)
        self.embedding_model = model
        self.news_fetcher = NewsFetcher()

    def generate_embedding(self, text: str) -> np.ndarray:
       
        response = genai.embed_content(model=self.embedding_model, content=text)#self.gemini_client.embed_text(text)
        return np.array(response["embedding"])

    def compute_similarity(self, user_embedding: np.ndarray, article_embedding: np.ndarray) -> float:
        # Compute cosine similarity between user and article embeddings.

        return np.dot(user_embedding, article_embedding) / (
            np.linalg.norm(user_embedding) * np.linalg.norm(article_embedding)
        )

    def aggregate_interactions(self, interaction_embeddings: List[np.ndarray]) -> np.ndarray:
        # Aggregate user interaction embeddings by averaging.
        if not interaction_embeddings:
            return np.zeros(768)  # Return a zero vector if no interactions are found
        return np.mean(interaction_embeddings, axis=0)

    def recommend(self, user_preferences: str, user_interactions: List[str], limit: int = 5) -> List[Dict]:
        """
        Provide personalized recommendations based on user interactions and preferences.
        """
        try:
            if not user_interactions:
                print("No interaction data found for user. Defaulting to preferences only.")
                interaction_embeddings = []
            else:
                # Fetch news details and embeddings for interacted news
                interaction_news = self.news_fetcher.fetch_news_by_ids(user_interactions)
                interaction_embeddings = [np.array(item['embedding']) for item in interaction_news]
                #print(user_interactions)

            # Aggregate interaction embeddings
            aggregated_embedding = self.aggregate_interactions(interaction_embeddings)
            
            # Generate embedding for explicit user preferences
            preference_embedding = self.generate_embedding(user_preferences)

            # Combine the aggregated and preference embeddings (weighted sum)
            user_embedding = 0.5 * aggregated_embedding + 0.5 * preference_embedding

            # Fetch all news articles
            articles = self.news_fetcher.news_fetcher(limit=500)

            # Filter out already interacted articles
            interacted_ids = set(user_interactions)
            articles = [article for article in articles if str(article["_id"]) not in interacted_ids]
            
            # Calculate similarity scores
            recommendations = []
            for article in articles:
                article_embedding = np.array(article['embedding'])
                similarity = self.compute_similarity(user_embedding, article_embedding)

                # Remove unnecessary fields before adding to recommendations
                article.pop("embedding", None)
                article.pop("text", None)
                recommendations.append({**article, "similarity": similarity})

            # Sort articles by similarity score in descending order
            recommendations = sorted(recommendations, key=lambda x: x["similarity"], reverse=True)

            # Return top N recommendations
            return recommendations[:limit]
        except Exception as e:
            print(f"An error occurred during recommendation: {e}")
            return []


    '''
    def recommend(self, user_preferences: str, limit: int = 5) -> List[Dict]:
        # personalized recommendations for the user.

        # Fetch news articles
        # articles = self.news_fetcher.fetch_latest_news()
        
        articles = news_fetcher(limit=500)  # Fetch more for better filtering
        
        # Generate embedding for user preferences
        user_embedding = self.generate_embedding(user_preferences)

        # Calculate similarity scores
        recommendations = []
        for article in articles:
            # article_text = f"{article['title']} {article['text']}"
            # article_embedding = self.generate_embedding(article_text)
            article_embedding = np.array(article['embedding'])
            similarity = self.compute_similarity(user_embedding, article_embedding)

            article.pop("embedding", None)
            article.pop("text", None)
            recommendations.append({**article, "similarity": similarity})
            # recommendations.append({"title": article['title'], "text":article['text'], "similarity": similarity})

        # Sort articles by similarity score in descending order
        recommendations = sorted(recommendations, key=lambda x: x["similarity"], reverse=True)

        # Return top N recommendations
        return recommendations[:limit]
    '''