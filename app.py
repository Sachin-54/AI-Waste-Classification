# ============================================================
# TERRA SORT - AI WASTE CLASSIFICATION BACKEND
# ============================================================

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

import os
import uuid
import numpy as np
import joblib

from PIL import Image
from werkzeug.utils import secure_filename

import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.applications.efficientnet import preprocess_input


# ============================================================
# FLASK CONFIGURATION
# ============================================================

app = Flask(__name__)

# Allow frontend JavaScript to communicate with Flask
CORS(app)

# Folder where uploaded images will be stored
UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Maximum upload size = 10 MB
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

# Allowed image formats
ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp"
}

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ============================================================
# MODEL PATHS
# ============================================================

SVM_MODEL_PATH = "model/efficientnet_svm.pkl"

SCALER_PATH = "model/efficientnet_scaler.pkl"


# ============================================================
# LOAD SVM MODEL
# ============================================================

print("\n==========================================")
print("Loading TerraSort ML Model...")
print("==========================================")

try:

    svm_model = joblib.load(SVM_MODEL_PATH)

    print("SVM model loaded successfully!")
    print("Model:", SVM_MODEL_PATH)

except Exception as e:

    print("ERROR loading SVM model:")
    print(e)

    svm_model = None


# ============================================================
# LOAD SCALER
# ============================================================

try:

    scaler = joblib.load(SCALER_PATH)

    print("Scaler loaded successfully!")
    print("Scaler:", SCALER_PATH)

except Exception as e:

    print("ERROR loading scaler:")
    print(e)

    scaler = None


# ============================================================
# LOAD EFFICIENTNET
# ============================================================

print("\nLoading EfficientNet feature extractor...")

try:

    efficientnet_model = EfficientNetB0(
        weights="imagenet",
        include_top=False,
        pooling="avg",
        input_shape=(224, 224, 3)
    )

    print("EfficientNetB0 loaded successfully!")

except Exception as e:

    print("ERROR loading EfficientNet:")
    print(e)

    efficientnet_model = None


# ============================================================
# DISPLAY MODEL INFORMATION
# ============================================================

if svm_model is not None:

    print("\nSVM information:")

    try:
        print("Classes:", svm_model.classes_)
    except:
        print("Could not read model classes.")

    try:
        print(
            "Expected number of features:",
            svm_model.n_features_in_
        )
    except:
        print(
            "Could not determine expected feature count."
        )


if scaler is not None:

    print("\nScaler information:")

    try:
        print(
            "Scaler feature count:",
            scaler.n_features_in_
        )
    except:
        print(
            "Could not determine scaler feature count."
        )


print("==========================================\n")


# ============================================================
# CHECK FILE EXTENSION
# ============================================================

def allowed_file(filename):

    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in ALLOWED_EXTENSIONS


# ============================================================
# IMAGE PREPROCESSING
# ============================================================

def preprocess_image(image_path):

    """
    Converts the uploaded image into EfficientNet features.

    Pipeline:

    Image
       ↓
    RGB
       ↓
    224 x 224
       ↓
    EfficientNet preprocessing
       ↓
    EfficientNetB0
       ↓
    1280-dimensional feature vector
    """

    try:

        # ------------------------------------------
        # Open image
        # ------------------------------------------

        image = Image.open(image_path)

        # Convert image to RGB
        image = image.convert("RGB")

        # ------------------------------------------
        # Resize image
        # ------------------------------------------

        image = image.resize((224, 224))

        # ------------------------------------------
        # Convert to numpy array
        # ------------------------------------------

        image_array = np.array(image)

        # ------------------------------------------
        # Add batch dimension
        # Shape:
        #
        # (224,224,3)
        #
        # becomes:
        #
        # (1,224,224,3)
        # ------------------------------------------

        image_array = np.expand_dims(
            image_array,
            axis=0
        )

        # ------------------------------------------
        # EfficientNet preprocessing
        # ------------------------------------------

        image_array = preprocess_input(
            image_array
        )

        # ------------------------------------------
        # Extract EfficientNet features
        # ------------------------------------------

        features = efficientnet_model.predict(
            image_array,
            verbose=0
        )

        # ------------------------------------------
        # Flatten
        # ------------------------------------------

        features = features.reshape(1, -1)

        return features

    except Exception as e:

        print("Image preprocessing error:")
        print(e)

        raise e


