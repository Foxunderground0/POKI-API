from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import requests
import urllib.request
import time

# Set the Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-notifications")  # Disable notifications
chrome_options.add_argument("--disable-infobars")  # Disable infobars
chrome_options.add_argument("--mute-audio")  # Mute audio

# Set up the ChromeDriver service and WebDriver
# Replace with the path to your ChromeDriver executable
service = Service('path/to/chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)

# Set the waiting time for the elements to load (adjust as needed)
wait_time = 3


def scrape_images_from_profile(profile_url, num_scrolls):
    # Load the profile page
    driver.get(profile_url)
    time.sleep(wait_time)

    # Dismiss the notification prompt if it appears
    try:
        notif_prompt = driver.find_element(
            By.XPATH, '//div[@data-testid="tweetbox"]')
        actions = ActionChains(driver)
        actions.move_to_element(notif_prompt).click().perform()
        time.sleep(wait_time)
    except:
        pass

    # Parse and download images at each scroll step
    for _ in range(num_scrolls):
        print(_)
        # Get the page source
        page_source = driver.page_source

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find and scrape the images
        tweet_elements = soup.find_all('article', {'role': 'article'})
        for idx, tweet_element in enumerate(tweet_elements):
            image_elements = tweet_element.find_all('img', {'src': True})
            for image_idx, element in enumerate(image_elements):
                image_url = element['src']
                # Replace '_normal' in the image URL to get the original resolution image
                image_url = image_url.replace('_normal', '')
                # Check if the image width is greater than 600 pixels
                headers = requests.head(image_url).headers
                if int(headers.get('content-length', 0)) > 600:
                    # Download the image using urllib.request
                    urllib.request.urlretrieve(
                        image_url, f"scraped\\image_{idx}_{image_idx}.jpg")

        # Scroll down to load more tweets
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(wait_time)


# "https://twitter.com/pokimanelol"
profile_url = "https://twitter.com/pokimanelol"
num_scrolls = 100  # Number of times to scroll the feed

scrape_images_from_profile(profile_url, num_scrolls)
