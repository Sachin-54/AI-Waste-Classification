# SortSense — AI Waste Classification System

> An AI-powered full-stack web application that classifies waste images into six categories using **EfficientNetB0 feature extraction + Support Vector Machine (SVM)**, with a Flask backend, responsive HTML/CSS/JavaScript frontend, and MySQL-based user authentication.

## Overview

**SortSense** is designed to make waste identification faster and easier through image-based classification.

A user can:

- Create an account and log in securely.
- Upload a waste image through the web interface.
- Preview an image before classification.
- Drag and drop an image into the classifier.
- Receive an AI-generated waste category and confidence score.
- Submit contact/feedback information through the application.

The machine-learning pipeline uses **EfficientNetB0 as a pretrained feature extractor** and an **SVM classifier** trained on the extracted features.

### Supported Waste Categories

| Class | Category |
|---:|---|
| 0 | Cardboard |
| 1 | Glass |
| 2 | Metal |
| 3 | Paper |
| 4 | Plastic |
| 5 | Trash |

---

## Key Features

### AI-Based Waste Classification
The application accepts an image and processes it through:

```text
Uploaded Image
      ↓
RGB Conversion
      ↓
Resize to 224 × 224
      ↓
EfficientNetB0 Preprocessing
      ↓
EfficientNetB0 Feature Extraction
      ↓
1280-Dimensional Feature Vector
      ↓
Feature Scaling
      ↓
SVM Classification
      ↓
Waste Category + Confidence
```

### Full-Stack Web Application

- **Frontend:** HTML5, CSS3, JavaScript
- **Backend:** Python + Flask
- **Machine Learning:** TensorFlow/Keras, EfficientNetB0, scikit-learn SVM
- **Database:** MySQL
- **Authentication:** Flask sessions + Werkzeug password hashing
- **Image processing:** Pillow
- **Model persistence:** Joblib

### User Authentication

The application includes:

- User registration
- Password hashing
- Login/logout
- Session-based authentication
- Authentication-status endpoint
- Forgot-password page/interface

### Image Upload

The classifier supports:

- JPG
- JPEG
- PNG
- WEBP
- Drag-and-drop upload
- Client-side preview
- Unique server-side filenames
- Maximum backend upload size of 10 MB

> The current frontend JavaScript limits uploads to **5 MB**, while Flask is configured for a maximum of **10 MB**. Therefore, normal browser uploads are effectively limited to 5 MB unless the frontend validation is changed.

---

# System Architecture

```text
┌───────────────────────────────────────────┐
│             Web Browser / UI              │
│                                           │
│ HTML + CSS + JavaScript                   │
│ Login • Register • Upload • Results       │
└─────────────────────┬─────────────────────┘
                      │ HTTP / Form / Fetch
                      ▼
┌───────────────────────────────────────────┐
│             Flask Application             │
│                                           │
│ Routing • Sessions • Validation • APIs    │
└──────────────┬────────────────┬───────────┘
               │                │
               │                │
               ▼                ▼
┌─────────────────────┐   ┌─────────────────┐
│   ML Inference      │   │     MySQL       │
│                     │   │                 │
│ EfficientNetB0      │   │ Users           │
│       ↓              │   │ Contact Messages│
│ Feature Scaling      │   └─────────────────┘
│       ↓              │
│ SVM Classifier       │
└─────────────────────┘
```

---

# Machine Learning Pipeline

## 1. Image Input

The user uploads an image using the web interface.

The backend accepts:

```text
.jpg
.jpeg
.png
.webp
```

The uploaded image receives a UUID-based filename to avoid collisions.

## 2. Image Preprocessing

The backend:

1. Opens the image with Pillow.
2. Converts it to RGB.
3. Resizes it to `224 × 224`.
4. Converts it into a NumPy array.
5. Applies EfficientNet preprocessing.

## 3. Feature Extraction

The application loads:

```python
EfficientNetB0(
    weights="imagenet",
    include_top=False,
    pooling="avg",
    input_shape=(224, 224, 3)
)
```

Instead of using EfficientNet's final classification layer, the network is used as a **feature extractor**.

This produces a **1280-dimensional feature representation** for each image.

## 4. Feature Scaling

The extracted feature vector is transformed using the stored scaler:

```text
model/efficientnet_scaler.pkl
```

This ensures that the features are represented in the same scale used during SVM training.

## 5. SVM Prediction

The scaled feature vector is passed to:

```text
model/efficientnet_svm.pkl
```

The SVM predicts one of the six waste classes.

## 6. Confidence

