
import firebase_admin

from firebase_admin import credentials, firestore
# Fetch the service account key JSON file contents
cred = credentials.Certificate('secretkey.json')
# Initialize the app with a service account, granting admin privileges
app = firebase_admin.initialize_app(cred)

store = firestore.client()
doc_ref = store.collection(u'users')
