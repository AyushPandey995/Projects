📚 BookInsight – Book Data Extraction using Web Scraping

A Python web scraping project that extracts the complete book catalogue from Books to Scrape: 1,000 books across 50 pages. The data is cleaned into a structured dataset and exported as a CSV file, ready for analysis.

📌 Project Overview

Books to Scrape is a sandbox website built for practising web scraping. This project automates the collection of every book listing on the site:

Inspect the website and identify its pagination pattern.
Download all 50 catalogue pages as local HTML files.
Parse the saved HTML with BeautifulSoup to extract book details.
Combine the results into a Pandas DataFrame and export to CSV.

Saving the raw HTML first means the parsing logic can be refined and re-run offline, without sending repeated requests to the website.

🎯 Objective

Build a reliable, reusable scraping pipeline that turns unstructured web pages into a clean, analysis-ready dataset of book titles, prices, and ratings.

🔍 Scraping Strategy

After inspecting the website, the following was identified:

The catalogue contains 1,000 books spread across 50 pages (20 books per page).
Page URLs follow a fixed pattern: https://books.toscrape.com/catalogue/page-{n}.html, where n runs from 1 to 50.
Each book sits inside an <article> tag, so title, price, and rating can be located with consistent selectors.

Looping through pages 1 to 50 covers the entire catalogue.

🔄 Workflow
text
books.toscrape.com
        │
        ▼
 Inspect site & find URL pattern
        │
        ▼
 Loop pages 1–50 with Requests
        │
        ▼
 Save raw pages → Scraped_Data/Scraped_Page_{n}.html
        │
        ▼
 Parse HTML with BeautifulSoup
        │
        ▼
 Extract title, price, rating from each <article>
        │
        ▼
 Build Pandas DataFrame (1,000 rows)
        │
        ▼
 Export → Scraped_Data_1.csv
📊 Extracted Data
Column	Description	Example
Book_Title	Full title of the book	A Light in the Attic
Price	Price in pounds, with the £ symbol at the end	51.77£
Rating(Out Of 5)	Star rating stored as a word (One to Five)	Three

Output: Scraped_Data_1.csv with 1,000 rows and 3 columns.

Sample rows:

Book_Title	Price	Rating(Out Of 5)
A Light in the Attic	51.77£	Three
Tipping the Velvet	53.74£	One
Soumission	50.10£	One
Sharp Objects	47.82£	Four
Sapiens: A Brief History of Humankind	54.23£	Five
⚙️ How It Works
1. Fetch the pages
python
for i in range(1, 51):
    data = requests.get(f'https://books.toscrape.com/catalogue/page-{i}.html')
    with open(f'Scraped_Data/Scraped_Page_{i}.html', 'w', encoding='utf-8') as f:
        f.write(data.text)
2. Parse each book
python
soup = BeautifulSoup(content, "html.parser")

for article in soup.find_all('article'):
    title  = article.find('h3').find('a')['title']
    price  = article.select_one('p.price_color').text.split('£')[1]
    rating = article.find('p')['class'][1]

The full title is read from the link's title attribute, because the visible text on the page is truncated for long titles.

3. Build and export the dataset
python
df = pd.DataFrame(data, columns=['Book_Title', 'Price', 'Rating(Out Of 5)'])
df.to_csv("Scraped_Data_1.csv", index=False)
🛠️ Tech Stack
🐍 Python
Requests: sending HTTP requests and downloading pages
BeautifulSoup (bs4): parsing HTML and extracting data
Pandas: structuring and exporting the dataset
Jupyter Notebook: development environment
🚀 How to Run

1. Clone the repository

bash
git clone https://github.com/<your-username>/BookInsight.git
cd BookInsight

2. Install dependencies

bash
pip install requests beautifulsoup4 pandas jupyter

3. Create the folder for the raw pages

bash
mkdir Scraped_Data

4. Open and run the notebook

bash
jupyter notebook Books_to_Scrape.ipynb

Run all cells in order. The 50 HTML pages are saved to Scraped_Data/, and the final dataset is written to Scraped_Data_1.csv.

📂 Project Structure
text
BookInsight/
│
├── Books_to_Scrape.ipynb    # Scraping and parsing notebook
├── Scraped_Data/            # Raw HTML pages (Scraped_Page_1.html … Scraped_Page_50.html)
├── Scraped_Data_1.csv       # Final extracted dataset
└── README.md
🔭 Future Improvements
Convert Price to a numeric column and Rating to integers (1–5) for direct analysis
Extract more fields from each book's detail page: category, availability, UPC, and description
Add error handling, retries, and request delays for more robust scraping
Refactor the notebook into a reusable Python script or module
Add exploratory analysis and visualizations, such as price distribution and rating trends
Store the data in a database (SQLite or PostgreSQL)
⚠️ Disclaimer

Books to Scrape is a sandbox site created specifically for practising web scraping. When scraping real websites, always check their robots.txt and terms of service first.
