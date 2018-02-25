from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import dbtools


class Object(object):
    pass


options = Options()
options.add_argument("--headless")


#driver = webdriver.Firefox(firefox_options=options, executable_path="D:\projects\Diploma\Parsing\geckodriver.exe") #No GUI
driver = webdriver.Firefox(executable_path="D:\projects\Diploma\Parsing\geckodriver.exe")                         #GUI


def read_info(url):

    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    rows = list(soup.find_all("div", {"class": "event-wrapper"}))

    titles = []
    locations = []
    preview = []
    descriptions = []
    time = []
    refs = []

    for row in rows:
        temp_title = row.find("h3", {"itemprop": "name"})
        temp_location = row.find("div", {"itemprop": "address"})
        temp_preview = ""#row.find("p", {"class": "challenge-description"})

        temp_time = row.find("meta", {"itemprop": "startDate"}).get("content") + "-" + row.find("meta", {"itemprop": "endDate"}).get("content")

        temp_ref = row.find("a", href=True)['href'].encode('ascii', 'ignore')

        try:
            driver.get(temp_ref)
        except:
            continue

        temp_page = driver.page_source
        temp_soup = BeautifulSoup(temp_page, 'html.parser')

        temp_description = temp_soup.find("body")

        if hasattr(temp_title, "text"):
            titles.append(temp_title.text.strip())
        else:
            titles.append("")

        if hasattr(temp_location, "text"):
            locations.append(temp_location.text.strip())
        else:
            locations.append("")

        if hasattr(temp_preview, "text"):
            preview.append(temp_preview.text.strip())
        else:
            preview.append("")

        if hasattr(temp_description, "text"):
            descriptions.append(temp_description.text.replace("\n", "").replace('"', '').strip())
        else:
            descriptions.append("")

        time.append(temp_time)
        refs.append(temp_ref)

    i = 0
    data = [None] * len(titles)

    while i < len(data):

        data[i] = Object()
        data[i].title = titles[i].encode('ascii', 'ignore')
        data[i].location = locations[i].encode('ascii', 'ignore')
        data[i].preview = preview[i].encode('ascii', 'ignore')
        data[i].description = descriptions[i].encode('ascii', 'ignore')
        data[i].time = time[i].encode('ascii', 'ignore')
        data[i].ref = refs[i]

        i = i + 1

    dbtools.insert_data(data)


read_info("https://mlh.io/seasons/na-2018/events")