If the SVM provides probabilities, the highest class probability is returned.

Otherwise, the application derives a relative confidence score from the SVM decision function.

> The displayed confidence should be treated as a model score rather than a guaranteed real-world probability.

---

# Project Structure

```text
AI_Waste_Management/
│
├── app.py
│
├── model/
│   ├── efficientnet_svm.pkl
│   └── efficientnet_scaler.pkl
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── forgot-password.html
│
├── static/
│   ├── css/
│   │   ├── style.css
│   │   └── auth.css
│   │
│   ├── js/
│   │   ├── script.js
│   │   └── auth.js
│   │
│   └── img/
│       ├── logo.png
│       ├── cardboard.jpg
│       ├── glass.jpg
│       ├── metal.jpg
│       ├── paper.jpg
│       ├── plastic.jpg
│       └── trash.jpg
│
├── uploads/
│   └── uploaded images
│
├── database/
│   └── database files/scripts can be placed here
│
├── dataset/
│   └── training dataset can be placed here
│
├── requirements.txt
└── .gitignore
```

---

# Requirements

Before running the project, install:

- Python 3.10 or 3.11 recommended
- MySQL Server
- MySQL Workbench (recommended, optional)
- Git
- A modern web browser

The project uses TensorFlow/Keras, so using a Python version compatible with the TensorFlow release installed on your machine is important.

---

# Installation & Setup

## 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd AI_Waste_Management
```

If you already downloaded the project, simply open a terminal inside the project directory.

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal after activation.

---

## 3. Install Python Dependencies

The included `requirements.txt` was generated from a Conda environment and contains many machine-specific `file://` entries. Those entries are **not portable** and should not be used as-is for a fresh machine.

For a clean installation, install the application's core dependencies:

```bash
pip install Flask flask-cors mysql-connector-python numpy pillow joblib scikit-learn tensorflow
```

You can then verify the important packages:

```bash
pip show Flask tensorflow keras scikit-learn mysql-connector-python pillow joblib
```

### Recommended: create a clean requirements file

After confirming the application works:

```bash
pip freeze > requirements-local.txt
```

For a production repository, it is preferable to maintain a clean, portable requirements file containing only the dependencies required by the application.

---

# MySQL Database Setup

The application connects to MySQL using the database configuration currently defined in `app.py`.

The expected database name is:

```text
waste_classificaton
```

> Note: `waste_classificaton` is intentionally spelled this way because it matches the database name used by the current application code.

## 1. Start MySQL

Make sure your MySQL server is running.

You can start it using MySQL Workbench, MySQL services, or your preferred MySQL administration tool.

## 2. Create the Database

Run:

```sql
CREATE DATABASE waste_classificaton;
USE waste_classificaton;
```

## 3. Create the Users Table

Run:

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);
```

## 4. Create the Contact Messages Table

Run:

```sql
CREATE TABLE contact_messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    waste_type VARCHAR(100) NOT NULL,
    message TEXT NOT NULL
);
```

## 5. Configure Database Credentials

The current application uses:

```text
Host: localhost
User: root
Database: waste_classificaton
```

Update the password in `app.py` to match your local MySQL installation.

### Important Security Recommendation

Do **not** commit database passwords or Flask secret keys to GitHub.

The current code contains credentials directly in `app.py`. Before publishing the repository publicly, move these values to environment variables.

A recommended configuration pattern is:

```python
import os

app.secret_key = os.getenv("SECRET_KEY")

connection = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME", "waste_classificaton")
)
```

Then configure the variables in your local environment or `.env` file.

---

# Model Files

The application expects the trained model artifacts at:

```text
model/
├── efficientnet_svm.pkl
└── efficientnet_scaler.pkl
```

### `efficientnet_svm.pkl`

Contains the trained SVM classifier.

### `efficientnet_scaler.pkl`

Contains the feature scaler used to transform EfficientNet features before classification.

**Both files are required for prediction.**

If either file cannot be loaded, `/predict` will return an error.

---

# Running the Application

From the project root:

```bash
python app.py
```

The Flask server starts at:

```text
http://127.0.0.1:5000
```

Open the URL in your browser.

---

# Application Workflow

## Step 1 — Register

Open:

```text
http://127.0.0.1:5000/register
```

Create an account using:

- Name
- Email
- Password

Passwords are hashed using Werkzeug before they are stored in MySQL.

## Step 2 — Login

Open:

```text
http://127.0.0.1:5000/login
```

Enter the registered email and password.

After successful authentication, Flask stores the user's session information.

## Step 3 — Upload Waste Image

From the main application:

1. Select an image or drag and drop it.
2. Check the preview.
3. Click the classification/prediction button.

## Step 4 — AI Classification

The image is sent to:

```text
POST /predict
```

The backend performs:

```text
Image
 → EfficientNetB0
 → Feature Vector
 → Scaler
 → SVM
 → Prediction
