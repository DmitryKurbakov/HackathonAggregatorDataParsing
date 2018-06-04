from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import dbtools
import helpers
import time as timeout


class Object(object):
    pass


class DataParsing:
    def __init__(self):
        self.options = Options()
        self.options.add_argument("--headless")

        #self.driver = webdriver.Firefox(firefox_options=self.options, executable_path="D:\projects\Diploma\Parsing\geckodriver.exe")  # No GUI
        self.driver = webdriver.Chrome("/Users/dmitry/PycharmProjects/HackathonAggregatorDataParsing/chromedriver")                         #GUI

    def scrap_source0(self):
        self.driver.get('https://devpost.com/hackathons')

        el = self.driver.find_element_by_xpath('//*[@id="container"]/div/div/div/div[1]/div[2]/a')
        while el.is_displayed():
            if el.text == "":
                break
            el.click()
            timeout.sleep(1)

        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        rows = list(soup.select("#container > div > div > div > div.results > div.challenge-results > div"))

        print("got rows")

        titles = []
        locations = []
        preview = []
        # descriptions = []
        time = []
        refs = []
        source = "https://devpost.com/hackathons"

        for row in rows:
            temp_title = row.find("h2", {"class": "title"})
            temp_location = row.find("p", {"class": "challenge-location"})
            temp_preview = row.find("p", {"class": "challenge-description"})
            temp_time = row.find("span", {"class": "value date-range"})

            temp_ref = row.find("a", href=True)['href'].encode('ascii', 'ignore')

            if hasattr(temp_title, "text"):
                titles.append(temp_title.text.strip().encode('ascii', 'ignore'))
            else:
                titles.append("")

            if hasattr(temp_location, "text"):
                locations.append(temp_location.text.strip().encode('ascii', 'ignore'))
            else:
                locations.append("")

            if hasattr(temp_preview, "text"):
                preview.append(temp_preview.text.strip().encode('ascii', 'ignore'))
            else:
                preview.append("")

            if hasattr(temp_time, "text"):
                time.append(helpers.format_date(temp_time.text.strip().encode('ascii', 'ignore')))
            else:
                time.append("")

            refs.append(temp_ref)

        print("got data")

        i = 0
        data = [None] * len(titles)

        while i < len(data):
            data[i] = Object()
            data[i].title = titles[i].decode("utf-8")
            data[i].location = locations[i]
            data[i].preview = preview[i]
            #data[i].description = descriptions[i].encode('ascii', 'ignore')
            data[i].time = time[i]
            data[i].ref = refs[i]
            data[i].area = ""
            data[i].source = source

            i = i + 1

        dbtools.insert_data(data)

        print("transferred data to database handler")

    def scrap_source1(self):
        self.read_info("https://mlh.io/seasons/na-2019/events")
        # self.read_info("https://mlh.io/seasons/na-2018/events")
        # self.read_info("https://mlh.io/seasons/eu-2018/events")
        # self.read_info("https://mlh.io/seasons/localhost-2018/events")

    def read_info(self, url):

        self.driver.get(url)

        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        rows = list(soup.find_all("div", {"class": "event-wrapper"}))

        titles = []
        locations = []
        preview = []
        descriptions = []
        time = []
        refs = []
        source = url

        for row in rows:
            temp_title = row.find("h3", {"itemprop": "name"})
            temp_location = row.find("div", {"itemprop": "address"})
            temp_preview = ""  # row.find("p", {"class": "challenge-description"})

            temp_time = row.find("meta", {"itemprop": "startDate"}).get("content") + "-" + row.find("meta", {
                "itemprop": "endDate"}).get("content")

            temp_ref = row.find("a", href=True)['href'].encode('ascii', 'ignore')

            if hasattr(temp_title, "text"):
                titles.append(temp_title.text.strip().encode('ascii', 'ignore'))
            else:
                titles.append("")

            if hasattr(temp_location, "text"):
                locations.append(temp_location.text.strip().encode('ascii', 'ignore'))
            else:
                locations.append("")

            if hasattr(temp_preview, "text"):
                preview.append(temp_preview.text.strip().encode('ascii', 'ignore'))
            else:
                preview.append("")

            time.append(temp_time)
            refs.append(temp_ref)

        i = 0
        data = [None] * len(titles)

        while i < len(data):
            data[i] = Object()
            data[i].title = titles[i].decode("utf-8")
            data[i].location = locations[i]
            data[i].preview = preview[i]
            # data[i].description = descriptions[i]
            data[i].time = time[i]
            data[i].ref = refs[i]
            data[i].area = ""
            data[i].source = source

            i = i + 1

        dbtools.insert_data(data)

    def scrap_source2(self):
        self.driver.get('https://hackevents.co/hackathons')

        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        rows = []
        #rows = list(soup.select('#main > div.hackathons > div > div'))

        while True:
            temp_rows = list(soup.select('#main > div.hackathons > div > div'))
            for x in temp_rows:
                rows.append(x)

            el = self.driver.find_elements_by_css_selector('#main > div.hackathons > ul > li.next_page > a')
            if el.__len__() != 1:
                break
            el[0].click()
            timeout.sleep(2)
            self.driver.get(self.driver.current_url)
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')


            #rows = list(soup.select("#container > div > div > div > div.results > div.challenge-results > div"))

        print("got rows")

        titles = []
        locations = []
        preview = []
        # descriptions = []
        time = []
        refs = []
        source = "https://hackevents.co/hackathons"

        for row in rows:
            temp_title = row.find("a", {"class": "title"})
            city = row.find("span", {"class": "city"}).text
            country = row.find("span", {"class": "country"}).text
            temp_location = city + ', ' + country
            temp_preview = ""
            temp_time = row.find("span", {"class": "info-date"})

            temp_ref = row.find("a", {"class": "title"}, href=True)['href'].encode('ascii', 'ignore').decode('utf-8')

            if hasattr(temp_title, "text"):
                titles.append(temp_title.text.strip().encode('ascii', 'ignore'))
            else:
                titles.append("")

            if hasattr(temp_preview, "text"):
                preview.append(temp_preview.text.strip().encode('ascii', 'ignore'))
            else:
                preview.append("")

            if hasattr(temp_time, "text"):
                time.append(helpers.format_date_source2(temp_time.text.strip().encode('ascii', 'ignore')))
            else:
                time.append("")

            refs.append('https://hackevents.co' + temp_ref)
            locations.append(temp_location.strip().encode('ascii', 'ignore'))

        print("got data")

        i = 0
        data = [None] * len(titles)

        while i < len(data):
            data[i] = Object()
            data[i].title = titles[i].decode("utf-8")
            data[i].location = locations[i].decode("utf-8")
            data[i].preview = preview[i]
            # data[i].description = descriptions[i].encode('ascii', 'ignore')
            data[i].time = time[i]
            data[i].ref = refs[i]
            data[i].area = ""
            data[i].source = source

            i = i + 1

        dbtools.insert_data(data)

        print("transferred data to database handler")

    def scrap_source3(self):
        self.driver.get('https://rb.ru/list/hack-spring/')

        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        te = soup.select('#post-text')
        temp_rows = list(te[0].contents)
        rows = []

        for row in temp_rows:
            if temp_rows.index(row) + 2 < temp_rows.__len__():
                if row.name == 'h4' and temp_rows[temp_rows.index(row) + 2].name == 'p' and row.text != '':
                    rows.append(row)
                    rows.append(temp_rows[temp_rows.index(row) + 2])

            #rows = list(soup.select("#container > div > div > div > div.results > div.challenge-results > div"))

        print("got rows")

        titles = []
        locations = []
        preview = []
        # descriptions = []
        time = []
        refs = []
        source = "https://rb.ru/list/hack-spring/"

        i = 0
        while i < len(rows) - 1:
            temp_title = rows[i].text
            temp_ref = rows[i].find("a", href=True)['href']

            titles.append(temp_title.strip())
            refs.append(temp_ref)
            i += 2

        i = 1
        while i < len(rows):
            strong_text = ''
            strong_texts = rows[i].find_all('strong')
            for s in strong_texts:
                if s.text != '':
                    strong_text = s.text

            date_and_location = helpers.format_date_and_location_source3(strong_text)
            temp_time = date_and_location['date']
            temp_location = date_and_location['location']
            temp_preview = rows[i].text

            time.append(temp_time)
            locations.append(temp_location)
            preview.append(temp_preview)
            i += 2

        print("got data")

        i = 0
        data = [None] * len(titles)

        while i < len(data):
            data[i] = Object()
            data[i].title = titles[i]
            data[i].location = locations[i]
            data[i].preview = preview[i]
            # data[i].description = descriptions[i].encode('ascii', 'ignore')
            data[i].time = time[i]
            data[i].ref = str(refs[i])
            data[i].area = ""
            data[i].source = source

            i = i + 1

        dbtools.insert_data(data)

        print("transferred data to database handler")

    def scrap_source4(self):

        self.driver.get('https://it-events.com/hackathons?type=upcoming')

        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        rows = list(soup.select("body > div.container > div:nth-of-type(2) > div.col-10 > section > div"))

        print("got rows")

        titles = []
        locations = []
        preview = []
        # descriptions = []
        time = []
        refs = []
        source = "https://it-events.com"

        for row in rows:
            temp_title = row.find("a", {"class": "event-list-item__title"})
            temp_location = row.find("div", {"class": "event-list-item__info event-list-item__info_location"})
            temp_preview = ""
            temp_time = row.find("div", {"class": "event-list-item__info"})

            temp_ref = source + "/events" + row.find("a", href=True)['href'].encode('ascii', 'ignore').decode('utf-8')

            if hasattr(temp_title, "text"):
                titles.append(temp_title.text.strip())
            else:
                titles.append("")

            if hasattr(temp_location, "text"):
                locations.append(temp_location.text.strip())
            else:
                locations.append("")

            if hasattr(temp_preview, "text"):
                preview.append(temp_preview.text.strip().encode('ascii', 'ignore'))
            else:
                preview.append("")

            if hasattr(temp_time, "text"):
                time.append(helpers.format_date_source_4(temp_time.text.strip()))
            else:
                time.append("")

            refs.append(temp_ref)

        print("got data")

        i = 0
        data = [None] * len(titles)

        while i < len(data):
            data[i] = Object()
            data[i].title = titles[i]
            data[i].location = locations[i]
            data[i].preview = preview[i]
            data[i].time = time[i]
            data[i].ref = refs[i]
            data[i].area = ""
            data[i].source = source

            i = i + 1

        dbtools.insert_data(data)

        print("transferred data to database handler")