# ============================================================
# GET PREDICTION LABEL
# ============================================================

def get_prediction_label(prediction):

    """
    Convert numeric SVM prediction into a readable waste label.
    """

    # Convert numpy values into normal Python values
    if isinstance(prediction, np.generic):
        prediction = prediction.item()

    # Numeric class mapping
    labels = {
        0: "Cardboard",
        1: "Glass",
        2: "Metal",
        3: "Paper",
        4: "Plastic",
        5: "Trash"
    }

    # Return the waste category
    if prediction in labels:
        return labels[prediction]

    # If the model already returns a string
    return str(prediction)


# ============================================================
# CALCULATE CONFIDENCE
# ============================================================

def get_confidence(features):

    """
    Gets an approximate confidence value.

    If the SVM was trained with probability=True,
    predict_proba() is used.

    Otherwise, the SVM decision function is converted
    into a relative score.

    """

    try:

        # ------------------------------------------
        # SVM probability
        # ------------------------------------------

        if hasattr(
            svm_model,
            "predict_proba"
        ):

            probabilities = svm_model.predict_proba(
                features
            )

            confidence = np.max(
                probabilities
            ) * 100

            return round(
                float(confidence),
                2
            )

        # ------------------------------------------
        # SVM decision function
        # ------------------------------------------

        if hasattr(
            svm_model,
            "decision_function"
        ):

            decision_scores = svm_model.decision_function(
                features
            )

            # Binary classification
            if np.ndim(decision_scores) == 1:

                score = abs(
                    float(decision_scores[0])
                )

                confidence = (
                    score /
                    (1 + score)
                ) * 100

                return round(
                    min(confidence, 99.99),
                    2
                )

            # Multiclass classification
            else:

                scores = np.asarray(
                    decision_scores[0]
                )

                # Softmax-like conversion
                scores = scores - np.max(scores)

                probabilities = np.exp(scores)

                probabilities = (
                    probabilities /
                    np.sum(probabilities)
                )

                confidence = (
                    np.max(probabilities)
                    * 100
                )

                return round(
                    float(confidence),
                    2
                )

    except Exception as e:

        print(
            "Confidence calculation error:",
            e
        )

    return None


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
@app.route("/index.html")
def home():
    return render_template("index.html")


# ============================================================
# PAGE ROUTES
# ============================================================

@app.route("/login")
@app.route("/login.html")
def login():
    return render_template("login.html")


@app.route("/register")
@app.route("/register.html")
def register():
    return render_template("register.html")


@app.route("/forgot-password")
@app.route("/forgot-password.html")
def forgot_password():
    return render_template("forgot-password.html")


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health", methods=["GET"])
def health():

    model_status = (
        svm_model is not None
    )

    scaler_status = (
        scaler is not None
    )

    efficientnet_status = (
        efficientnet_model is not None
    )

    return jsonify({

        "success": True,

        "backend": "running",

        "svm_model": model_status,

        "scaler": scaler_status,

        "efficientnet": efficientnet_status

    })


# ============================================================
# WASTE IMAGE PREDICTION
# ============================================================