```

## Step 5 — View Result

The response contains the predicted category, confidence score, and original filename.

Example response:

```json
{
    "success": true,
    "prediction": "Plastic",
    "confidence": 94.52,
    "filename": "plastic-bottle.jpg"
}
```

---

# API / Backend Routes

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Main application page |
| GET | `/index.html` | Main application page |
| GET/POST | `/login` | User login |
| GET/POST | `/login.html` | User login page |
| GET | `/auth-status` | Check current authentication status |
| GET | `/logout` | Clear session and log out |
| GET/POST | `/register` | User registration |
| GET/POST | `/register.html` | Registration page |
| GET | `/forgot-password` | Forgot-password page |
| GET | `/forgot-password.html` | Forgot-password page |
| GET | `/health` | Check backend/model availability |
| POST | `/predict` | Classify uploaded waste image |
| POST | `/contact` | Store contact/feedback message |

---

# Health Check

The backend provides a health endpoint:

```text
GET /health
```

Open:

```text
http://127.0.0.1:5000/health
```

A healthy response looks similar to:

```json
{
    "success": true,
    "backend": "running",
    "svm_model": true,
    "scaler": true,
    "efficientnet": true
}
```

This is useful for quickly checking whether the machine-learning components loaded successfully.

---

# Prediction API

## Request

```text
POST /predict
```

The image must be submitted using the form field:

```text
file
```

Example using JavaScript:

```javascript
const formData = new FormData();
formData.append("file", selectedFile);

const response = await fetch("/predict", {
    method: "POST",
    body: formData
});

