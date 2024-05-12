from fastapi import FastAPI
from database import doc_ref, send_push_notification
import google.cloud
from geopy.distance import geodesic


app = FastAPI()

@app.get("/")
async def root():
    try:
        docs = doc_ref.get()
        for doc in docs:
            print(u'Doc Data:{}'.format(doc.to_dict()))
    except google.cloud.exceptions.NotFound:
        print(u'Missing data')

@app.get("/nearby")
def get_nearby_coordinates(longitude: float, latitude: float, uid:str):
    nearby_users = []
    tokens = []
    username = ""
    userpic = ""

    #rmm
    docs = doc_ref.get()
    for doc in docs:
        user = doc.to_dict()
        print(user)
        user_id = user['uid']
        user_lat = user['lat']
        user_lng = user['lng']
        if user_id == uid:
            username = user['firstname']
            userpic = user['profile picture']
            continue
        distance = geodesic((latitude, longitude), (user_lat, user_lng)).kilometers

        print(user_lat, user_lng)
        if distance <= 100:
            user['distance']= distance
            nearby_users.append(user)
    for nearby_user in nearby_users:
        send_push_notification(nearby_user['FCM'], f'{username} needs Help', f'{nearby_user["distance"]} Miles away', imgurl=userpic)
    return nearby_users