# import os
# from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import PyMongoError
from datetime import datetime, timedelta
from app.db import db
import logging

from typing import List, Dict
from bson import ObjectId


class NewsFetcher:
    def __init__(self):
        """
        Constructor to initialize MongoDB connection parameters.
        """
        # load_dotenv()
        # username = os.getenv("MONGO_USERNAME")
        # password = os.getenv("MONGO_PASSWORD")
        
        # self.uri = f"mongodb+srv://{username}:{password}@cluster0.3rx4l.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        #self.uri = db_uri
        #self.db_name = db_name
        self.collection_name = "news_scraper"

    def serialize_doc(self, doc: Dict) -> Dict:
        """
        Converts MongoDB ObjectId to string and processes nested fields if needed.
        """
        for key, value in doc.items():
            if isinstance(value, ObjectId):
                doc[key] = str(value)
            elif isinstance(value, list):
                doc[key] = [self.serialize_doc(item) if isinstance(item, dict) else item for item in value]
        return doc

    def news_fetcher(self, limit: int) -> List[Dict]:
        """
        Efficiently fetch news articles from MongoDB with nested 'top_5_similar'.
        Filters invalid documents at the database level.
        """
        try:
            collection = db[self.collection_name]

            # Use MongoDB query to exclude documents with None values
            all_documents = list(
                collection.find(
                    {
                        # Filters to exclude None values for required fields
                        "title": {"$exists": True, "$ne": None},
                        "summary": {"$exists": True, "$ne": None},
                        "sentiment": {"$exists": True, "$ne": None},
                        "embedding": {"$exists": True, "$ne": None},
                        # Check nested array field for non-empty lists
                        "$or": [
                            {"top_5_similar": {"$exists": False}},  # If not present, accept it
                            {"top_5_similar": {"$ne": []}}         # If present, must not be empty
                        ]
                    },
                    {
                        "_id": 1,
                        "title": 1,
                        "summary": 1,
                        "sentiment": 1,
                        "main_image": 1,
                        "embedding": 1,
                        "domain": 1,
                        "category": 1,
                        "url": 1,
                        "publication_date": 1,
                        "top_5_similar": 1
                    }
                ).limit(limit)
            )

            # Serialize ObjectIds and nested fields for valid documents
            return [self.serialize_doc(doc) for doc in all_documents]

        except Exception as e:
            print(f"An error occurred: {e}")
            return []
        

    def fetch_news_by_ids(self, news_ids: List[str]) -> List[Dict]:
            """
            Fetch news articles based on a list of news IDs.
            """
            try:
                collection = db[self.collection_name]
                object_ids = [ObjectId(news_id) for news_id in news_ids]

                # Fetch articles that match any of the given IDs
                news_articles = list(
                    collection.find(
                        {
                            "_id": {"$in": object_ids}  # Match any ID in the list
                        
                            # Filters to exclude None values for required fields
                            #"title": {"$exists": True, "$ne": None},
                            #"summary": {"$exists": True, "$ne": None},
                            #"sentiment": {"$exists": True, "$ne": None},
                            #"embedding": {"$exists": True, "$ne": None},
                        },
                        {
                            "_id": 1,
                            "embedding": 1
                        }
                    )
                )

                # Serialize ObjectIds and nested fields for valid documents
                return [self.serialize_doc(doc) for doc in news_articles]
            except Exception as e:
                print(f"Error fetching news by IDs: {e}")
                return []




    '''
    def news_fetcher(limit: int) -> List[Dict]:
        """
        Fetch news articles from MongoDB.
        """
        try:
            collection = db.news_scraper
            all_documents = list(
                collection.find({}, {
                    "_id": 1,
                    "title": 1,
                    "summary": 1,
                    "sentiment": 1,
                    "main_image": 1,
                    "embedding": 1,
                    "domain": 1,
                    "category": 1,
                    "url": 1,
                    "publication_date": 1,
                    #"top_5_similar": 1, 
                }).limit(limit)
            )
            #return all_documents
            
            # Efficient filtering: Check if 'embedding' exists and is not None
            filtered_documents = []
            for doc in all_documents:
                # Check if any field is None, skip document if found
                if any(value is None for value in doc.values()):
                    continue  # Skip this document
                
                # Otherwise, add the document to the filtered list
                filtered_documents.append(doc)

            return filtered_documents

        except Exception as e:
            print(f"An error occurred: {e}")
            return []
    '''
