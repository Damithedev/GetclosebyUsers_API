from fastapi import FastAPI
from database import doc_ref
import google.cloud
from geopy.distance import geodesic

app = FastAPI()
user1 = {'name': 'User1', 'location': (52.52, 13.405)}
user2 = {'name': 'User2', 'location': (51.51, 7.467)}
user3 = {'name': 'User3', 'location': (48.8566, 2.3522)}

# Example list of users
users = [user1, user2, user3]
@app.get("/")
async def root():
    try:
        docs = doc_ref.get()
        for doc in docs:
            print(u'Doc Data:{}'.format(doc.to_dict()))
    except google.cloud.exceptions.NotFound:
        print(u'Missing data')

@app.get("/nearby")
def get_nearby_coordinates(longitude: float, latitude: float):
    nearby_users = []
    docs = doc_ref.get()
    for doc in docs:
        user = doc.to_dict()
        print(user)
        user_lat = user['lat']
        user_lng = user['lng']
        distance = geodesic((latitude, longitude), (user_lat, user_lng)).kilometers
        print(user_lat, user_lng)
        if distance <= 100:
            nearby_users.append(user)
    return nearby_users