@app.route(
    "/predict",
    methods=["POST"]
)
def predict():

    try:

        # ====================================================
        # CHECK MODELS
        # ====================================================

        if svm_model is None:

            return jsonify({

                "success": False,

                "error":
                    "SVM model could not be loaded."

            }), 500


        if scaler is None:

            return jsonify({

                "success": False,

                "error":
                    "Scaler could not be loaded."

            }), 500


        if efficientnet_model is None:

            return jsonify({

                "success": False,

                "error":
                    "EfficientNet could not be loaded."

            }), 500


        # ====================================================
        # CHECK FILE
        # ====================================================

        if "file" not in request.files:

            return jsonify({

                "success": False,

                "error":
                    "No image file was uploaded."

            }), 400


        file = request.files["file"]


        # ====================================================
        # CHECK FILENAME
        # ====================================================

        if file.filename == "":

            return jsonify({

                "success": False,

                "error":
                    "No image was selected."

            }), 400


        # ====================================================
        # CHECK FILE TYPE
        # ====================================================

        if not allowed_file(
            file.filename
        ):

            return jsonify({

                "success": False,

                "error":
                    "Invalid image format. "
                    "Please upload JPG, JPEG, PNG or WEBP."

            }), 400


        # ====================================================
        # CREATE SAFE UNIQUE FILENAME
        # ====================================================

        original_filename = secure_filename(
            file.filename
        )

        extension = original_filename.rsplit(
            ".",
            1
        )[1].lower()

        unique_filename = (
            str(uuid.uuid4())
            + "."
            + extension
        )


        # ====================================================
        # SAVE IMAGE
        # ====================================================

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            unique_filename
        )

        file.save(filepath)

        print("\n==========================================")
        print("New image received")
        print("Filename:", original_filename)
        print("Saved as:", filepath)
        print("==========================================")


        # ====================================================
        # EXTRACT EFFICIENTNET FEATURES
        # ====================================================

        features = preprocess_image(
            filepath
        )

        print(
            "EfficientNet feature shape:",
            features.shape
        )


        # ====================================================
        # SCALE FEATURES
        # ====================================================

        scaled_features = scaler.transform(
            features
        )

        print(
            "Scaled feature shape:",
            scaled_features.shape
        )


        # ====================================================
        # CHECK FEATURE DIMENSION
        # ====================================================

        try:

            expected_features = (
                svm_model.n_features_in_
            )

            actual_features = (
                scaled_features.shape[1]
            )

            if (
                expected_features
                != actual_features
            ):

                return jsonify({

                    "success": False,

                    "error":
                        "Feature size mismatch. "
                        f"The SVM expects "
                        f"{expected_features} features, "
                        f"but EfficientNet generated "
                        f"{actual_features} features."

                }), 500

        except AttributeError:

            pass


        # ====================================================
        # SVM PREDICTION
        # ====================================================

        prediction = svm_model.predict(
            scaled_features
        )

        predicted_value = prediction[0]


        # ====================================================
        # CONVERT TO LABEL
        # ====================================================

        predicted_class = get_prediction_label(
            predicted_value
        )


        # ====================================================
        # CONFIDENCE
        # ====================================================

        confidence = get_confidence(
            scaled_features
        )


        # ====================================================
        # PRINT RESULT
        # ====================================================

        print("\nPrediction result:")
        print(
            "Predicted class:",
            predicted_class
        )
        print(
            "Confidence:",
            confidence
        )
        print("==========================================\n")


        # ====================================================
        # RETURN RESULT TO FRONTEND
        # ====================================================

        return jsonify({

            "success": True,

            "prediction":
                predicted_class,

            "confidence":
                confidence,

            "filename":
                original_filename

        })


    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except Exception as e:

        print("\n==========================================")
        print("PREDICTION ERROR")
        print("==========================================")
        print(str(e))
        print("==========================================\n")

        return jsonify({

            "success": False,

            "error":
                "An error occurred while "
                "processing the image.",

            "details":
                str(e)

        }), 500


# ============================================================
# FILE SIZE ERROR
# ============================================================

@app.errorhandler(413)
def file_too_large(error):

    return jsonify({

        "success": False,

        "error":
            "File is too large. "
            "Maximum size is 10 MB."

    }), 413


# ============================================================
# GENERAL ERROR HANDLER
# ============================================================

@app.errorhandler(500)
def internal_error(error):

    return jsonify({

        "success": False,

        "error":
            "Internal server error."

    }), 500


# ============================================================
# RUN FLASK APPLICATION
# ============================================================

if __name__ == "__main__":

    print("\n")
    print("==========================================")
    print("        TERRASORT BACKEND")
    print("==========================================")
    print("Server starting...")
    print("URL: http://127.0.0.1:5000")
    print("==========================================")
    print("\n")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )