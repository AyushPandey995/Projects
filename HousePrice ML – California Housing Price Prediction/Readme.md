# 🏠 HousePrice ML – California Housing Price Prediction

A machine learning project that predicts **median house values in California** from location, income, and housing characteristics. It covers the full workflow: data exploration, cleaning, visualization, preprocessing, model training, model persistence, and inference.

---

## 📌 Project Overview

The California housing dataset describes housing districts across the state. This project explores and cleans the raw data, builds a preprocessing pipeline for numerical and categorical features, and trains a **Random Forest Regressor** to predict `median_house_value`. The trained model and pipeline are saved with Joblib and reused to generate predictions on unseen data.

---

## 📈 Results

**Sample predictions** (from `predicted.csv`):

| Actual `median_house_value` | Predicted `median_house_value` |
| --------------------------- | ------------------------------ |
| XXXX                        | XXXX                           |
| XXXX                        | XXXX                           |
| XXXX                        | XXXX                           |

---

## 📊 Dataset

The dataset is the California Housing dataset, derived from the 1990 US Census: [add source link here].

| Feature              | Description                                  |
| -------------------- | -------------------------------------------- |
| `longitude`          | Longitude of the housing area                |
| `latitude`           | Latitude of the housing area                 |
| `housing_median_age` | Median age of houses in the area             |
| `total_rooms`        | Total number of rooms                        |
| `total_bedrooms`     | Total number of bedrooms                     |
| `population`         | Population of the area                       |
| `households`         | Number of households                         |
| `median_income`      | Median income of the area                    |
| `ocean_proximity`    | Categorical: proximity to the ocean          |

**Target variable:** `median_house_value`

**Data quirks handled:**
- `total_bedrooms` contains missing values, filled using median imputation.
- `median_house_value` is capped at a maximum value in the raw data, which can limit accuracy for the most expensive districts.

---

## 🔄 Project Workflow

```text
California Housing Dataset
          │
          ▼
 Exploration, Cleaning & Visualization
          │
          ▼
 Stratified Train/Test Split (on income category)
          │
          ▼
 ColumnTransformer Pipeline
   ┌──────┴──────────────┐
   ▼                     ▼
 Numerical Features    Categorical Feature
   │                     │
   ▼                     ▼
 Median Imputation     One-Hot Encoding
   │                     │
   ▼                     │
 Standard Scaling        │
   └──────┬──────────────┘
          ▼
 Random Forest Regressor
          │
          ▼
 House Price Prediction
```

---

## 🧹 Data Preprocessing

**Numerical features**
- Missing values are filled with the **median** (`SimpleImputer`).
- Values are standardized with `StandardScaler`.

**Categorical feature (`ocean_proximity`)**
- Converted to numerical form with:

```python
OneHotEncoder(handle_unknown='ignore')
```

Both branches are combined with a `ColumnTransformer` so the exact same transformations are applied at training and inference time.

---

## ✂️ Train/Test Split

`StratifiedShuffleSplit` keeps the income distribution consistent across the train and test sets. An `income_cat` column is created by binning `median_income` into categories, and the split is stratified on it.

```text
Test size:     20%
Random state:  42
```

---

## 🤖 Model

```python
model = RandomForestRegressor(random_state=42)
model.fit(housing_prepared, housing_labels)
```

The trained model and the preprocessing pipeline are saved with Joblib:

```text
model.pkl
pipeline.pkl
```

---

## 🔮 Inference

At prediction time, the saved pipeline transforms the input data and the saved model generates predictions. Results are written to `predicted.csv` with these columns:

```text
median_house_value
predicted_median_house_value
```

---

## 🚀 How to Run

**1. Clone the repository**

```bash
git clone https://github.com/<your-username>/HousePrice-ML.git
cd HousePrice-ML
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Run the project**

```bash
python main.py
```

The script trains the model and saves `model.pkl` and `pipeline.pkl` if they don't exist. Otherwise it loads them and writes predictions to `predicted.csv`.

---

## 🛠️ Tech Stack

Python · NumPy · Pandas · Scikit-learn · Joblib · Matplotlib

---

## 🔭 Future Improvements

- Compare multiple regressors (Gradient Boosting, XGBoost, Linear Regression)
- Hyperparameter tuning with `GridSearchCV` / `RandomizedSearchCV`
- Cross-validation for more reliable performance estimates
- Feature engineering (rooms per household, bedrooms per room, population per household)
- A simple web interface for live predictions
- Model deployment

---

## 👨‍💻 About

Built as part of my learning journey in **Data Science and Machine Learning**, taking raw housing data through cleaning, preprocessing, modeling, and prediction.
