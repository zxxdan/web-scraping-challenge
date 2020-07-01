

# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import time


def scrape_data():

    # NASA Mars News
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html5lib' to get HTML same as webpage
    soup = BeautifulSoup(response.text, 'html5lib')

    # Getting Title and Paragraph text of latest article
    news_title = soup.find('div', class_="content_title").text
    news_p = soup.find('div', class_="rollover_description_inner").text

    # JPL Mars Space Images - Featured Image
    # Currently utilizing ChromeDriver 83.0.4103.14 alongside (winx32)
    # Google Chrome is up to date Version 83.0.4103.116 (Official Build) (64-bit)

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Loading URL of the page to be scraped
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Retreiving the current featured image URL
    img_html = browser.html
    img_soup = BeautifulSoup(img_html, 'html.parser')
    img_url = img_soup.find('a', id='full_image')['data-fancybox-href']
    base_url = 'https://www.jpl.nasa.gov'
    featured_image_url = (base_url + img_url)

    # Mars Weather
    # Loading URL of the page to be scraped
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    # Retreiving the latest Tweet for Mars' temperature details
    time.sleep(3)
    tweet_html = browser.html
    tweet_soup = BeautifulSoup(tweet_html, 'html.parser')
    tweet = tweet_soup.find_all(
        'div', class_='css-901oao r-jwli3a r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0')
    # tweet = tweet_soup.find_all('div', lang='en')

    # Mars Facts
    # Scraped table from URL, and created table in Pandas
    mars_facts_url = "https://space-facts.com/mars/"
    table = pd.read_html(mars_facts_url)

    # Adding column names, and resetting index
    mars_facts_df = table[0]
    mars_facts_df.columns = ["Parameters", "Value"]
    mars_facts_df.set_index(["Parameters"])

    # Coverting from Pandas to HTML table string, replacing any '\n' with ''
    mars_facts_html = mars_facts_df.to_html(index=False)
    mars_facts_html = mars_facts_html.replace("\n", "")

    # Creating HTML file of Mars Facts
    mars_facts_df.to_html('mars_facts.html')

    # Mars Hemispheres
    # Loading URL of the page to be scraped
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    # Within the main page, loop through to look for the title (name of the hemisphere), which also doubles as the link to that hemisphere's details
    # Upon loop of each hemisphere, click on the details page, and find the link of full detailed image
    # While within loop, append to empty lists
    # Return to main page, and start next loop

    hemi_html = browser.html
    hemi_soup = BeautifulSoup(hemi_html, 'html.parser')
    hemi_imgs = hemi_soup.find_all('a', class_='itemLink product-item')

    title = []
    img_url = []

    for hemi_img in hemi_imgs:
        if(hemi_img.text):
            title.append(hemi_img.text.strip())

            browser.click_link_by_partial_text(hemi_img.text.strip())

            spec_hemi_html = browser.html
            spec_hemi_soup = BeautifulSoup(spec_hemi_html, 'html.parser')
            spec_hemi_imgs = spec_hemi_soup.find_all('li')[0]
            if(spec_hemi_imgs.a):
                img_url.append(spec_hemi_imgs.a.get('href'))

            browser.visit(url)

    # Create list of dictionaries
    hemisphere_image_urls = []

    for i, j in zip(title, img_url):
        hemisphere_image_urls.append({"Title": i, "Image_URL": j})

    browser.quit()

    scraped_mars_data = {
        "News_Title": news_title,
        "News_Preview": news_p,
        "Featured_Image_URL": featured_image_url,
        "Mars_Temperature": tweet[0].text,
        "Mars_Facts": mars_facts_html,
        "Hemisphere_Info": hemisphere_image_urls
    }
    return scraped_mars_data
