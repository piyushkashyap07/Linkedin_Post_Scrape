from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from pymongo import MongoClient
import tensorflow as tf
import numpy as np
import pickle
from dotenv import load_dotenv
from tensorflow.keras.preprocessing.sequence import pad_sequences

app = FastAPI()

# MongoDB connection string
MONGO_DETAILS = os.getenv("MONGO_URI")

client = MongoClient(MONGO_DETAILS)
database = client['test']
job_collection = database['job_posts']

class Job(BaseModel):
    job_title: str
    company: str
    location: str
    job_description: str
    job_category: str

class JobRequest(BaseModel):
    job_description: str

# Load the trained model
model = tf.keras.models.load_model('Checkpoints/job_category_model.h5')

# Load the tokenizer
with open('Checkpoints/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# Load the label encoder
with open('Checkpoints/label_encoder.pickle', 'rb') as handle:
    label_encoder = pickle.load(handle)

max_length = 100

@app.get('/jobs')
def get_jobs(page: int = Query(1, ge=1)):
    size = 20  # Fixed size parameter
    skips = size * (page - 1)
    jobs = list(job_collection.find({}, {"_id": 0}).skip(skips).limit(size))
    total_jobs = job_collection.count_documents({})
    return {
        "page": page,
        "size": size,
        "total": total_jobs,
        "jobs": jobs
    }

@app.get('/')
def welcome():
    return {"message": "Welcome to the deployment!!!"}

@app.post('/jobs')
def add_job(job: Job):
    job_dict = job.dict()
    result = job_collection.insert_one(job_dict)
    return {"inserted_id": str(result.inserted_id)}

@app.post('/predict')
def predict_job_category(request: JobRequest):
    text = request.job_description
    seq = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(seq, maxlen=max_length, padding='post', truncating='post')
    pred = model.predict(padded)
    category = label_encoder.inverse_transform([np.argmax(pred)])
    return {"category": category[0]}

# Run the app
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
