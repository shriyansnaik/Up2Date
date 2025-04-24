import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

def fetch_and_delete_firestore_links():
    cred_json = os.environ.get("FIREBASE_CREDENTIALS")
    if not cred_json:
        raise ValueError("FIREBASE_CREDENTIALS environment variable not set")

    cred_dict = json.loads(cred_json)
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)
    
    db = firestore.client()
    collections = db.collections()
    result = {}
    
    for collection in collections:
        docs = collection.stream()
        docs_to_delete = []
        
        for doc in docs:
            docs_to_delete.append(doc.id)
            data = doc.to_dict()
            keyword = data.get("keyword")
            links = data.get("links", [])
            
            if keyword and isinstance(links, list):
                if keyword not in result:
                    result[keyword] = []
                result[keyword].extend(links)
        
        for doc_id in docs_to_delete:
            collection.document(doc_id).delete()
    
    return result
