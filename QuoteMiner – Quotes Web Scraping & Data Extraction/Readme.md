# 💬 QuoteMiner – Quotes Web Scraping & Data Extraction

A Python web scraping project that extracts the complete quote collection from [Quotes to Scrape](https://quotes.toscrape.com/): **100 quotes across 10 pages**, along with each quote's author, tags, and author profile link. The data is structured into a clean dataset and exported as a CSV file, ready for analysis.

---

## 📌 Project Overview

Quotes to Scrape is a sandbox website built for practising web scraping. This project automates the collection of every quote on the site:

1. Inspect the website and identify its pagination pattern.
2. Download all 10 pages as local files.
3. Parse the saved HTML with BeautifulSoup to extract quote details.
4. Combine the results into a Pandas DataFrame and export to CSV.

Saving the raw pages first means the parsing logic can be refined and re-run offline, without sending repeated requests to the website.

---

## 🎯 Objective

Build a reliable, reusable scraping pipeline that turns unstructured web pages into a clean, analysis-ready dataset of quotes, authors, tags, and author profile links.

---

## 🔍 Scraping Strategy

After inspecting the website, the following was identified:

- The site contains **100 quotes** spread across **10 pages** (10 quotes per page).
- Page URLs follow a fixed pattern: `https://quotes.toscrape.com/page/{n}/`, where `n` runs from 1 to 10.
- Each quote sits inside a `<div class="quote">` block, with the text, author, tags, and author link in consistent child elements.

Looping through pages 1 to 10 covers the entire collection.

---

## 🔄 Workflow

```text
quotes.toscrape.com
        │
        ▼
 Inspect site & find URL pattern
        │
        ▼
 Loop pages 1–10 with Requests
        │
        ▼
 Save raw pages → Scraped_Data/Scraped_Page_{n}
        │
        ▼
 Parse HTML with BeautifulSoup
        │
        ▼
 Extract quote, author, tags, author link from each quote block
        │
        ▼
 Build Pandas DataFrame (100 rows)
        │
        ▼
 Export → Scraped_Data.csv
```

---

## 📊 Extracted Data

| Column              | Description                                             | Example                     |
| ------------------- | ------------------------------------------------------- | --------------------------- |
| `Quote`             | Full text of the quote                                  | “It is our choices, Harry…” |
| `Author`            | Name of the person who said the quote                   | J.K. Rowling                |
| `About_Quote`       | List of topic tags attached to the quote                | ['abilities', 'choices']    |
| `More_About_Author` | Relative link to the author's profile page on the site  | /author/J-K-Rowling         |

**Output:** `Scraped_Data.csv` with 100 rows and 4 columns.

**Sample rows:**

| Quote                                                | Author          | About_Quote                                  | More_About_Author        |
| ---------------------------------------------------- | --------------- | -------------------------------------------- | ------------------------ |
| “The world as we have created it is a process of…”   | Albert Einstein | ['change', 'deep-thoughts', 'thinking', 'world'] | /author/Albert-Einstein |
| “It is our choices, Harry, that show what we truly…” | J.K. Rowling    | ['abilities', 'choices']                     | /author/J-K-Rowling      |
| “Try not to become a man of success. Rather…”        | Albert Einstein | ['adulthood', 'success', 'value']            | /author/Albert-Einstein  |

---

## ⚙️ How It Works

### 1. Fetch the pages

```python
for i in range(1, 11):
    data = requests.get(f'https://quotes.toscrape.com/page/{i}/')
    with open(f'Scraped_Data/Scraped_Page_{i}', 'w', encoding='utf-8') as f:
        f.write(data.text)
```

### 2. Parse each quote

```python
soup = BeautifulSoup(content, 'html.parser')

for div in soup.find_all('div', class_='quote'):
    quote  = div.find('span', class_='text').text
    author = div.find('small', class_='author').text
    tags   = [tag.text for tag in div.find_all('a', class_='tag')]
    more_about_author_link = div.find('a')['href']
```

### 3. Build and export the dataset

```python
df = pd.DataFrame(data, columns=('Quote', 'Author', 'About_Quote', 'More_About_Author'))
df.to_csv("Scraped_Data.csv", index=False)
```

---

## 🛠️ Tech Stack

- 🐍 Python
- **Requests**: sending HTTP requests and downloading pages
- **BeautifulSoup (bs4)**: parsing HTML and extracting data
- **Pandas**: structuring and exporting the dataset
- **Jupyter Notebook**: development environment

---

## 🚀 How to Run

**1. Clone the repository**

```bash
git clone https://github.com/<your-username>/QuoteMiner.git
cd QuoteMiner
```

**2. Install dependencies**

```bash
pip install requests beautifulsoup4 pandas jupyter
```

**3. Create the folder for the raw pages**

```bash
mkdir Scraped_Data
```

**4. Open and run the notebook**

```bash
jupyter notebook Quotes_to_Scrape.ipynb
```

Run all cells in order. The 10 raw pages are saved to `Scraped_Data/`, and the final dataset is written to `Scraped_Data.csv`.

---

## 📂 Project Structure

```text
QuoteMiner/
│
├── Quotes_to_Scrape.ipynb   # Scraping and parsing notebook
├── Scraped_Data/            # Raw pages (Scraped_Page_1 … Scraped_Page_10)
├── Scraped_Data.csv         # Final extracted dataset
└── README.md
```

---

## 🔭 Future Improvements

- Rename `About_Quote` to `Tags` and split tags into separate columns for easier analysis
- Convert `More_About_Author` into full URLs and scrape each author's profile page for birth date, birthplace, and biography
- Analyse the most frequent authors and most popular tags
- Add error handling, retries, and request delays for more robust scraping
- Refactor the notebook into a reusable Python script or module
- Store the data in a database (SQLite or PostgreSQL)

---

## ⚠️ Disclaimer

Quotes to Scrape is a sandbox site created specifically for practising web scraping. When scraping real websites, always check their `robots.txt` and terms of service first.

---

## 👨‍💻 About

Built as part of my learning journey in **Data Science**, this project covers the end-to-end process of collecting raw web data and converting it into a clean, structured dataset.
