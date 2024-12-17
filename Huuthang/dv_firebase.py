import pyrebase

# Firebase configuration (replace with your own)
firebaseConfig = {
  "apiKey": "YOUR_API_KEY",
  "authDomain": "YOUR_AUTH_DOMAIN",
  "databaseURL": "YOUR_DATABASE_URL",
  "projectId": "YOUR_PROJECT_ID",
  "storageBucket": "YOUR_STORAGE_BUCKET",
  "messagingSenderId": "YOUR_MESSAGING_SENDER_ID",
  "appId": "YOUR_APP_ID",
  "measurementId": "YOUR_MEASUREMENT_ID"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

def save_temperature_to_firebase(temperature):
    import datetime
    now = datetime.datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "ngay_thang": now.strftime("%Y-%m-%d"),
        "thoi_gian": now.strftime("%H:%M:%S"),
        "nhiet_do": temperature
    }
    db.child("Nhiet_Do").push(data) # Push data to Firebase