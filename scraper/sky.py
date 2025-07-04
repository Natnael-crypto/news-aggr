import asyncio
from datetime import datetime
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import csv

BASE_URL = "https://news.sky.com/"

async def scrape_sky_news_cards():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(BASE_URL, timeout=60000)
        await page.wait_for_selector(".ui-story-wrap", timeout=15000)

        html = await page.content()
        soup = BeautifulSoup(html, "html.parser")

        articles = []
        seen_urls = set()

        for card in soup.select(".ui-story-wrap"):
            # Extract URL and title
            a_tag = card.select_one(".ui-story-headline")
            if not a_tag:
                continue

            relative_url = a_tag.get("href")
            url = f"https://news.sky.com{relative_url}" if relative_url.startswith("/") else relative_url
            if url in seen_urls:
                continue
            seen_urls.add(url)

            title = a_tag.get_text(strip=True)

            # Extract image
            img_tag = card.select_one("picture img")
            image_url = img_tag["src"] if img_tag and img_tag.has_attr("src") else ""

            articles.append({
                "title": title,
                "url": url,
                "image_url": image_url,
                "scraped_at": datetime.utcnow(),
                "source":"sky"
            })

        await browser.close()
        return articles

# # Save to CSV
# if __name__ == "__main__":
#     articles = asyncio.run(scrape_sky_news_cards())

#     for i, article in enumerate(articles):
#         print(f"\n🔹 Article {i}")
#         print(f"Title     : {article['title']}")
#         print(f"URL       : {article['url']}")
#         print(f"Image URL : {article['image_url']}")

#     with open("sky_news_articles.csv", "w", newline="", encoding="utf-8") as f:
#         writer = csv.DictWriter(f, fieldnames=["title", "url", "image_url","scraped_at"])
#         writer.writeheader()
#         writer.writerows(articles)

#     print(f"\n✅ Saved {len(articles)} Sky News articles to 'sky_news_articles.csv'")
