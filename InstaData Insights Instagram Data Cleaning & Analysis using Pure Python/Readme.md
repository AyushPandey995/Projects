# 📸 InstaData Insights – Instagram Data Cleaning & Analysis using Pure Python

A pure Python project that cleans and analyses manually collected Instagram profile data. It converts **107 raw, unstructured profile records** into a clean JSON dataset, then answers key questions about posts, followers, followings, and profile categories, using no external libraries.

---

## 📌 Project Overview

The Instagram user data was **collected manually** and saved as plain text. Each profile is a block of lines (username, post count, follower count, following count, display name, category, and bio), and profiles are separated by blank lines.

This project:

1. Reads the raw text file and splits it into individual profile records.
2. Parses each record into a structured dictionary, converting counts like `9.8K` into real integers.
3. Handles profiles with missing category or bio information.
4. Exports the cleaned data to `data.json`.
5. Analyses the data to answer five questions.

Development was done on a small sample (`initialdata.txt`) first, and the final logic was then applied to the full dataset (`finaldata.txt`).

---

## 🎯 Objective

Turn raw, manually collected Instagram data into a structured dataset and extract insights using **only core Python** (file handling, string operations, loops, dictionaries, sets, and the `json` module).

---

## ❓ Questions Answered

1. Who has the maximum number of posts?
2. Who has the maximum number of followers?
3. Who follows the maximum number of people?
4. How many profile categories (Digital creator, Nonprofit organization, etc.) exist?
5. How many people are in the dataset?

---

## 📈 Results

Computed on the full dataset of **107 profiles**:

| Question                  | Answer                                          |
| ------------------------- | ----------------------------------------------- |
| Most posts                | `startuphub_blr` (Startup Hub Bangalore): 2,300 |
| Most followers            | `_anujsinghal` (Anuj Singhal): 681,000          |
| Follows the most accounts | `bangalore_tech_bro` (Rahul \| HSR Hustler): 890 |
| Unique profile categories | 34                                              |
| Total profiles            | 107                                             |

---

## 🔄 Workflow

```text
finaldata.txt (raw text)
        │
        ▼
 Read file & split on blank lines
        │
        ▼
 Filter out empty chunks (107 profiles)
        │
        ▼
 Parse each chunk with chunk_detail()
   ├─ username, name
   ├─ posts, followers, followings (K / M → integers)
   └─ category & bio (defaults if missing)
        │
        ▼
 List of dictionaries
        │
        ├──► Export → data.json
        │
        ▼
 Analysis with loops & sets
   ├─ Max posts
   ├─ Max followers
   ├─ Max followings
   ├─ Unique categories
   └─ Total people
```

---

## 🗂️ Data Format

**Raw input:** one profile per block, separated by a blank line.

```text
<username>
<N> posts
<N or N.nK/M> followers
<N> following
<display name>
<category>
<bio line(s)>
```

**Cleaned output:** each profile becomes a dictionary with these fields:

| Field              | Type    | Description                                   |
| ------------------ | ------- | --------------------------------------------- |
| `User_name`        | string  | Instagram handle                              |
| `No_of_post`       | integer | Number of posts                               |
| `No_of_followers`  | integer | Followers (K/M abbreviations expanded)        |
| `No_of_followings` | integer | Accounts followed (K/M abbreviations expanded) |
| `Name`             | string  | Display name                                  |
| `Type_of_profile`  | string  | Profile category (`Unknown` if missing)       |
| `Bio`              | string  | Bio text (`Empty` if missing)                 |

**Sample record from `data.json`:**

```json
{
    "User_name": "techie_koramangala",
    "No_of_post": 420,
    "No_of_followers": 9800,
    "No_of_followings": 310,
    "Name": "Arjun M.",
    "Type_of_profile": "Software Engineer",
    "Bio": "💻 Full-stack @ SaaS startup\n☕ Working from cafes in Koramangala\ngithub.com/arjunmakes"
}
```

---

## ⚙️ How It Works

### 1. Read and split the raw data

```python
with open("finaldata.txt", "r", encoding="utf-8") as f:
    data = f.read()

chunks = data.split("\n\n")
chunks = [c for c in chunks if len(c) > 3]
```

### 2. Parse each profile

`chunk_detail()` splits a chunk into lines, extracts each field, and converts abbreviated counts:

```python
if "K" in sep_chunk[2]:
    no_of_followers = int(no_of_followers * 1000)
elif "M" in sep_chunk[2]:
    no_of_followers = int(no_of_followers * 1000000)
```

Profiles with no category or bio fall back to `"Unknown"` and `"Empty"`.

```python
detail = [chunk_detail(chunk) for chunk in chunks]
```

### 3. Export to JSON

```python
with open("data.json", "w") as f:
    f.write(json.dumps(detail, indent=4))
```

### 4. Analyse

Each question is answered with a simple loop that tracks the running maximum, and a `set` collects the unique categories:

```python
category = set()
for chunk in detail:
    category.add(chunk["Type_of_profile"])
```

---

## 🛠️ Tech Stack

- 🐍 **Python 3.12+**, standard library only
- `json` module for exporting data
- **Jupyter Notebook** as the development environment

No external packages are required.

---

## 🚀 How to Run

**1. Clone the repository**

```bash
git clone https://github.com/<your-username>/InstaData-Insights.git
cd InstaData-Insights
```

**2. Install Jupyter (only needed to run the notebook)**

```bash
pip install jupyter
```

**3. Open and run the notebook**

```bash
jupyter notebook Task_and_solution.ipynb
```

Run all cells in order. Make sure `finaldata.txt` is in the same folder as the notebook. The cleaned dataset is written to `data.json`.

---

## 📂 Project Structure

```text
InstaData-Insights/
│
├── Task_and_solution.ipynb   # Cleaning and analysis notebook
├── initialdata.txt           # Small sample used to develop the parsing logic
├── finaldata.txt             # Full raw dataset (107 profiles)
├── data.json                 # Cleaned, structured output
└── README.md
```

---

## 🔭 Future Improvements

- Export the cleaned data to CSV and analyse it with Pandas
- Rank the top 10 accounts by followers, posts, and followings instead of only the maximum
- Show the number of profiles in each category
- Calculate the follower-to-following ratio for each profile
- Add data validation for malformed or incomplete records
- Visualize the results with charts

---

## 👨‍💻 About

Built as part of my learning journey in **Data Science**, this project shows how raw, manually collected text data can be cleaned, structured, and analysed using core Python alone.
