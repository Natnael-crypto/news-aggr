

import asyncio
import random
from scraper.bbc import scrape_bbc_cards
from scraper.cnn import cnnMain
from scraper.guardian import scrape_guardian_cards
from scraper.sky import scrape_sky_news_cards



def scraper():
    bbc=asyncio.run(scrape_bbc_cards())
    cnn=asyncio.run(cnnMain())
    guardian=asyncio.run(scrape_guardian_cards())
    sky=asyncio.run(scrape_sky_news_cards())

    print(f"Scarped {len(bbc)} from BBC {len(cnn)} from CNN {len(guardian)} from GUARDIAN {len(sky)} from SKY New")

    all =bbc+cnn+guardian+sky

    random.shuffle(all)
    
    return all