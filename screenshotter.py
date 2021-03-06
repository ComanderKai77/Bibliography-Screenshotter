import asyncio
import os
from pyppeteer import launch
import re
import requests
import sys
import time

async def init():
    global browser
    global page

    browser = await launch(headless=True, args=["--no-sandbox"])
    page = await browser.newPage()

async def take_screenshot(url, path):
    global page

    # Increase viewport size to force lazy images to load
    await change_viewport_size(1920, 100000)
    await page.goto(url)

    # Change wait time when something isn't loading
    await page.waitFor(1000)
    await change_viewport_size(1920, 1080)

    # Change wait time when something isn't loading
    await page.waitFor(4000)
    await page.screenshot({"path": path, "fullPage": True, "waitUntil" : "networkidle0"})

async def change_viewport_size(width, height):
    await page.setViewport({
        "width": width,
        "height": height
    })

async def scroll_to_end():
    await page.evaluate("""() => {
        return {
            scroll: window.scrollTo(0, document.body.scrollHeight)
        }
    }""")

async def close():
    global browser

    await browser.close()

def read_file(path):
    with open(path, "r") as file:
        return file.read().replace("\n", "")

def get_url_list(literature):
    return re.findall('url\s*=\s*"?\s*{\s*(\S*)\s*}\s*"?\s*', literature, re.IGNORECASE)

def generate_filename(url, type):
    filename = re.sub("[^\w\ ]", "_", url)
    while "__" in filename:
        filename = filename.replace("__", "_")

    return "screenshots/{}.{}".format(filename, type)

def download_pdf(url):
    print("Downloading PDF from ", url)
    request = requests.get(url, allow_redirects=True)
    open(generate_filename(url, "pdf"), "wb").write(request.content)

async def prepare_screenshot(url):
    print("Taking screenshot from ", url)
    await take_screenshot(url, generate_filename(url, "png"))

async def main(literature_file):
    start_time = time.time()
    await init()

    file = read_file(literature_file)
    url_list = get_url_list(file)
    print("URL entries: ", len(url_list))

    for url in url_list:
        if url.endswith(".pdf"):
            download_pdf(url)
        else:
            await prepare_screenshot(url)

    await close()
    print("Took: {:.0f}s for {} elements".format(time.time() - start_time, len(url_list)))

if __name__ == "__main__":
    if sys.version_info[0] < 3 or (sys.version_info[0] == 3 and sys.version_info[1] < 4):
        raise Exception("This software requires Python 3.4 or greater")

    if len(sys.argv) < 2:
        raise Exception("Missing argument: Literature file")

    if os.path.exists("screenshots"):
        raise Exception("'screenshots' folder already exists")
    os.mkdir("screenshots")

    asyncio.get_event_loop().run_until_complete(main(sys.argv[1]))
