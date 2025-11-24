# Webscrapper_Buddy

📘 Webscrapper Buddy
Automated Web Scraper using Selenium (ChromeDriver) + BeautifulSoup + Ollama (LLM Parser) + Streamlit UI

🚀 Overview
Webscrapper Buddy is an AI-powered web scraping tool that:
Uses Selenium to extract dynamic website data
Collects HTML using DOM chunking
Parses extracted content with an LLM (via Ollama)
Converts output into structured text (tables, lists, descriptions)
Allows downloading data in Excel (.xlsx) or PDF formats
Provides a simple Streamlit interface for input and output
This tool is useful for scraping course pages, product pages, job listings, or any website that requires AI-based parsing.

🧠 Key Features
🔹 1. Automated Selenium Scraping
Uses ChromeDriver
Bypasses heavy HTML, JS-rendered pages
Extracts DOM elements safely

🔹 2. AI Parsing (via Ollama)
Uses your local LLM model (like llama3, mistral, etc.)
Breaks DOM into chunks for accurate parsing
Produces structured JSON-like responses

🔹 3. Streamlit Web App
Enter URL
Scrape page
Parse scraped content
Show readable output
Download to Excel / PDF

🔹 4. Export Options

Built-in support for:
✔ Excel (.xlsx)
✔ PDF (generated using Matplotlib table rendering)
