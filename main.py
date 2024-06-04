from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import doc_ref, send_push_notification
import google.cloud
from geopy.distance import geodesic
import socketio


app = FastAPI()

# Configure CORS for FastAPI
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Socket.IO server with ASGI mode and CORS allowed origins
sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='asgi')

# Wrap Socket.IO server with ASGI application
socket_app = socketio.ASGIApp(sio, app)
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
            if user['FCM'] is not None:
                nearby_users.append(user)
    for nearby_user in nearby_users:

        send_push_notification(nearby_user['FCM'], f'{username} needs Help', f'{nearby_user["distance"]} Miles away', imgurl=userpic, uid= uid, distance= f'{nearby_user["distance"]}')
    return nearby_users


@sio.on("connect")
async def connect(sid, env):
      print("New Client Connected to This id :"+" "+str(sid))
      await sio.emit("send_msg", "Hello from Server", to='2339djjd')
@sio.on("disconnect")
async def disconnect(sid):
    print("Client Disconnected: "+" "+str(sid))

@sio.on("helpneeded")
async def helpusers(sid, msg):
    print(msg)




if __name__ == '__main__':
    import uvicorn
    uvicorn.run(socket_app, host='0.0.0.0', port=8000)