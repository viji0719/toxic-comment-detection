# 🛡️ Toxic Comment Detection System

A Machine Learning–powered web application that detects and moderates toxic/offensive comments in real time using Natural Language Processing.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [API Endpoints](#api-endpoints)
- [ML Pipeline](#ml-pipeline)
- [Database Schema](#database-schema)

---

## Overview

This system analyzes user-submitted comments and classifies them as toxic or non-toxic using a trained Logistic Regression model with TF-IDF vectorization. It includes user authentication, admin moderation tools, and automatic user blocking after repeated violations.

---

## ✨ Features

- 🔍 **Real-time toxic comment detection** using a trained ML model
- 🔤 **Text normalization** to catch bypass attempts (e.g., `b!tch` → `bitch`)
- 🚫 **Automatic user blocking** after 2 toxic comments
- 👤 **User authentication** (register/login)
- 🛠️ **Admin dashboard** to review, filter, and delete flagged comments
- 💾 **SQLite database** for persistent storage of users and comments

---

## 📁 Project Structure

```
toxic-comment-detection/
│
├── app.py                        # Main Flask server (REST API)
│
├── ml_pipeline/
│   ├── step1_view_data.py        # Load and inspect the dataset
│   ├── step2_text_to_numbers.py  # Convert text to TF-IDF vectors
│   ├── step3_train_model.py      # Train Logistic Regression classifier
│   ├── step4_test_model.py       # Test model performance
│   └── step5_save_model.py       # Save trained model and vectorizer
│
├── models/
│   ├── toxic_model.pkl           # Pre-trained Logistic Regression model
│   └── vectorizer.pkl            # Fitted TF-IDF vectorizer
│
├── database/
│   ├── comments.db               # SQLite database
│   ├── create_users_table.py     # Initialize users table
│   ├── reset_db.py               # Reset entire database
│   ├── reset_tables.py           # Reset specific tables
│   └── reset_comments_table.py   # Reset comments table only
│
└── data/
    └── train.csv                 # Training dataset (comment_text, toxic label)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| ML Model | Scikit-learn (Logistic Regression) |
| Vectorizer | TF-IDF (Scikit-learn) |
| Database | SQLite |
| Serialization | Pickle (.pkl) |

---

## 🚀 Getting Started

### Prerequisites

```bash
pip install flask scikit-learn pandas numpy
```

### Run the Server

```bash
python app.py
```

The API will be available at `http://localhost:5000`.

### (Optional) Retrain the Model

If you want to retrain the model from scratch using `train.csv`, run the pipeline steps in order:

```bash
python step1_view_data.py
python step2_text_to_numbers.py
python step3_train_model.py
python step4_test_model.py
python step5_save_model.py
```

### Initialize the Database

```bash
python create_users_table.py
```

---

## 🔌 API Endpoints

### Auth

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/register` | Register a new user |
| `POST` | `/login` | Login and receive session token |

### Comments

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/submit_comment` | Submit a comment for toxicity analysis |
| `GET` | `/comments` | Retrieve all submitted comments |

### Admin

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/admin/comments` | View all comments |
| `GET` | `/admin/toxic` | View toxic comments only |
| `DELETE` | `/admin/comment/<id>` | Delete a specific comment |

---

## 🤖 ML Pipeline

1. **Data Loading** — Reads `train.csv` containing `comment_text` and binary `toxic` labels.
2. **Vectorization** — Transforms raw text into numerical TF-IDF feature vectors.
3. **Training** — Fits a Logistic Regression classifier on the vectorized data.
4. **Evaluation** — Tests accuracy, precision, recall, and F1-score.
5. **Persistence** — Saves the model (`toxic_model.pkl`) and vectorizer (`vectorizer.pkl`) for inference.

**Text Normalization** is applied before vectorization to handle common character substitutions:

```
b!tch  →  bitch
h@te   →  hate
@ss    →  ass
```

---

## 🗄️ Database Schema

### `users`
| Column | Type | Description |
|---|---|---|
| `id` | INTEGER | Primary key |
| `username` | TEXT | Unique username |
| `password` | TEXT | Hashed password |
| `toxic_count` | INTEGER | Number of toxic comments submitted |
| `is_blocked` | BOOLEAN | Whether the user is blocked |

### `comments`
| Column | Type | Description |
|---|---|---|
| `id` | INTEGER | Primary key |
| `user_id` | INTEGER | Foreign key to users |
| `comment_text` | TEXT | The submitted comment |
| `is_toxic` | BOOLEAN | ML classification result |
| `timestamp` | DATETIME | Time of submission |

### `toxic_comments`
| Column | Type | Description |
|---|---|---|
| `id` | INTEGER | Primary key |
| `comment_id` | INTEGER | Foreign key to comments |
| `user_id` | INTEGER | Foreign key to users |
| `flagged_at` | DATETIME | Time the comment was flagged |

---

## 🔮 Future Improvements

- Build a React or HTML/CSS frontend
- Upgrade to a deep learning model (e.g., BERT) for higher accuracy
- Add multi-label toxicity detection (threat, insult, obscene, etc.)
- Switch to PostgreSQL for production scalability
- Add rate limiting and JWT-based authentication
- Deploy to cloud (AWS / GCP / Heroku)