const result = await response.json();
console.log(result);
```

## Successful Response

```json
{
    "success": true,
    "prediction": "Cardboard",
    "confidence": 91.34,
    "filename": "box.jpg"
}
```

## Common Error Responses

### No file

```json
{
    "success": false,
    "error": "No image file was uploaded."
}
```

### Invalid format

```json
{
    "success": false,
    "error": "Invalid image format. Please upload JPG, JPEG, PNG or WEBP."
}
```

### Model unavailable

```json
{
    "success": false,
    "error": "SVM model could not be loaded."
}
```

---

# Frontend

The frontend is built without a separate frontend framework.

### HTML

Located in:

```text
templates/
```

### CSS

Located in:

```text
static/css/
```

### JavaScript

Located in:

```text
static/js/
```

The JavaScript handles:

- Image selection
- Image preview
- Drag and drop
- Client-side file validation
- Authentication-state checking
- UI changes based on login status
- Communication with Flask APIs

---

# Security Considerations

The current project already includes some useful security practices:

### Password Hashing

Passwords are not stored as plain text.

```python
generate_password_hash(password)
```

is used during registration, and:

```python
check_password_hash(...)
```

is used during login.

### Safe Filenames

Uploaded filenames are sanitized using:

```python
secure_filename(...)
```

and a UUID is used to generate a unique stored filename.

### Parameterized SQL

Database queries use parameterized values rather than directly concatenating user input:

```python
cursor.execute(
    "SELECT * FROM users WHERE email = %s",
    (email,)
)
```

This reduces SQL injection risk.

### Recommended Improvements Before Production

For a production deployment, consider:

- Move database credentials to environment variables.
- Generate a strong random Flask `SECRET_KEY`.
- Disable `debug=True`.
- Add CSRF protection to form submissions.
- Add stronger server-side input validation.
- Add rate limiting to authentication and prediction endpoints.
- Validate actual image content, not only file extensions.
- Add upload cleanup/retention rules.
- Use HTTPS.
- Run Flask behind a production WSGI server.
- Avoid exposing detailed exception messages to clients.
- Add account password-reset functionality rather than only displaying a forgot-password page.

---

# Troubleshooting

## `ModuleNotFoundError`

Example:

```text
ModuleNotFoundError: No module named 'flask'
```

Activate your virtual environment and install the required dependencies:

```bash
venv\Scripts\activate
pip install Flask flask-cors mysql-connector-python numpy pillow joblib scikit-learn tensorflow
```

---

## MySQL Connection Failed

Check:

1. MySQL Server is running.
2. Host is correct.
3. Username is correct.
4. Password is correct.
5. Database `waste_classificaton` exists.
6. The required tables exist.

Test:

```sql
USE waste_classificaton;
SHOW TABLES;
```

You should see:

```text
users
contact_messages
```

---

## SVM Model Could Not Be Loaded

Check that these files exist:

```text
model/efficientnet_svm.pkl
model/efficientnet_scaler.pkl
```

Run the application from the project root:

```bash
python app.py
```

Do not start `app.py` from another working directory unless the model paths are updated.

---

## EfficientNet Fails to Load

Possible causes include:

- TensorFlow installation problems.
- Unsupported Python/TensorFlow combination.
- Missing dependencies.
- Problems downloading ImageNet weights on the first run.

Try reinstalling TensorFlow in a clean virtual environment.

---

## Feature Size Mismatch

The application verifies that the number of features produced by EfficientNet matches the number expected by the trained SVM.

If you see:

```text
Feature size mismatch
```

the feature extractor and SVM were not trained/configured with the same feature representation.

Do not retrain or replace one component independently without ensuring that the complete pipeline remains compatible.

---

# Development Notes

The project currently stores uploaded images in:

```text
uploads/
```

The directory is automatically created by Flask if it does not exist.

For a public GitHub repository, it is generally better not to commit user-uploaded images unless they are intentionally included as project examples.

You can add the following to `.gitignore` if uploads should remain local:

```gitignore
uploads/*
!uploads/.gitkeep
```

---

# Future Enhancements

Potential improvements for future versions include:

- Train and compare multiple ML models.
- Add model evaluation metrics such as accuracy, precision, recall and F1-score.
- Add a confusion matrix to the project documentation.
- Add image classification history for logged-in users.
- Store prediction history in MySQL.
- Add an administrator dashboard.
- Add password reset through email.
- Add waste disposal/recycling recommendations for each category.
- Add multilingual support.
- Add Docker support.
- Deploy the Flask application to a cloud platform.
- Add automated testing.
- Add CI/CD using GitHub Actions.
- Replace the current hard-coded configuration with environment-based configuration.
- Add a dedicated model-training pipeline separate from the production inference application.

---

# Limitations

This project is an image-classification system and its prediction depends on the quality and similarity of the input image to the data used to train the model.

Performance may be affected by:

- Poor lighting
- Blurry images
- Multiple waste objects in one image
- Objects that are partially hidden
- Background clutter
- Waste categories that visually overlap
- Images that differ significantly from the training data

The classifier should therefore be considered a decision-support tool rather than a replacement for professional waste-management procedures.

---

# Technology Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5 |
| Styling | CSS3 |
| Client-side logic | JavaScript |
| Backend | Python / Flask |
| API communication | HTTP / JSON / FormData |
| Computer Vision | Pillow |
| Deep Learning | TensorFlow / Keras |
| Feature Extractor | EfficientNetB0 |
| Classifier | Support Vector Machine (SVM) |
| Feature Scaling | scikit-learn scaler |
| Model Serialization | Joblib |
| Database | MySQL |
| Authentication | Flask Sessions + Werkzeug |
| Cross-Origin Support | Flask-CORS |

---

# Quick Start

For a quick local setup:

```bash
# 1. Clone
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd AI_Waste_Management

# 2. Create environment
python -m venv venv

# 3. Activate (Windows)
venv\Scripts\activate

# 4. Install dependencies
pip install Flask flask-cors mysql-connector-python numpy pillow joblib scikit-learn tensorflow

# 5. Configure MySQL
# Create database: waste_classificaton
# Create tables: users, contact_messages
# Update database credentials in app.py

# 6. Run
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

---

# Contributing

Contributions are welcome.

A typical contribution workflow is:

```bash
git checkout -b feature/your-feature
```

Make your changes, test the application, then:

```bash
git add .
git commit -m "Add your feature"
git push origin feature/your-feature
```

Open a pull request describing:

- What changed
- Why the change was needed
- How it was tested

---

# License

No license is currently specified for this project.

If you intend to publish the repository publicly, add an appropriate license file such as MIT, Apache-2.0, or another license that matches how you want the project to be used.

---

# Author

**Sachin**

AI Waste Management / Full-Stack Machine Learning Project

---

## Project Summary

SortSense demonstrates how a machine-learning model can be integrated into a complete web application rather than being used only as a standalone notebook.

The project combines:

**Machine Learning + Computer Vision + Flask Backend + JavaScript Frontend + MySQL + User Authentication**

to provide an end-to-end waste image classification platform.
