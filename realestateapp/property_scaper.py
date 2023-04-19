import asyncio
# from pyppeteer import launch
from bs4 import BeautifulSoup
# from pyppeteer.errors import TimeoutError
from pprint import pprint
import json
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import os

# url = 'https://www.realtor.com/realestateandhomes-detail/800-FM-518-Rd_Kemah_TX_77565_M97022-84297'
url = 'https://www.realtor.com/realestateandhomes-detail/1225-Lawrence-Rd_Kemah_TX_77565_M70417-96158'


async def main(url):
    browser = await launch(headless=True)
    page = await browser.newPage()
    try:
        await page.goto(url, timeout=5000)  # load the page and wait up to 5 seconds
    except TimeoutError:
        content = await page.content()  # get the HTML content of the partially-loaded page
        # content = await page.
        # print('TimeoutError occurred, but got content:', content)
    else:
        content = await page.content()  # get the HTML content of the fully-loaded page
        # print('Content of the page:', content)
    await browser.close()
    soup = BeautifulSoup(content, 'html.parser')
    storage = {}
    scripts = soup.find_all('script')
    for script_tag in scripts:
        if 'id' in script_tag.attrs and script_tag.attrs['id'] == '__NEXT_DATA__':
            page = json.loads(script_tag.text)
            break
    for feature in page['props']['pageProps']['property']['details']:
        storage[feature['category']] = feature['text']
    pprint(storage)
    await browser.close()


# def run(url):
# asyncio.get_event_loop().run_until_complete(main(url))


def scrape_zillow(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),
                              chrome_options=chrome_options)

    driver.get(url)
    try:
        element_present = EC.presence_of_element_located((By.TAG_NAME, 'body'))
        WebDriverWait(driver, 3000).until(element_present)
    except TimeoutException:
        print(f'Timeout reached after 5000 seconds.')
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    storage = {}
    scripts = soup.find_all('script')
    for script_tag in scripts:
        if 'id' in script_tag.attrs and script_tag.attrs['id'] == '__NEXT_DATA__':
            page = json.loads(script_tag.text)
            for feature in page['props']['pageProps']['property']['details']:
                # storage[feature['category']] = feature['text']
                num = len(feature['text']) // 2
                storage[feature['category']] = []
                storage[feature['category']].append(feature['text'][:num + 1])
                storage[feature['category']].append(feature['text'][num + 1:])
            pprint(storage)
            # print(content)
            break
    driver.quit()
    return storage
