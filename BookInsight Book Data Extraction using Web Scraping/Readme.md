# 📚 BookInsight – Book Data Extraction using Web Scraping

A Python web scraping project that extracts the complete book catalogue from [Books to Scrape](https://books.toscrape.com/): **1,000 books across 50 pages**. The data is cleaned into a structured dataset and exported as a CSV file, ready for analysis.

---

## 📌 Project Overview

Books to Scrape is a sandbox website built for practising web scraping. This project automates the collection of every book listing on the site:

1. Inspect the website and identify its pagination pattern.
2. Download all 50 catalogue pages as local HTML files.
3. Parse the saved HTML with BeautifulSoup to extract book details.
4. Combine the results into a Pandas DataFrame and export to CSV.

Saving the raw HTML first means the parsing logic can be refined and re-run offline, without sending repeated requests to the website.

---

## 🎯 Objective

Build a reliable, reusable scraping pipeline that turns unstructured web pages into a clean, analysis-ready dataset of book titles, prices, and ratings.

---

## 🔍 Scraping Strategy

After inspecting the website, the following was identified:

- The catalogue contains **1,000 books** spread across **50 pages** (20 books per page).
- Page URLs follow a fixed pattern: `https://books.toscrape.com/catalogue/page-{n}.html`, where `n` runs from 1 to 50.
- Each book sits inside an `<article>` tag, so title, price, and rating can be located with consistent selectors.

Looping through pages 1 to 50 covers the entire catalogue.

---

## 🔄 Workflow

```text
books.toscrape.com
        │
        ▼
 Inspect site & find URL pattern
        │
        ▼
 Loop pages 1–50 with Requests
        │
        ▼
