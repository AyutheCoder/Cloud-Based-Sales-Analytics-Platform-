# Google Cloud Data Analytics Project

This repository contains code and configuration files for Google Cloud Data Analytics Project.This project demonstrates the integration of several GCP services to create an efficient and automated data pipeline for sales data. We'll show you how to:


Refer youtube Video for this project
 [![YouTube](https://img.shields.io/badge/YouTube-Video-red)](https://youtu.be/_CQCOusfGrs)


![image](https://github.com/vishal-bulbule/sales-data-pipeline-project/assets/143475073/530f2c9e-945c-414c-8c85-5b489e92360e)



## Overview

1. **Web Portal**: Built with Python Flask to allow users to upload sales data files.
2. **Angular Frontend**: A modern UI with Firebase Authentication and secure uploads.
2. **Storage**: Uploaded files are stored in a GCS bucket.
3. **Cloud Function**: Automatically triggered when a file is uploaded to the GCS bucket, extracts data from the file, and loads it into BigQuery.
4. **ETL Process**: Extract, Transform, Load process implemented to handle data from raw upload to processed state.
5. **Reporting**: Summary views and dashboards in Looker Studio for key metrics, with filtering and drill-down capabilities.



![image](https://github.com/vishal-bulbule/sales-data-pipeline-project/assets/143475073/613ef050-9538-4a87-98f5-95694e87455e)

## Architecture

![image](https://github.com/vishal-bulbule/sales-data-pipeline-project/assets/143475073/7ec3e2ec-f981-4fe4-9b3e-2c48dcbcdf0a)

## Local development

### Prerequisites

- Python 3.11+ and pip
- Node.js 18+ and npm 10+
- Google Cloud CLI (`gcloud`) with access to the same GCP project
- A Firebase project with Email/Password authentication enabled
- A GCS bucket such as `bkt-sales-data`

### Backend (Flask)

1. Create and activate a virtual environment:
   - Windows PowerShell:
     - `python -m venv .venv`
     - `.\.venv\Scripts\Activate.ps1`
   - macOS/Linux:
     - `python -m venv .venv`
     - `source .venv/bin/activate`
2. Install Python dependencies:
   - `pip install -r requirements.txt`
3. Authenticate Google Cloud locally for GCS access:
   - `gcloud auth application-default login`
4. Set environment variables for the local run:
   - `GCS_BUCKET_NAME=bkt-sales-data`
   - `FIREBASE_PROJECT_ID=ayushi-sales-analytics`
   - `ALLOWED_ORIGINS=http://localhost:4200`
5. Start the backend:
   - `python main.py`

The backend will run on `http://localhost:8080/`. Use `http://localhost:8080/health` to confirm it is alive.

### Frontend (Angular)

1. The frontend already uses the local backend URL in [frontend/src/environments/environment.ts](frontend/src/environments/environment.ts).
2. Install frontend dependencies:
   - `cd frontend`
   - `npm install`
3. Start the Angular dev server:
   - `npm start`

The frontend will run on `http://localhost:4200/`.

### Troubleshooting

- If the backend fails with `DefaultCredentialsError`, run `gcloud auth application-default login` again.
- If uploads fail, confirm the GCS bucket exists and the service account has `roles/storage.objectCreator` on that bucket.
- If you use a different Firebase project ID, update `FIREBASE_PROJECT_ID` in the backend environment and the Firebase config in [frontend/src/environments/environment.ts](frontend/src/environments/environment.ts).

## Firebase Authentication

1. In the Firebase console, enable **Email/Password** auth.
2. Add `localhost` and your Cloud Run frontend domain to **Authorized domains**.

## Cloud Run deployment (two services)

### Backend service

1. Deploy:
	- `gcloud run deploy sales-backend --source . --region asia-south1 --allow-unauthenticated`
2. Set environment variables on the service:
	- `GCS_BUCKET_NAME=bkt-sales-data`
	- `FIREBASE_PROJECT_ID=ayushi-sales-analytics`
	- `ALLOWED_ORIGINS=https://YOUR_FRONTEND_URL`

### Frontend service

1. Update production config with the backend URL:
	- [frontend/src/environments/environment.prod.ts](frontend/src/environments/environment.prod.ts)
2. Deploy:
	- `gcloud run deploy sales-frontend --source ./frontend --region asia-south1 --allow-unauthenticated`

## Notes

- The backend verifies Firebase ID tokens and only accepts authenticated uploads on `/api/upload`.
- Ensure the Cloud Run service account has `roles/storage.objectCreator` on your bucket.
