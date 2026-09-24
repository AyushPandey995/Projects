# 🌐 SocialSphere – Social Network Data Analysis & Recommendation System Using Pure Python

A pure Python project that loads, cleans, and analyses social network data, then builds two recommendation features on top of it: **"People You May Know"** and **"Pages You Might Like"**. It uses only the Python standard library: dictionaries, sets, loops, and the `json` module.

---

## 📌 Project Overview

Social platforms keep users engaged by suggesting new connections and content. This project simulates that experience end to end on a small social network dataset containing **users**, **friendships**, and **liked pages**.

The project is split into four tasks, each in its own notebook:

| Task   | Notebook        | What it does                                              |
| ------ | --------------- | --------------------------------------------------------- |
| Task 1 | `Task_1.ipynb`  | Load the JSON data and display users, friends, and pages  |
| Task 2 | `Task_2.ipynb`  | Clean the data: missing values, duplicates, inactive users |
| Task 3 | `Task_3.ipynb`  | "People You May Know" using mutual friends                |
| Task 4 | `Task_4.ipynb`  | "Pages You Might Like" using collaborative filtering      |

---

## 🎯 Objective

Apply core Python to a realistic data problem: read structured data, clean it, and turn user connections and interactions into ranked recommendations, without any external libraries.

---

## ✨ Key Features

- **Loaded and explored** JSON data with users, friend lists, and liked pages
- **Resolved IDs into names**, so friends and pages print in readable form
- **Cleaned** messy records: removed users with empty names, duplicate friend entries, inactive users, and duplicate pages
- **Built** a mutual-friends recommender that ranks suggestions by number of shared friends
- **Implemented** collaborative filtering to rank page recommendations by shared interests

---

## 🗂️ Data Format

Data is stored in JSON with two sections, `users` and `pages`:

```json
{
    "users": [
        {"id": 1, "name": "Amit",  "friends": [2, 3], "liked_pages": [101]},
        {"id": 2, "name": "Priya", "friends": [1, 4], "liked_pages": [102]},
        {"id": 3, "name": "Rahul", "friends": [1],    "liked_pages": [101, 103]},
        {"id": 4, "name": "Sara",  "friends": [2],    "liked_pages": [104]}
    ],
    "pages": [
        {"id": 101, "name": "Python Developers"},
        {"id": 102, "name": "Data Science Enthusiasts"},
        {"id": 103, "name": "AI & ML Community"},
        {"id": 104, "name": "Web Dev Hub"}
    ]
}
```

| Field         | Description                          |
| ------------- | ------------------------------------ |
| `id`          | Unique user or page ID               |
| `name`        | User or page name                    |
| `friends`     | List of friend user IDs              |
| `liked_pages` | List of page IDs the user has liked  |

---

## 🔄 Workflow

```text
Task_1_data.json
        │
        ▼
 Task 1: Load & display data
        │
        ▼
 Task 2: Clean data ──► Task_2_data_new.json
        │
        ▼
 Task 3: People You May Know   (mutual friends)
        │
        ▼
 Task 4: Pages You Might Like  (collaborative filtering)
```

---

## ⚙️ How Each Task Works

### 📥 Task 1: Load and Display Data

```python
def load_data(filename):
    with open(filename, "r") as f:
        return json.load(f)
```

`users_detail()` prints each user with their friends and liked pages, looking up IDs to show names (for example, `2 : Priya`), followed by the full list of pages.

### 🧹 Task 2: Clean the Data

The example dataset contains four data-quality problems, and the cleaning function fixes each:

| Problem                                    | Fix                                     |
| ------------------------------------------ | --------------------------------------- |
| User has an empty name                     | Remove the user                         |
| User has duplicate friend entries (`[2, 2]`) | Deduplicate with `set()`              |
| Inactive user (no friends, no liked pages) | Remove the user                         |
| Pages list has duplicate IDs               | Keep one page per ID                    |

```python
# Deduplicate friends
user['friends'] = list(set(user['friends']))

# Remove inactive users
data['users'] = [u for u in data['users'] if u['friends'] or u['liked_pages']]

# Deduplicate pages by ID
unique_pages = {}
for page in data['pages']:
    unique_pages[page['id']] = page
```

