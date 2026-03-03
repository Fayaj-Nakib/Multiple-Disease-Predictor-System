## Data Dictionary and Example Values

This document describes the input fields used by the Multiple Disease Prediction System, their typical ranges (based on the datasets in `dataset/`), and concrete example rows for positive and negative cases where applicable.

All ranges below are approximate; they are meant as guidance for validating inputs and helping users understand what is “normal”.

---

## Diabetes Prediction (`dataset/diabetes.csv`)

Standard Pima Indians Diabetes dataset.

### Fields

| Field                     | Type  | Typical Range (from CSV) | Description                                                       |
|---------------------------|-------|---------------------------|-------------------------------------------------------------------|
| `Pregnancies`             | int   | 0–17                      | Number of times pregnant.                                         |
| `Glucose`                 | int   | ≈ 0–200                   | Plasma glucose concentration after 2h OGTT (mg/dL).               |
| `BloodPressure`           | int   | ≈ 0–122                   | Diastolic blood pressure (mmHg).                                  |
| `SkinThickness`           | int   | ≈ 0–99                    | Triceps skinfold thickness (mm).                                  |
| `Insulin`                 | int   | 0–846                     | 2h serum insulin (mu U/ml).                                       |
| `BMI`                     | float | ≈ 0–67                    | Body Mass Index (kg/m²).                                          |
| `DiabetesPedigreeFunction`| float | ≈ 0.08–2.42               | Family history score for diabetes.                                |
| `Age`                     | int   | ≈ 21–81                   | Age in years.                                                     |
| `Outcome`                 | int   | 0 or 1                    | 1 = diabetic (positive), 0 = non-diabetic (negative).             |

> Notes:
> - Values of `0` in `Glucose`, `BloodPressure`, `SkinThickness`, and `Insulin` often indicate “missing” in the original dataset.
> - For UI validation, reasonable human ranges are, for example: `Glucose` 50–300, `BloodPressure` 40–130, `BMI` 15–60, `Age` 18–90.

### Example Rows

| Example          | Pregnancies | Glucose | BloodPressure | SkinThickness | Insulin | BMI  | DPF   | Age | Outcome |
|------------------|------------:|--------:|--------------:|--------------:|--------:|-----:|------:|----:|--------:|
| **Positive (1)** | 6           | 148     | 72            | 35            | 0       | 33.6 | 0.627 | 50  | 1       |
| **Negative (0)** | 1           | 85      | 66            | 29            | 0       | 26.6 | 0.351 | 31  | 0       |

---

## Heart Disease Prediction (`dataset/heart_disease_data.csv`)

UCI-style Cleveland heart disease dataset.

### Fields

| Field     | Type           | Typical Range (CSV) | Description                                                                 |
|----------|----------------|----------------------|-----------------------------------------------------------------------------|
| `age`    | int            | ≈ 29–77             | Age in years.                                                               |
| `sex`    | int (0 or 1)   | 0, 1                | Sex: 0 = female, 1 = male.                                                 |
| `cp`     | int (0–3)      | 0–3                 | Chest pain type (categorical encoding).                                    |
| `trestbps`| int           | ≈ 94–200            | Resting blood pressure (mmHg).                                             |
| `chol`   | int            | ≈ 126–564           | Serum cholesterol (mg/dL).                                                 |
| `fbs`    | int (0 or 1)   | 0, 1                | Fasting blood sugar > 120 mg/dL: 1 = yes, 0 = no.                          |
| `restecg`| int (0–2)      | 0–2                 | Resting ECG result (categorical encoding).                                 |
| `thalach`| int            | ≈ 71–202            | Maximum heart rate achieved (bpm).                                         |
| `exang`  | int (0 or 1)   | 0, 1                | Exercise-induced angina: 1 = yes, 0 = no.                                  |
| `oldpeak`| float          | ≈ 0.0–6.2           | ST depression induced by exercise, relative to rest.                       |
| `slope`  | int (0–2)      | 0–2                 | Slope of the peak exercise ST segment (categorical).                       |
| `ca`     | int            | 0–4                 | Number of major vessels (0–4) colored by fluoroscopy.                      |
| `thal`   | int            | 0–3 (commonly 1–3)  | Thalassemia: 1 = normal, 2 = fixed defect, 3 = reversible defect.          |
| `target` | int (0 or 1)   | 0, 1                | 1 = heart disease present (positive), 0 = no disease (negative).           |

