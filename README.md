
# 📰 Real-Time News Aggregator

A Python web application that scrapes the latest articles from multiple news websites (BBC, CNN, Guardian, Sky News) and stores them in a database. The app includes a scheduler to scrape data periodically and serves it via a RESTful API.

---

## 📦 Features

- 🌐 Scrapes real-time articles using **Playwright**
- 🗃 Stores news in a **SQL database** using **SQLAlchemy**
- 🔄 Automatically updates news every 24 hours using **APScheduler**
- 🛠 Built with **Flask** for modularity and extensibility

---

## 🧰 Tech Stack

- **Backend**: Flask, Flask-SQLAlchemy
- **Scraping**: Playwright (headless browser automation)
- **Database**: MySQL
- **ORM**: SQLAlchemy
- **Scheduler**: APScheduler
- **Environment**: Python-dotenv

---

## ⚙️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/Natnael-crypto/news-aggr
cd news-aggr
````

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up `.env` file

Create a `.env` file in the project root:

```env
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/news
```

> You can use PostgreSQL or SQLite by adjusting the `DATABASE_URL`.

### 4. Run Playwright install

```bash
playwright install
```

### 5. Run the app

```bash
python app.py
```

The app will:

* Run the scraper once on startup
* Schedule it to run every 24 hours
* Expose data via a Flask app

---

## 📥 Example Response (from API endpoint)

```json
{
  "articles": [
    {
      "id": 1,
      "title": "Breaking: Major Update from BBC",
      "url": "https://bbc.com/news/...",
      "image_url": "https://...",
      "source": "bbc",
      "scraped_at": "2025-07-05T11:30:00"
    }
  ],
  "total": 120,
  "pages": 12,
  "current_page": 1
}
```

---

## 🧪 Future Improvements

* Filter news by keywords or date
* Full-text search functionality
* Add authentication and admin dashboard