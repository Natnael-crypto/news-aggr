# scrapers/cnn.py

import asyncio
import csv
import os
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
from datetime import datetime
import hashlib
from bs4 import BeautifulSoup

CNN_URL = "https://edition.cnn.com/"


async def scrape_cnn_cards():
    articles = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True,slow_mo=1000)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(CNN_URL,wait_until="domcontentloaded", timeout=60000)

        cards = await page.query_selector_all('[data-component-name="card"]')

        for card in cards:
            try:
                title_el = await card.query_selector(".container__headline-text")
                title = await title_el.inner_text() if title_el else ""

                link_el = await card.query_selector("a.container__link")
                href = await link_el.get_attribute("href") if link_el else ""
                if href and href.startswith("/"):
                    url = f"https://www.cnn.com{href}"
                else:
                    url = href

                image_el = await card.query_selector("img.image__dam-img")
                image_url = await image_el.get_attribute("src") if image_el else ""

                content_hash = hashlib.sha256((title or url or "").encode()).hexdigest()

                if title and url:
                    article = {
                        "title": title.strip(),
                        "url": url.strip(),
                        "image_url": image_url,
                        "scraped_at": datetime.utcnow(),
                        "source":"cnn"

                    }
                    articles.append(article)

            except Exception as e:
                print(f"[ERROR] Failed to parse one card: {e}")

        await browser.close()

    return articles


async def extract_cnn_article(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, slow_mo=1000)
        page = await browser.new_page()
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)

        try:
            await page.wait_for_selector('.article__main', timeout=15000, state='attached')
        except PlaywrightTimeout:
            print(f"[WARN] .article__main not found for URL: {url}")
            await browser.close()
            return ""

        html = await page.content()
        soup = BeautifulSoup(html, 'html.parser')

        article_main = soup.select_one('.article__main')
        if not article_main:
            print("[INFO] .article__main missing in parsed HTML.")
            await browser.close()
            return ""

        primary_video = article_main.select_one('.image__dam-img')
        primary_img = primary_video['src'] if primary_video else None

        await browser.close()
        return primary_img




async def cnnMain():
    articles = await scrape_cnn_cards()
    cleaned_articles = []
    for idx, article in enumerate(articles):
        if article["image_url"] == "":
            image = await extract_cnn_article(article["url"])
            if not image:
                # print(f"Skipping article {idx} - no image.")
                continue
            article["image_url"] = image
            # print(f"\n🔹 Article {idx} image : {image}")
            # print(f"Title     : {article['title']}")
            # print(f"URL       : {article['url']}")

        cleaned_articles.append(article)

    return cleaned_articles