### Example Rows

| Example          | age | sex | cp | trestbps | chol | fbs | restecg | thalach | exang | oldpeak | slope | ca | thal | target |
|------------------|----:|----:|---:|---------:|-----:|----:|--------:|--------:|------:|--------:|------:|---:|-----:|-------:|
| **Positive (1)** | 63  | 1   | 3  | 145      | 233  | 1   | 0       | 150     | 0     | 2.3     | 0     | 0  | 1    | 1      |
| **Positive (1)** | 37  | 1   | 2  | 130      | 250  | 0   | 1       | 187     | 0     | 3.5     | 0     | 0  | 2    | 1      |
| **Negative (0)** | 53  | 0   | 2  | 128      | 216  | 0   | 0       | 115     | 0     | 0.0     | 2     | 0  | 0    | 0      |

> For UI, use dropdowns for `sex`, `fbs`, and `exang` (`Male/Female`, `Yes/No`), and map back to the numeric encodings internally.

---

## Parkinson’s Prediction (`dataset/parkinsons.csv`)

Dataset of sustained phonation voice recordings with acoustic features.

### Fields (simplified)

| Field              | Type   | Typical Range (CSV) | Description                                                   |
|--------------------|--------|---------------------|---------------------------------------------------------------|
| `name`             | string | —                   | Recording ID (e.g. `phon_R01_S01_1`).                         |
| `MDVP:Fo(Hz)`      | float  | ~88–260             | Average fundamental frequency (Hz).                           |
| `MDVP:Fhi(Hz)`     | float  | ~100–600+           | Maximum fundamental frequency (Hz).                           |
| `MDVP:Flo(Hz)`     | float  | ~65–240             | Minimum fundamental frequency (Hz).                           |
| Jitter features    | float  | ≈ 0.002–0.03        | Measures of frequency variation (`Jitter(%)`, `RAP`, etc.).   |
| Shimmer features   | float  | ≈ 0.01–0.3          | Measures of amplitude variation (`Shimmer`, `APQ*`, `DDA`).   |
| `NHR`              | float  | ~0–0.4              | Noise-to-Harmonics Ratio.                                     |
| `HNR`              | float  | ~5–40               | Harmonics-to-Noise Ratio.                                     |
| `RPDE`, `DFA`      | float  | RPDE ~0.2–0.7, DFA ~0.6–0.9 | Nonlinear dynamic/complexity measures.              |
| `spread1`, `spread2`| float | spread1 ~ -7 to -2, spread2 ~0–0.5 | Signal spread metrics.                        |
| `D2`               | float  | ~1.5–3.7            | Correlation dimension (signal complexity).                    |
| `PPE`              | float  | ~0.04–0.6           | Pitch period entropy.                                         |
| `status`           | int    | 0 or 1              | 1 = Parkinson’s (positive), 0 = healthy (negative).           |

### Example Rows

All of these example rows have `status = 1` (Parkinson’s).

| Example          | name             | Fo(Hz) | Fhi(Hz) | Flo(Hz) | Jitter(%) | Shimmer | HNR   | status |
|------------------|------------------|-------:|--------:|--------:|----------:|--------:|------:|--------|
| **Positive (1)** | phon_R01_S01_1   | 119.99 | 157.30  | 74.99   | 0.00784   | 0.04374 | 21.03 | 1      |
| **Positive (1)** | phon_R01_S02_1   | 120.27 | 137.24  | 114.82  | 0.00333   | 0.01608 | 24.89 | 1      |

