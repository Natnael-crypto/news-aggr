import asyncio
import csv
from datetime import datetime
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

BASE_URL = "https://www.bbc.com"

async def scrape_bbc_cards():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(BASE_URL + "/news", wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_selector('a[data-testid="internal-link"]', timeout=15000)

        html = await page.content()
        await browser.close()

        soup = BeautifulSoup(html, "html.parser")
        articles = []

        for a_tag in soup.select('a[data-testid="internal-link"]'):
            title_tag = a_tag.select_one('[data-testid="card-headline"]')
            img_tag = a_tag.select_one('img')
            description_tag = a_tag.select_one('[data-testid="card-description"]')

            title = title_tag.get_text(strip=True) if title_tag else ""
            url = BASE_URL + a_tag.get("href", "")
            image_url = img_tag.get("src") if img_tag else ""

            if title and image_url:
                articles.append({
                    "title": title,
                    "url": url,
                    "image_url": image_url,
                    "scraped_at": datetime.utcnow(),
                    "source":"bbc"
                })

        return articles


# if __name__ == "__main__":
#     articles = asyncio.run(scrape_bbc_cards())

#     # Print to console
#     for i, article in enumerate(articles):
#         print(f"\n🔹 Article {i}")
#         print(f"Title     : {article['title']}")
#         print(f"URL       : {article['url']}")
#         print(f"Image URL : {article['image_url']}")

#     # Write to CSV file
#     with open("bbc_articles.csv", mode="w", newline="", encoding="utf-8") as file:
#         writer = csv.DictWriter(file, fieldnames=["title", "url", "image_url","scraped_at"])
#         writer.writeheader()
#         writer.writerows(articles)

#     print(f"\n✅ Saved {len(articles)} articles to 'bbc_articles.csv'")