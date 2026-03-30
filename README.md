# 💸 PhonePe Pulse Data Analysis & Prediction



## 📌 Overview
This project is a comprehensive end-to-end data engineering and machine learning solution built around the **PhonePe Pulse** dataset. It extracts vast amounts of digital payment data, performs extensive Exploratory Data Analysis (EDA), stores the processed data in a MySQL database, and utilizes Machine Learning models to predict transaction amounts and growth probabilities. Finally, it serves these predictions through an interactive Flask web application.

## 🚀 Features
- **Data Extraction**: Automated Python scripts (`phonepe_extractor.py`, `code.py`) to parse nested JSON files from the PhonePe Pulse GitHub repository and convert them into structured Pandas DataFrames/CSVs.
- **Database Integration**: Seamlessly loads processed CSV data into a **MySQL** database (`phonepe_db`) using `SQLAlchemy` for robust data warehousing (`database.py`).
- **Exploratory Data Analysis (EDA)**: In-depth analysis of transaction trends, user behavior, and insurance metrics across various states and districts in India (`PhonePe_EDA_Completed.ipynb`).
- **Machine Learning**: 
  - **Random Forest Regressor** to predict future transaction amounts.
  - **Gradient Boosting Classifier** to determine the probability of high transaction growth (`PhonePe_ML_Completed.ipynb`).
- **Web Application**: A **Flask**-based interactive UI (`app.py` & `templates/index.html`) that allows users to input parameters (State, Year, Quarter, Category) and get real-time predictions.

## 🛠️ Technologies & Tools Used
- **Programming Language**: `Python` 🐍
- **Data Manipulation**: `Pandas`, `NumPy` 📊
- **Machine Learning**: `Scikit-Learn`, `Joblib` 🤖
- **Database**: `MySQL`, `SQLAlchemy`, `mysql-connector-python` 🗄️
- **Web Development**: `Flask`, `HTML/CSS` 🌐
- **Environment**: `Jupyter Notebook` 📓

## 📂 Project Structure
```text
📦 Phonepe_Project
 ┣ 📂 phonepe_data                 # Directory containing extracted CSV files
 ┣ 📂 templates                    # HTML templates for the Flask app
 ┃ ┗ 📜 index.html                 # Main frontend interface
 ┣ 📜 app.py                       # Flask application for ML predictions
 ┣ 📜 code.py                      # Data extraction script (alternative)
 ┣ 📜 database.py                  # Script to create DB & load CSVs into MySQL
 ┣ 📜 phonepe_extractor.py         # Main script to parse JSON from PhonePe Pulse repo
 ┣ 📜 PhonePe_EDA_Completed.ipynb  # Jupyter Notebook for EDA
 ┣ 📜 PhonePe_ML_Completed.ipynb   # Jupyter Notebook for Model Training
 ┣ 📜 phonpe_gbc_classifier.pkl    # Pre-trained Gradient Boosting Model
 ┣ 📜 phonpe_rf_regressor.pkl      # Pre-trained Random Forest Model
 ┗ 📜 README.md                    # Project documentation
```

## ⚙️ Setup & Installation

Follow these steps to set up the project locally:

### 1. Prerequisites
- Python 3.8+ installed
- MySQL Server installed and running locally
- PhonePe Pulse GitHub repository cloned to your local machine (update `PULSE_PATH` in extraction scripts accordingly).

### 2. Install Dependencies
```bash
pip install pandas numpy scikit-learn flask sqlalchemy mysql-connector-python joblib
```

### 3. Data Extraction
Update the `PULSE_PATH` variable in `phonepe_extractor.py` to point to your cloned PhonePe Pulse data directory, then run:
```bash
python phonepe_extractor.py
```
*This will generate CSV files inside the `phonepe_data` directory.*

### 4. Database Setup
Ensure your local MySQL server is running with the root user and no password (or update the credentials in `database.py`). Run the following command to create the database and load the tables:
```bash
python database.py
```

### 5. Running the Application
Start the Flask web server:
```bash
python app.py
```
Open your web browser and navigate to `http://127.0.0.1:5000/` to access the application.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📝 License
This project is licensed under the terms of the included LICENSE file.
