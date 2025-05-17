# 📊 Project: Data Extraction Utilities

> A collection of two utility scripts used for extracting and saving data in different formats—one for fetching and parsing AMFI mutual fund NAV data, and another for scraping OLX car cover listings. Both were developed as part of a recruitment exercise.

---

## 🚀 Table of Contents

1. [Overview](#overview)
2. [Scripts](#scripts)

   * [nav\_extract.sh](#nav_extractsh)
   * [olx.py](#olxpy)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Output Files](#output-files)
7. [Folder Structure](#folder-structure)
8. [Contributing](#contributing)
9. [License](#license)
10. [Contact](#contact)

---

## 📝 Overview

This repository contains two standalone scripts:

* **nav\_extract.sh**: A Bash script that downloads NAV data from AMFI, extracts scheme names and Net Asset Values, and writes them into a TSV file.
* **olx.py**: A Python (Selenium-based) scraper that visits OLX India, collects listings for car covers, and saves the data as both CSV and JSON.

These tools demonstrate proficiency in shell scripting, text processing, web scraping with Selenium, and data serialization.

---

## 🛠️ Scripts

### 1. nav\_extract.sh

A lightweight Bash utility to fetch mutual fund data.

```bash
#!/usr/bin/env bash
# nav_extract.sh — Download NAVAll.txt and extract Scheme Name + NAV as TSV

URL="https://www.amfiindia.com/spages/NAVAll.txt"
OUTFILE="nav.tsv"

curl -s "$URL" \
  | tail -n +2 \
  | cut -d\; -f3,4 \
  | tr ';' '\t' \
  > "$OUTFILE"

echo "Extracted $(wc -l < "$OUTFILE") entries to $OUTFILE"
```

* **Functionality**:

  * Downloads the full NAV listing.
  * Skips the header row.
  * Pulls fields *3* (Scheme Name) and *4* (NAV) delimited by `;`.
  * Converts `;` to tab characters (`\t`) and saves as `nav.tsv`.

### 2. olx.py

A robust Python scraper for OLX car cover listings using Selenium.

```python
# olx.py — Scrapes OLX India for car cover listings, saves CSV & JSON
import time, json, csv, sys, os
from selenium import webdriver
# ... rest of script ...
```

* **Functionality**:

  * Headless Chrome via `webdriver-manager`.
  * Visits multiple pages (configurable count).
  * Takes screenshots & saves HTML source per page.
  * Uses multiple XPath strategies to locate listing elements.
  * Extracts **title**, **price**, **location**, **date**, **link**, and **image URL**.
  * Outputs data into `car_covers_olx.csv` and `car_covers_olx.json`.

---

## 📋 Prerequisites

1. **General**

   * Git (to clone the repo)
   * Internet access
   * Sufficient disk space for output files and screenshots

2. **For `nav_extract.sh`**

   * **Bash** (v4+)
   * **curl**
   * **coreutils** (for `cut`, `tr`, `wc`)

3. **For `olx.py`**

   * **Python** 3.7+
   * **pip**
   * **Google Chrome** (latest stable)

   Install Python dependencies:

   ```bash
   pip install selenium webdriver-manager
   ```

---

## 🏗️ Installation

Clone this repository:

```bash
git clone https://github.com/yourusername/data-extract-tools.git
cd data-extract-tools
```

---

## ▶️ Usage

### 1. Running the NAV Extractor

```bash
chmod +x nav_extract.sh
./nav_extract.sh
```

* **Output**: `nav.tsv` containing `<Scheme Name>\t<NAV>` per line.

### 2. Running the OLX Scraper

```bash
python olx.py [pages]
```

* **Arguments**:

  * `pages` (optional): Number of pages to scrape (default: 3).

* **First Run**: Displays setup instructions and creates `setup_complete.txt`.

* **Outputs**:

  * `olx_page_<n>.png` (screenshots)
  * `olx_page_<n>.html` (HTML source)
  * `car_covers_olx.csv`
  * `car_covers_olx.json`

---

## 📂 Folder Structure

```
FULL-STACK-AI-ENGINEER/      # Project root
├── Outputs/               # All generated data files and snapshots
│   ├── car_covers_olx.csv    # Scraped OLX data as CSV
│   ├── car_covers_olx.json   # Scraped OLX data as JSON
│   ├── nav.tsv               # Extracted NAV data (TSV)
│   ├── olx_page_1.html       # Saved HTML of page 1
│   ├── olx_page_1.png        # Screenshot of page 1
│   ├── olx_page_2.html       # Saved HTML of page 2
│   ├── olx_page_2.png        # Screenshot of page 2
│   ├── olx_page_3.html       # Saved HTML of page 3
│   └── olx_page_3.png        # Screenshot of page 3
├── nav_extract.sh         # Bash script for NAV extraction
├── olx.py                 # Python scraper for OLX car covers
├── README.md              # Project documentation
└── setup_complete.txt     # Created on first run of olx.py
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Please:

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/foo`)
3. Commit changes (`git commit -m "feat: add foo"`)
4. Push (`git push origin feature/foo`)
5. Open a pull request

---

## 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 📬 Contact

**Piyush Kumar** • [piyushkarn96@gmail.com](mailto:piyushkarn96@gmail.com) • [GitHub @Piyush-Karn](https://github.com/Piyush-Karn)

> *Empowering data extraction, one script at a time!*
