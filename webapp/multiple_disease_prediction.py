import streamlit as st
import pandas as pd
import pickle
from pathlib import Path
from streamlit_option_menu import option_menu

import json
from PIL import Image
import requests  # pip install requests
from streamlit_lottie import st_lottie  # pip install streamlit-lottie


st.set_page_config(page_title="Multiple Disease Prediction", layout="wide")

# GitHub: https://github.com/andfanilo/streamlit-lottie
# Lottie Files: https://lottiefiles.com/

# loading the saved models
BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = BASE_DIR / "model"
IMAGE_DIR = BASE_DIR / "image"

diabetes_model = pickle.load(open(MODEL_DIR / 'diabetes_trained_model.sav', 'rb'))

heart_disease_model = pickle.load(open(MODEL_DIR / 'heart_disease_model.sav', 'rb'))

parkinsons_model = pickle.load(open(MODEL_DIR / 'parkinsons_model.sav', 'rb'))

lung_cancer_model = pickle.load(open(MODEL_DIR / 'lungCancer_trained_model.sav', 'rb'))


def load_lottie_url(url: str):
    """Load a Lottie animation from a URL."""
    try:
        response = requests.get(url, timeout=10)
    except Exception:
        return None
    if response.status_code != 200:
        return None
    return response.json()


