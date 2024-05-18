
import firebase_admin

from firebase_admin import credentials, firestore,messaging
# Fetch the service account key JSON file contents
cred = credentials.Certificate('secretkey.json')
# Initialize the app with a service account, granting admin privileges
app = firebase_admin.initialize_app(cred)

store = firestore.client()
doc_ref = store.collection(u'users')

def send_push_notification(token, title, body, imgurl,uid, distance ):
    # Create a message
    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body, image=imgurl,),
        token=token,
        data= {
            "route" : "Responder",
            "uid": uid,
            "distance": distance
        }
    )

    # Send the message
    response = messaging.send(message)
    print("Successfully sent message:", response)