> The dataset is skewed toward positive (`status = 1`) cases; healthy controls (`status = 0`) have similar feature ranges but different combinations.

For UI, all Parkinson’s inputs should be treated as continuous floats.

---

## Lung Cancer Prediction (`dataset/lungCancer.csv`)

Symptoms encoded as 1/2 categorical variables.

### Fields

| Field                  | Type              | Typical Range | Description                           | Encoding (CSV)           |
|------------------------|-------------------|---------------|---------------------------------------|--------------------------|
| `AGE`                  | int               | ≈ 21–87       | Age in years.                         |                          |
| `SMOKING`              | categorical (1/2) | 1 or 2        | Smoking history.                      | 1 = No, 2 = Yes          |
| `YELLOW_FINGERS`       | categorical (1/2) | 1 or 2        | Yellow fingers.                       | 1 = No, 2 = Yes          |
| `ANXIETY`              | categorical (1/2) | 1 or 2        | Anxiety.                              | 1 = No, 2 = Yes          |
| `PEER_PRESSURE`        | categorical (1/2) | 1 or 2        | Peer pressure.                        | 1 = No, 2 = Yes          |
| `CHRONIC DISEASE`      | categorical (1/2) | 1 or 2        | Chronic disease.                      | 1 = No, 2 = Yes          |
| `FATIGUE`              | categorical (1/2) | 1 or 2        | Fatigue.                              | 1 = No, 2 = Yes          |
| `ALLERGY`              | categorical (1/2) | 1 or 2        | Allergy.                              | 1 = No, 2 = Yes          |
| `WHEEZING`             | categorical (1/2) | 1 or 2        | Wheezing.                             | 1 = No, 2 = Yes          |
| `ALCOHOL CONSUMING`    | categorical (1/2) | 1 or 2        | Alcohol consumption.                  | 1 = No, 2 = Yes          |
| `COUGHING`             | categorical (1/2) | 1 or 2        | Coughing.                             | 1 = No, 2 = Yes          |
| `SHORTNESS OF BREATH`  | categorical (1/2) | 1 or 2        | Shortness of breath.                  | 1 = No, 2 = Yes          |
| `SWALLOWING DIFFICULTY`| categorical (1/2) | 1 or 2        | Swallowing difficulty.                | 1 = No, 2 = Yes          |
| `CHEST PAIN`           | categorical (1/2) | 1 or 2        | Chest pain.                           | 1 = No, 2 = Yes          |
| `LUNG_CANCER`          | categorical (1/2) | 1 or 2        | Lung cancer label.                    | 2 = Yes (cancer), 1 = No |

### Example Rows

| Example          | AGE | SMOKING | YELLOW_FINGERS | ANXIETY | PEER_PRESSURE | … | CHEST_PAIN | LUNG_CANCER |
|------------------|----:|--------:|---------------:|--------:|--------------:|---|-----------:|------------:|
| **Positive (2)** | 69  | 1       | 2              | 2       | 1             | … | 2          | 2           |
| **Negative (1)** | 59  | 1       | 1              | 1       | 2             | … | 1          | 1           |

> In the UI, these are shown as `Yes/No` dropdowns and mapped internally to 2/1 for the model, while profile/history views keep the human-readable labels (`Yes`/`No`).

---

## General Notes

- **Ranges** here are descriptive, based on the CSVs under `dataset/`. For strict validation you may want to clamp inputs slightly beyond these bounds but still allow reasonable human variation.
- **Targets** (`Outcome`, `target`, `status`, `LUNG_CANCER`) are not entered by the user in the web app; they were used only during model training.
- For better UX in the Streamlit app, consider:
  - Adding `help` text to each input using these descriptions and ranges.
  - Highlighting when inputs fall far outside typical ranges (e.g. `Age > 100`).

