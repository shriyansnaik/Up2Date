import firebase_admin
from firebase_admin import credentials, firestore

def fetch_firestore_links():
    # Initialize Firestore
    cred = credentials.Certificate("alerts-data-firebase-adminsdk-fbsvc-dd63c25b81.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    
    # Get all collections
    collections = db.collections()
    result = {}
    
    for collection in collections:
        # Get all documents in the collection
        docs = collection.stream()
        
        for doc in docs:
            data = doc.to_dict()
            keyword = data.get("keyword")
            links = data.get("links", [])
            
            if keyword and isinstance(links, list):
                if keyword not in result:
                    result[keyword] = []
                result[keyword].extend(links)
    
    return result