def apply_global_styles() -> None:
    st.markdown(
        """
        <style>
        .main {
            padding: 1rem 3rem;
        }
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 1.5rem;
        }
        .stButton>button {
            border-radius: 8px;
            padding: 0.4rem 1.4rem;
            font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# simple helper to parse numeric inputs
def parse_float_list(values: list[str]) -> list[float] | None:
    try:
        return [float(v) for v in values]
    except (TypeError, ValueError):
        st.error("Please fill in all fields with valid numeric values.")
        return None


# Security
import hashlib


def make_hashes(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def check_hashes(password: str, hashed_text: str) -> str | bool:
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False


# DB Management
import sqlite3

DB_PATH = Path(__file__).resolve().parent / "data.db"
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()


def create_usertable() -> None:
    c.execute("CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)")


def add_userdata(username: str, password: str) -> None:
    c.execute("INSERT INTO userstable(username,password) VALUES (?,?)", (username, password))
    conn.commit()


def login_user(username: str, password: str):
    c.execute("SELECT * FROM userstable WHERE username = ? AND password = ?", (username, password))
    return c.fetchall()


def view_user_data(username: str):
    c.execute("SELECT * FROM userstable WHERE username = ?", (username,))
    return c.fetchall()


def create_metrics_table() -> None:
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS health_metrics(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            disease TEXT,
            name TEXT,
            data TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()


def save_metrics(username: str, disease: str, name: str, data: dict) -> None:
    data = canonicalize_keys(data)
    c.execute(
        "INSERT INTO health_metrics(username, disease, name, data) VALUES (?,?,?,?)",
        (username, disease, name, json.dumps(data)),
    )
    conn.commit()


def update_metrics(row_id: int, data: dict, name: str | None = None) -> None:
    data = canonicalize_keys(data)
    if name is not None:
        c.execute(
            "UPDATE health_metrics SET name = ?, data = ? WHERE id = ?",
            (name, json.dumps(data), row_id),
        )
    else:
        c.execute(
            "UPDATE health_metrics SET data = ? WHERE id = ?",
            (json.dumps(data), row_id),
        )
    conn.commit()

def get_metrics(username: str, disease: str):
    c.execute(
        "SELECT id, name, data, created_at FROM health_metrics WHERE username = ? AND disease = ? ORDER BY created_at DESC",
        (username, disease),
    )
    return c.fetchall()


def get_all_metrics(username: str):
    c.execute(
        "SELECT id, disease, name, data, created_at FROM health_metrics WHERE username = ? ORDER BY created_at DESC",
        (username,),
    )
    return c.fetchall()


CANONICAL_FIELD_ALIASES = {
    "age": "Age",
    "sex": "Sex",
    "bmi": "BMI",
}


def canonicalize_keys(data: dict) -> dict:
    normalized = {}
    for key, value in data.items():
        key_str = str(key)
        canon = CANONICAL_FIELD_ALIASES.get(key_str.lower(), key_str)
        normalized[canon] = value
    return normalized


def get_latest_metrics(username: str, disease: str):
    """Return the most recent saved metrics dict for a disease, or None."""
    c.execute(
        "SELECT data FROM health_metrics WHERE username = ? AND disease = ? ORDER BY created_at DESC LIMIT 1",
        (username, disease),
    )
    row = c.fetchone()
    if not row:
        return None
    try:
        return json.loads(row[0])
    except Exception:
        return None


def upsert_metrics(username: str, disease: str, data: dict) -> None:
    """Insert or update a single metrics record per (username, disease)."""
    data = canonicalize_keys(data)
    c.execute(
        "SELECT id FROM health_metrics WHERE username = ? AND disease = ? ORDER BY created_at DESC LIMIT 1",
        (username, disease),
    )
    row = c.fetchone()
    if row:
        c.execute(
            "UPDATE health_metrics SET data = ? WHERE id = ?",
            (json.dumps(data), row[0]),
        )
    else:
        c.execute(
            "INSERT INTO health_metrics(username, disease, name, data) VALUES (?,?,?,?)",
            (username, disease, f"{disease}_profile", json.dumps(data)),
        )
    conn.commit()


def create_history_table() -> None:
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS prediction_history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            disease TEXT,
            result TEXT,
            inputs TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()


def save_history(username: str | None, disease: str, result: str, inputs: dict) -> None:
    if not username:
        return
    inputs = canonicalize_keys(inputs)
    c.execute(
        "INSERT INTO prediction_history(username, disease, result, inputs) VALUES (?,?,?,?)",
        (username, disease, result, json.dumps(inputs)),
    )
    conn.commit()


def get_history(username: str):
    c.execute(
        "SELECT disease, result, created_at FROM prediction_history WHERE username = ? ORDER BY created_at DESC",
        (username,),
    )
    return c.fetchall()


def init_auth_state() -> None:
    if "is_authenticated" not in st.session_state:
        st.session_state.is_authenticated = False
    if "username" not in st.session_state:
        st.session_state.username = ""


def render_home_page() -> None:
    lottie_hello = load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_M9p23l.json")
    if lottie_hello:
        st_lottie(
            lottie_hello,
            speed=1,
            reverse=False,
            loop=True,
            quality="low",
            height=400,
            width=700,
            key=None,
        )

    st.markdown("### Welcome to the Multiple Disease Prediction System")
    st.markdown(
        "- Enter a few health measurements.\n"
        "- Let the trained models analyze your inputs.\n"
        "- Get an instant prediction for several common conditions."
    )

    lottie_health = load_lottie_url("https://assets7.lottiefiles.com/packages/lf20_gmspxrnd.json")
    if lottie_health:
        st_lottie(
            lottie_health,
            speed=1,
            reverse=False,
            loop=True,
            quality="low",
            height=400,
            width=700,
            key=None,
        )

    st.markdown(
        "Thank you for choosing us. Praying to God for your good health. "
        "Please help us by giving an honest feedback so that we can improve more."
    )


def render_diabetes_page() -> None:
    username = st.session_state.get("username")

    col_img, col_form = st.columns([1, 2])

    with col_img:
        img = Image.open(IMAGE_DIR / "1.webp")
        st.image(img)

    with col_form:
        st.subheader("Diabetes Prediction")
        st.caption("Based on pregnancies, glucose, blood pressure and other measurements.")

        # Load current profile values for this disease
        if username:
            if st.button("Load from profile", key="diab_load_btn"):
                loaded = get_latest_metrics(username, "diabetes")
                if loaded:
                    for field, value in loaded.items():
                        st.session_state[f"diab_{field}"] = str(value)
                    st.rerun()

        col1, col2, col3 = st.columns(3)

        with col1:
            Pregnancies = st.text_input("Number of Pregnancies", key="diab_Pregnancies")

        with col2:
            Glucose = st.text_input("Glucose Level", key="diab_Glucose")

        with col3:
            BloodPressure = st.text_input("Blood Pressure value", key="diab_BloodPressure")

        with col1:
            SkinThickness = st.text_input("Skin Thickness value", key="diab_SkinThickness")

        with col2:
            Insulin = st.text_input("Insulin Level", key="diab_Insulin")

        with col3:
            BMI = st.text_input("BMI value", key="diab_BMI")

        with col1:
            DiabetesPedigreeFunction = st.text_input(
                "Diabetes Pedigree Function value", key="diab_DiabetesPedigreeFunction"
            )

        with col2:
            Age = st.text_input("Age of the Person", key="diab_Age")

        diab_diagnosis = ""

        if st.button("Diabetes Test Result"):
            features = [
                Pregnancies,
                Glucose,
                BloodPressure,
                SkinThickness,
                Insulin,
                BMI,
                DiabetesPedigreeFunction,
                Age,
            ]
            numeric_features = parse_float_list(features)
            if numeric_features is not None:
                diab_prediction = diabetes_model.predict([numeric_features])

                if diab_prediction[0] == 1:
                    diab_diagnosis = "The person is diabetic"
                else:
                    diab_diagnosis = "The person is not diabetic"

                save_history(
                    username,
                    "diabetes",
                    diab_diagnosis,
                    {
                        "Pregnancies": Pregnancies,
                        "Glucose": Glucose,
                        "BloodPressure": BloodPressure,
                        "SkinThickness": SkinThickness,
                        "Insulin": Insulin,
                        "BMI": BMI,
                        "DiabetesPedigreeFunction": DiabetesPedigreeFunction,
                        "Age": Age,
                    },
                )

        if diab_diagnosis:
            st.success(diab_diagnosis)
            if username:
                upsert_metrics(
                    username,
                    "diabetes",
                    {
                        "Pregnancies": Pregnancies,
                        "Glucose": Glucose,
                        "BloodPressure": BloodPressure,
                        "SkinThickness": SkinThickness,
                        "Insulin": Insulin,
                        "BMI": BMI,
                        "DiabetesPedigreeFunction": DiabetesPedigreeFunction,
                        "Age": Age,
                    },
                )


def render_heart_disease_page() -> None:
    username = st.session_state.get("username")
    col_img, col_form = st.columns([1, 2])

    with col_img:
        img = Image.open(IMAGE_DIR / "2.jpg")
        st.image(img)

    with col_form:
        st.subheader("Heart Disease Prediction")
        st.caption("Uses common cardiovascular indicators like blood pressure, cholesterol and chest pain type.")

        # Load current profile values for this disease
        if username:
            if st.button("Load from profile", key="heart_load_btn"):
                loaded = get_latest_metrics(username, "heart")
                if loaded:
                    for field, value in loaded.items():
                        st.session_state[f"heart_{field}"] = str(value)
                    st.rerun()

        col1, col2, col3 = st.columns(3)

        with col1:
            age = st.text_input("Age", key="heart_Age")

        with col2:
            sex_label = st.selectbox(
                "Sex",
                ["Male", "Female"],
                key="heart_Sex",
            )

        with col3:
            cp = st.text_input("Chest Pain types", key="heart_cp")

        with col1:
            trestbps = st.text_input("Resting Blood Pressure", key="heart_trestbps")

        with col2:
            chol = st.text_input("Serum Cholestoral in mg/dl", key="heart_chol")

        with col3:
            fbs_label = st.selectbox(
                "Fasting Blood Sugar > 120 mg/dl",
                ["No", "Yes"],
                key="heart_fbs",
            )

        with col1:
            restecg = st.text_input("Resting Electrocardiographic results", key="heart_restecg")

        with col2:
            thalach = st.text_input("Maximum Heart Rate achieved", key="heart_thalach")

        with col3:
            exang_label = st.selectbox(
                "Exercise Induced Angina",
                ["No", "Yes"],
                key="heart_exang",
            )

        with col1:
            oldpeak = st.text_input("ST depression induced by exercise", key="heart_oldpeak")

        with col2:
            slope = st.text_input("Slope of the peak exercise ST segment", key="heart_slope")

        with col3:
            ca = st.text_input("Major vessels colored by flourosopy", key="heart_ca")

        with col1:
            thal = st.text_input(
                "thal: 0 = normal; 1 = fixed defect; 2 = reversable defect",
                key="heart_thal",
            )

        heart_diagnosis = ""

        if st.button("Heart Disease Test Result"):
            sex_val = 1 if sex_label == "Male" else 0
            fbs_val = 1 if fbs_label == "Yes" else 0
            exang_val = 1 if exang_label == "Yes" else 0

            features = [
                age,
                sex_val,
                cp,
                trestbps,
                chol,
                fbs_val,
                restecg,
                thalach,
                exang_val,
                oldpeak,
                slope,
                ca,
                thal,
            ]
            numeric_features = parse_float_list(features)
            if numeric_features is not None:
                heart_prediction = heart_disease_model.predict([numeric_features])

                if heart_prediction[0] == 1:
                    heart_diagnosis = "The person is having heart disease"
                else:
                    heart_diagnosis = "The person does not have any heart disease"

                save_history(
                    username,
                    "heart",
                    heart_diagnosis,
                    {
                        "Age": age,
                        "Sex": sex_label,
                        "cp": cp,
                        "trestbps": trestbps,
                        "chol": chol,
                        "fbs": fbs_label,
                        "restecg": restecg,
                        "thalach": thalach,
                        "exang": exang_label,
                        "oldpeak": oldpeak,
                        "slope": slope,
                        "ca": ca,
                        "thal": thal,
                    },
                )

        if heart_diagnosis:
            st.success(heart_diagnosis)

        if username and heart_diagnosis:
            data = {
                "Age": age,
                "Sex": sex_label,
                "cp": cp,
                "trestbps": trestbps,
                "chol": chol,
                "fbs": fbs_label,
                "restecg": restecg,
                "thalach": thalach,
                "exang": exang_label,
                "oldpeak": oldpeak,
                "slope": slope,
                "ca": ca,
                "thal": thal,
            }
            upsert_metrics(username, "heart", data)


def render_parkinsons_page() -> None:
    username = st.session_state.get("username")
    col_img, col_form = st.columns([1, 2])

    with col_img:
        img = Image.open(IMAGE_DIR / "3.webp")
        st.image(img)

    with col_form:
        st.subheader("Parkinsons Prediction")
        st.caption("Analyzes various vocal measurements related to tremor and voice stability.")

        if username:
            if st.button("Load from profile", key="park_load_btn"):
                loaded = get_latest_metrics(username, "parkinsons")
                if loaded:
                    for field, value in loaded.items():
                        st.session_state[f"park_{field}"] = str(value)
                    st.rerun()

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            fo = st.text_input("MDVP:Fo(Hz)", key="park_fo")

        with col2:
            fhi = st.text_input("MDVP:Fhi(Hz)", key="park_fhi")

        with col3:
            flo = st.text_input("MDVP:Flo(Hz)", key="park_flo")

        with col4:
            Jitter_percent = st.text_input("MDVP:Jitter(%)", key="park_Jitter_percent")

        with col5:
            Jitter_Abs = st.text_input("MDVP:Jitter(Abs)", key="park_Jitter_Abs")

        with col1:
            RAP = st.text_input("MDVP:RAP", key="park_RAP")

        with col2:
            PPQ = st.text_input("MDVP:PPQ", key="park_PPQ")

        with col3:
            DDP = st.text_input("Jitter:DDP", key="park_DDP")

        with col4:
            Shimmer = st.text_input("MDVP:Shimmer", key="park_Shimmer")

        with col5:
            Shimmer_dB = st.text_input("MDVP:Shimmer(dB)", key="park_Shimmer_dB")

        with col1:
            APQ3 = st.text_input("Shimmer:APQ3", key="park_APQ3")

        with col2:
            APQ5 = st.text_input("Shimmer:APQ5", key="park_APQ5")

        with col3:
            APQ = st.text_input("MDVP:APQ", key="park_APQ")

        with col4:
            DDA = st.text_input("Shimmer:DDA", key="park_DDA")

        with col5:
            NHR = st.text_input("NHR", key="park_NHR")

        with col1:
            HNR = st.text_input("HNR", key="park_HNR")

        with col2:
            RPDE = st.text_input("RPDE", key="park_RPDE")

        with col3:
            DFA = st.text_input("DFA", key="park_DFA")

        with col4:
            spread1 = st.text_input("spread1", key="park_spread1")

        with col5:
            spread2 = st.text_input("spread2", key="park_spread2")

        with col1:
            D2 = st.text_input("D2", key="park_D2")

        with col2:
            PPE = st.text_input("PPE", key="park_PPE")

        parkinsons_diagnosis = ""

        if st.button("Parkinson's Test Result"):
            features = [
                fo,
                fhi,
                flo,
                Jitter_percent,
                Jitter_Abs,
                RAP,
                PPQ,
                DDP,
                Shimmer,
                Shimmer_dB,
                APQ3,
                APQ5,
                APQ,
                DDA,
                NHR,
                HNR,
                RPDE,
                DFA,
                spread1,
                spread2,
                D2,
                PPE,
            ]
            numeric_features = parse_float_list(features)
            if numeric_features is not None:
                parkinsons_prediction = parkinsons_model.predict([numeric_features])

                if parkinsons_prediction[0] == 1:
                    parkinsons_diagnosis = "The person has Parkinson's disease"
                else:
                    parkinsons_diagnosis = "The person does not have Parkinson's disease"

                save_history(
                    username,
                    "parkinsons",
                    parkinsons_diagnosis,
                    {
                        "fo": fo,
                        "fhi": fhi,
                        "flo": flo,
                        "Jitter_percent": Jitter_percent,
                        "Jitter_Abs": Jitter_Abs,
                        "RAP": RAP,
                        "PPQ": PPQ,
                        "DDP": DDP,
                        "Shimmer": Shimmer,
                        "Shimmer_dB": Shimmer_dB,
                        "APQ3": APQ3,
                        "APQ5": APQ5,
                        "APQ": APQ,
                        "DDA": DDA,
                        "NHR": NHR,
                        "HNR": HNR,
                        "RPDE": RPDE,
                        "DFA": DFA,
                        "spread1": spread1,
                        "spread2": spread2,
                        "D2": D2,
                        "PPE": PPE,
                    },
                )

        if parkinsons_diagnosis:
            st.success(parkinsons_diagnosis)

        if username and parkinsons_diagnosis:
            data = {
                "fo": fo,
                "fhi": fhi,
                "flo": flo,
                "Jitter_percent": Jitter_percent,
                "Jitter_Abs": Jitter_Abs,
                "RAP": RAP,
                "PPQ": PPQ,
                "DDP": DDP,
                "Shimmer": Shimmer,
                "Shimmer_dB": Shimmer_dB,
                "APQ3": APQ3,
                "APQ5": APQ5,
                "APQ": APQ,
                "DDA": DDA,
                "NHR": NHR,
                "HNR": HNR,
                "RPDE": RPDE,
                "DFA": DFA,
                "spread1": spread1,
                "spread2": spread2,
                "D2": D2,
                "PPE": PPE,
            }
            upsert_metrics(username, "parkinsons", data)


def render_lung_cancer_page() -> None:
    img = Image.open(IMAGE_DIR / "4.webp")
    st.image(img)
    st.subheader("Lung Cancer Prediction")
    st.caption("Answer a set of lifestyle and symptom questions (Yes = 2, No = 1).")

    col1, col2, col3 = st.columns(3)

    with col1:
        AGE = st.text_input("Age")

    with col2:
        SMOKING = st.text_input("SMOKING")

    with col3:
        YELLOW_FINGERS = st.text_input("YELLOW_FINGERS")

    with col1:
        ANXIETY = st.text_input("ANXIETY")

    with col2:
        PEER_PRESSURE = st.text_input("PEER_PRESSURE")

    with col3:
        CHRONIC_DISEASE = st.text_input("CHRONIC DISEASE")

    with col1:
        FATIGUE = st.text_input("FATIGUE")

    with col2:
        ALLERGY = st.text_input("ALLERGY")

    with col3:
        WHEEZING = st.text_input("WHEEZING")

    with col1:
        ALCOHOL_CONSUMING = st.text_input("ALCOHOL CONSUMING")

    with col2:
        COUGHING = st.text_input("COUGHING")

    with col3:
        SHORTNESS_OF_BREATH = st.text_input("SHORTNESS OF BREATH")

    with col1:
        SWALLOWING_DIFFICULTY = st.text_input("SWALLOWING DIFFICULTY")

    with col2:
        CHEST_PAIN = st.text_input("CHEST PAIN")

    lung_cancer_diagnosis = ""

    if st.button("lung cancer Test Result"):
        features = [
            AGE,
            SMOKING,
            YELLOW_FINGERS,
            ANXIETY,
            PEER_PRESSURE,
            CHRONIC_DISEASE,
            FATIGUE,
            ALLERGY,
            WHEEZING,
            ALCOHOL_CONSUMING,
            COUGHING,
            SHORTNESS_OF_BREATH,
            SWALLOWING_DIFFICULTY,
            CHEST_PAIN,
        ]
        numeric_features = parse_float_list(features)
        if numeric_features is not None:
            lung_cancer_prediction = lung_cancer_model.predict([numeric_features])

            if lung_cancer_prediction[0] == 2:
                lung_cancer_diagnosis = "The person has lung cancer"
            else:
                lung_cancer_diagnosis = "The person has no lung cancer"

    if lung_cancer_diagnosis:
        st.success(lung_cancer_diagnosis)


def render_lung_cancer_page_two_col() -> None:
    username = st.session_state.get("username")
    col_img, col_form = st.columns([1, 2])

    with col_img:
        img = Image.open(IMAGE_DIR / "4.webp")
        st.image(img)

    with col_form:
        st.subheader("Lung Cancer Prediction")
        st.caption("Answer a set of lifestyle and symptom questions (Yes = 2, No = 1).")

        if username:
            if st.button("Load from profile", key="lung_load_btn"):
                loaded = get_latest_metrics(username, "lung")
                if loaded:
                    for field, value in loaded.items():
                        st.session_state[f"lung_{field}"] = str(value)
                    st.rerun()

        col1, col2, col3 = st.columns(3)

        with col1:
            AGE = st.text_input("Age", key="lung_Age")

        yn_options = ["No", "Yes"]

        with col2:
            SMOKING_label = st.selectbox("SMOKING", yn_options, key="lung_SMOKING")

        with col3:
            YELLOW_FINGERS_label = st.selectbox(
                "YELLOW_FINGERS", yn_options, key="lung_YELLOW_FINGERS"
            )

        with col1:
            ANXIETY_label = st.selectbox("ANXIETY", yn_options, key="lung_ANXIETY")

        with col2:
            PEER_PRESSURE_label = st.selectbox(
                "PEER_PRESSURE", yn_options, key="lung_PEER_PRESSURE"
            )

        with col3:
            CHRONIC_DISEASE_label = st.selectbox(
                "CHRONIC DISEASE", yn_options, key="lung_CHRONIC_DISEASE"
            )

        with col1:
            FATIGUE_label = st.selectbox("FATIGUE", yn_options, key="lung_FATIGUE")

        with col2:
            ALLERGY_label = st.selectbox("ALLERGY", yn_options, key="lung_ALLERGY")

        with col3:
            WHEEZING_label = st.selectbox("WHEEZING", yn_options, key="lung_WHEEZING")

        with col1:
            ALCOHOL_CONSUMING_label = st.selectbox(
                "ALCOHOL CONSUMING", yn_options, key="lung_ALCOHOL_CONSUMING"
            )

        with col2:
            COUGHING_label = st.selectbox("COUGHING", yn_options, key="lung_COUGHING")

        with col3:
            SHORTNESS_OF_BREATH_label = st.selectbox(
                "SHORTNESS OF BREATH", yn_options, key="lung_SHORTNESS_OF_BREATH"
            )

        with col1:
            SWALLOWING_DIFFICULTY_label = st.selectbox(
                "SWALLOWING DIFFICULTY", yn_options, key="lung_SWALLOWING_DIFFICULTY"
            )

        with col2:
            CHEST_PAIN_label = st.selectbox(
                "CHEST PAIN", yn_options, key="lung_CHEST_PAIN"
            )

        lung_cancer_diagnosis = ""

        if st.button("lung cancer Test Result"):
            def yn_to_code(label: str) -> int:
                # dataset encoding: Yes = 2, No = 1
                return 2 if label == "Yes" else 1

            features = [
                AGE,
                yn_to_code(SMOKING_label),
                yn_to_code(YELLOW_FINGERS_label),
                yn_to_code(ANXIETY_label),
                yn_to_code(PEER_PRESSURE_label),
                yn_to_code(CHRONIC_DISEASE_label),
                yn_to_code(FATIGUE_label),
                yn_to_code(ALLERGY_label),
                yn_to_code(WHEEZING_label),
                yn_to_code(ALCOHOL_CONSUMING_label),
                yn_to_code(COUGHING_label),
                yn_to_code(SHORTNESS_OF_BREATH_label),
                yn_to_code(SWALLOWING_DIFFICULTY_label),
                yn_to_code(CHEST_PAIN_label),
            ]
            numeric_features = parse_float_list(features)
            if numeric_features is not None:
                lung_cancer_prediction = lung_cancer_model.predict([numeric_features])

                if lung_cancer_prediction[0] == 2:
                    lung_cancer_diagnosis = "The person has lung cancer"
                else:
                    lung_cancer_diagnosis = "The person has no lung cancer"

                save_history(
                    username,
                    "lung",
                    lung_cancer_diagnosis,
                    {
                        "Age": AGE,
                        "SMOKING": SMOKING_label,
                        "YELLOW_FINGERS": YELLOW_FINGERS_label,
                        "ANXIETY": ANXIETY_label,
                        "PEER_PRESSURE": PEER_PRESSURE_label,
                        "CHRONIC_DISEASE": CHRONIC_DISEASE_label,
                        "FATIGUE": FATIGUE_label,
                        "ALLERGY": ALLERGY_label,
                        "WHEEZING": WHEEZING_label,
                        "ALCOHOL_CONSUMING": ALCOHOL_CONSUMING_label,
                        "COUGHING": COUGHING_label,
                        "SHORTNESS_OF_BREATH": SHORTNESS_OF_BREATH_label,
                        "SWALLOWING_DIFFICULTY": SWALLOWING_DIFFICULTY_label,
                        "CHEST_PAIN": CHEST_PAIN_label,
                    },
                )

        if lung_cancer_diagnosis:
            st.success(lung_cancer_diagnosis)

        if username:
            data = {
                "Age": AGE,
                "SMOKING": SMOKING_label,
                "YELLOW_FINGERS": YELLOW_FINGERS_label,
                "ANXIETY": ANXIETY_label,
                "PEER_PRESSURE": PEER_PRESSURE_label,
                "CHRONIC_DISEASE": CHRONIC_DISEASE_label,
                "FATIGUE": FATIGUE_label,
                "ALLERGY": ALLERGY_label,
                "WHEEZING": WHEEZING_label,
                "ALCOHOL_CONSUMING": ALCOHOL_CONSUMING_label,
                "COUGHING": COUGHING_label,
                "SHORTNESS_OF_BREATH": SHORTNESS_OF_BREATH_label,
                "SWALLOWING_DIFFICULTY": SWALLOWING_DIFFICULTY_label,
                "CHEST_PAIN": CHEST_PAIN_label,
            }
            upsert_metrics(username, "lung", data)


def render_profiles_page(username: str) -> None:
    img = Image.open(IMAGE_DIR / "5.png")
    st.image(img)
    st.subheader("User Profiles")

    user_result = view_user_data(username)
    clean_db = pd.DataFrame(user_result, columns=["Username", "Password"])
    st.dataframe(clean_db)

    metrics_rows = get_all_metrics(username)
    if metrics_rows:
        # Use the most recent preset per disease
        latest_by_disease = {}
        for row in metrics_rows:
            row_id, disease, name, data_json, created_at = row
            if disease not in latest_by_disease:
                latest_by_disease[disease] = row

        # Normalize common fields (case-insensitive) to a single canonical name
        basic_aliases = {
            "age": "Age",
            "sex": "Sex",
            "bmi": "BMI",
        }
        basic_data = {}
        disease_specific: dict[str, dict[str, str]] = {}

        for row in latest_by_disease.values():
            _, disease, name, data_json, created_at = row
            try:
                data = json.loads(data_json)
            except Exception:
                continue
            for key, value in data.items():
                key_lower = str(key).lower()
                if key_lower in basic_aliases:
                    canon = basic_aliases[key_lower]
                    if canon not in basic_data:
                        basic_data[canon] = value
                else:
                    disease_specific.setdefault(disease, {})[key] = value

        # Initialize edit state
        if "editing_basic_field" not in st.session_state:
            st.session_state["editing_basic_field"] = None
        if "editing_disease_field" not in st.session_state:
            st.session_state["editing_disease_field"] = {}

        if basic_data:
            st.subheader("Basic Data")
            for field_name in ["Age", "Sex", "BMI"]:
                if field_name not in basic_data:
                    continue
                current_val = str(basic_data.get(field_name, ""))
                is_editing = st.session_state["editing_basic_field"] == field_name
                col_field, col_value, col_action = st.columns([1, 3, 1])
                with col_field:
                    st.markdown(f"**{field_name}**")
                with col_value:
                    if is_editing:
                        new_val = st.text_input(
                            "",
                            value=current_val,
                            key=f"basic_input_{field_name}",
                            label_visibility="collapsed",
                        )
                    else:
                        st.markdown(str(current_val))
                with col_action:
                    if not is_editing:
                        if st.button("Edit", key=f"basic_edit_{field_name}"):
                            st.session_state["editing_basic_field"] = field_name
                            st.rerun()
                    else:
                        if st.button("Save", key=f"basic_save_{field_name}"):
                            # Update this single basic field in all disease profiles
                            for disease, row in latest_by_disease.items():
                                _, _, _, data_json, _ = row
                                try:
                                    data = json.loads(data_json)
                                except Exception:
                                    data = {}
                                data[field_name] = st.session_state.get(
                                    f"basic_input_{field_name}", current_val
                                )
                                upsert_metrics(username, disease, data)
                            st.session_state["editing_basic_field"] = None
                            st.success(f"{field_name} updated.")
                            st.rerun()

        if disease_specific:
            st.subheader("Disease-specific Data")
            for disease, fields in disease_specific.items():
                st.markdown(f"##### {disease.capitalize()} metrics")
                # Arrange fields in two columns to reduce vertical space
                items = list(fields.items())
                n_cols = 2
                col_slices = [items[i::n_cols] for i in range(n_cols)]
                cols = st.columns(n_cols)

                for col, slice_items in zip(cols, col_slices):
                    with col:
                        for field, value in slice_items:
                            key_id = f"{disease}:{field}"
                            is_editing = st.session_state["editing_disease_field"].get(
                                key_id, False
                            )
                            current_val = str(value)

                            sub_field, sub_value, sub_action = st.columns([1, 2, 1])
                            with sub_field:
                                st.markdown(f"**{field}**")
                            with sub_value:
                                if is_editing:
                                    new_val = st.text_input(
                                        "",
                                        value=current_val,
                                        key=f"profile_input_{key_id}",
                                        label_visibility="collapsed",
                                    )
                                else:
                                    st.markdown(current_val)
                            with sub_action:
                                if not is_editing:
                                    if st.button("Edit", key=f"profile_edit_{key_id}"):
                                        st.session_state["editing_disease_field"][key_id] = True
                                        st.rerun()
                                else:
                                    if st.button("Save", key=f"profile_save_{key_id}"):
                                        row = latest_by_disease.get(disease)
                                        base = {}
                                        if row:
                                            try:
                                                base = json.loads(row[3])
                                            except Exception:
                                                base = {}
                                        base[field] = st.session_state.get(
                                            f"profile_input_{key_id}", current_val
                                        )
                                        upsert_metrics(username, disease, base)
                                        st.session_state["editing_disease_field"][key_id] = False
                                        st.success(f"{field} updated.")
                                        st.rerun()

    # Prediction history
    history_rows = get_history(username)
    if history_rows:
        st.subheader("Prediction History")
        hist_df = pd.DataFrame(
            history_rows, columns=["Disease", "Result", "Created At"]
        )
        st.dataframe(hist_df)


def main() -> None:
    apply_global_styles()
    init_auth_state()
    create_usertable()
    create_metrics_table()
    create_history_table()
    st.title("Multiple Disease Prediction System")

    with st.sidebar:
        if st.session_state.is_authenticated:
            choice = option_menu(
                "Multiple Disease Prediction System",
                ["Home", "Dashboard"],
                icons=["house", "activity"],
                default_index=0,
            )
        else:
            choice = option_menu(
                "Multiple Disease Prediction System",
                ["Home", "Login", "SignUp"],
                icons=["house", "check-circle", "plus-circle"],
                default_index=0,
            )

    if choice == "Home":
        render_home_page()

    elif choice == "Login":
        st.subheader("Login Section")
        st.caption("Log in to access all disease prediction tools and your profile.")

        if st.session_state.is_authenticated:
            st.info("You are already logged in. Use the Dashboard to access predictions.")
            return

        lottie_hello = load_lottie_url("https://assets4.lottiefiles.com/packages/lf20_ktwnwv5m.json")

        col_anim, col_form = st.columns([2, 3])

        with col_anim:
            if lottie_hello:
                st_lottie(
                    lottie_hello,
                    speed=1,
                    reverse=False,
                    loop=True,
                    quality="low",
                    height=350,
                    width=500,
                    key=None,
                )

        with col_form:
            st.markdown("#### Sign in to your account")
            username = st.text_input("User Name", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            login_clicked = st.button("Login", key="login_button")

        if login_clicked:
            create_usertable()
            hashed_pswd = make_hashes(password)

            result = login_user(username, check_hashes(password, hashed_pswd))
            if result:
                st.session_state.is_authenticated = True
                st.session_state.username = username
                st.rerun()
            else:
                st.warning("Incorrect username or password. Please try again.")

    elif choice == "Dashboard":
        if not st.session_state.is_authenticated:
            st.warning("Please log in to access the dashboard.")
            return

        username = st.session_state.username or "User"

        col_spacer, col_status, col_logout = st.columns([2, 3, 1])
        with col_status:
            st.success(f"Logged in as {username}")
        with col_logout:
            if st.button("Logout"):
                st.session_state.is_authenticated = False
                st.session_state.username = ""
                st.rerun()

        selected = option_menu(
            "",
            [
                "Diabetes Prediction",
                "Heart Disease Prediction",
                "Parkinsons Prediction",
                "Lung Cancer Prediction",
                "Profiles",
            ],
            icons=["activity", "heart", "person", "person-fill", "person-fill"],
            default_index=0,
            orientation="horizontal",
        )

        if selected == "Diabetes Prediction":
            render_diabetes_page()
        elif selected == "Heart Disease Prediction":
            render_heart_disease_page()
        elif selected == "Parkinsons Prediction":
            render_parkinsons_page()
        elif selected == "Lung Cancer Prediction":
            render_lung_cancer_page_two_col()
        elif selected == "Profiles":
            render_profiles_page(username)

    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type="password")

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user, make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")



if __name__ == '__main__':
    main()