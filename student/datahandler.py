from pymongo import MongoClient
from student.models import Student
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
import pyrebase
import json
import os

firebaseConfig = {
    "apiKey": os.environ.get('FIREBASE_API_KEY'),
    "authDomain": os.environ.get('FIREBASE_AUTH_DOMAIN'),
    "databaseURL": os.environ.get('FIREBASE_DATABASE_URL'),
    "projectId": os.environ.get('FIREBASE_PROJECT_ID'),
    "storageBucket": os.environ.get('FIREBASE_STORAGE_BUCKET'),
    "messagingSenderId": os.environ.get('FIREBASE_MESSAGING_SENDER_ID'),
    "appId": os.environ.get('FIREBASE_APP_ID')
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# MongoDB connection
MONGODB_URI = "mongodb+srv://Namitha:NamiHarshu%40866@cluster0.edzfz.mongodb.net/CloudProject?retryWrites=true&w=majority"
client = MongoClient(MONGODB_URI)
db = client.get_database("CloudProject")
conn = db.Students

def createStudent(studentData,password):
    try:
        guser = auth.create_user_with_email_and_password(studentData['studentEmail'], password)
        auth.send_email_verification(guser['idToken'])
    except:
        print("google failed")
        return None
    
    try:
        user = User(username=guser['localId'],email=studentData['studentEmail'] ,first_name=studentData['studentName'],is_superuser=False)
        user.set_password("deZE%KYzH5jVBbHN")
        user.save()
        my_group = Group.objects.get(name='Studentgrp')
        my_group.user_set.add(user)
    except:
        print("Local User Failed")
        return None
    
    try:
        stu = Student(studentId = guser['localId'])
        stu.save()
    except:
        print("Student Model failed")
        return None
    
    try:
        studentData['localId'] = guser['localId']
        conn.insert_one(studentData)   
    except:
        print("mongo failed")
        return None
    return True

def getStudent(id):
    try:
        return conn.find_one({"localId" : id})
    except:
        return None