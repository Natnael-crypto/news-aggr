from datetime import datetime
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import asyncio
import csv

BASE_URL = "https://www.theguardian.com/world"

async def scrape_guardian_cards():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(BASE_URL, timeout=60000)
        await page.wait_for_selector(".dcr-199p3eh", timeout=15000)

        html = await page.content()
        soup = BeautifulSoup(html, "html.parser")

        articles = []
        seen_urls = set()

        for card in soup.select(".dcr-199p3eh"):
            a_tag = card.find("a", href=True)
            if not a_tag:
                continue

            relative_url = a_tag["href"]
            if relative_url.startswith("/"):
                url = f"https://www.theguardian.com{relative_url}"
            else:
                url = relative_url

            if url in seen_urls:
                continue
            seen_urls.add(url)

            title_tag = card.select_one("h3 span")
            title = title_tag.get_text(strip=True) if title_tag else "No title"

            img_tag = card.select_one("picture img")
            image_url = img_tag["src"] if img_tag and img_tag.has_attr("src") else ""

            articles.append({
                "title": title,
                "url": url,
                "image_url": image_url,
                "scraped_at": datetime.utcnow(),
                "source":"guardian"

            })

        await browser.close()
        return articles

# if __name__ == "__main__":
#     articles = asyncio.run(scrape_guardian_cards())

#     for i, article in enumerate(articles):
#         print(f"\n🔹 Article {i}")
#         print(f"Title     : {article['title']}")
#         print(f"URL       : {article['url']}")
#         print(f"Image URL : {article['image_url']}")

#     with open("guardian_articles.csv", "w", newline="", encoding="utf-8") as f:
#         writer = csv.DictWriter(f, fieldnames=["title", "url", "image_url","scraped_at"])
#         writer.writeheader()
#         writer.writerows(articles)

#     print(f"\n✅ Saved {len(articles)} Guardian articles to 'guardian_articles.csv'")