On the example dataset, the cleaning reduces **5 users to 3** and **5 pages to 4**. Where a page ID appears twice, the last entry is kept. The cleaned data is saved to `Task_2_data_new.json`.

### 🤝 Task 3: People You May Know

If two users are not friends but share mutual friends, each is suggested to the other. More mutual friends means a higher-priority suggestion.

**Example:** Amit is friends with Priya, and Priya is friends with Sara. Amit and Sara are not connected, so Sara is suggested to Amit through their mutual friend Priya.

**Algorithm:**
1. Build a lookup of each user's friends as a set.
2. For each friend of the target user, walk through that friend's friends.
3. Skip the target user and anyone already a direct friend.
4. Count how many times each candidate appears (the mutual friend count).
5. Sort candidates by count, highest first.

```python
for friend in direct_friends:
    for mutual in user_friends[friend]:
        if mutual != user_id and mutual not in direct_friends:
            suggestions[mutual] = suggestions.get(mutual, 0) + 1
```

### 📄 Task 4: Pages You Might Like

This uses **collaborative filtering**: if two people like the same thing, they may like the other things each one likes too.

**Example:** Amit and Priya both like AI World, so Priya's other page (Data Science Daily) is recommended to Amit, and Amit's other page (Python Hub) to Priya.

**Algorithm:**
1. Map every user to the set of pages they like.
2. For each other user, find the pages they share with the target user.
3. Give each page that the target user hasn't liked a score based on that overlap.
4. Sort pages by score, highest first.

```python
shared_pages = user_liked_pages.intersection(pages)
for page in pages:
    if page not in user_liked_pages:
        page_suggestions[page] = page_suggestions.get(page, 0) + len(shared_pages)
```

---

## 📈 Sample Results

Run on the sample dataset above:

| Feature               | Input   | Output           | Explanation                                              |
| --------------------- | ------- | ---------------- | -------------------------------------------------------- |
| People You May Know   | User 1  | `[4]`            | Amit and Sara share Priya as a mutual friend             |
| Pages You Might Like  | User 1  | `[103, 102, 104]` | Page 103 ranks first: Rahul shares Amit's page 101 interest |

---

## 🛠️ Tech Stack

- 🐍 **Python** (developed on 3.13), standard library only
- `json` module for reading and writing data
- **Jupyter Notebook** as the development environment

No external packages are required.

---

## 🚀 How to Run

**1. Clone the repository**

```bash
git clone https://github.com/<your-username>/SocialSphere.git
cd SocialSphere
```

**2. Install Jupyter (only needed to run the notebooks)**

```bash
pip install jupyter
```

**3. Run the notebooks in order**

```bash
jupyter notebook
```

Open `Task_1.ipynb` through `Task_4.ipynb` and run all cells in each. Keep the JSON data files in the same folder as the notebooks. `Task_3.ipynb` asks you to enter a user ID (for example, `1`).

---

## 📂 Project Structure

```text
SocialSphere/
│
├── Task_1.ipynb           # Load and display data
├── Task_2.ipynb           # Clean the data
├── Task_3.ipynb           # People You May Know
├── Task_4.ipynb           # Pages You Might Like
├── Task_1_data.json       # Clean sample dataset
├── Task_2_data.json       # Messy dataset used for cleaning
├── Task_2_data_new.json   # Cleaned output
└── README.md
```

---

## 🔭 Future Improvements

- Run the recommenders on the cleaned dataset, and remove references to deleted users from friend lists during cleaning
- Return names alongside IDs in the recommendation output
- Show the mutual friend count or shared-page score next to each suggestion
- Only recommend pages from users who share at least one liked page with the target user
- Support recommendations for all users in one run
- Add input validation for missing or malformed records
- Extend the friend suggestions to friends-of-friends-of-friends (second-degree connections)

---

## 👨‍💻 About

Built as part of my learning journey in **Data Science**, this project shows how core Python (dictionaries, sets, and JSON) is enough to clean real-world style data and power simple recommendation features.
