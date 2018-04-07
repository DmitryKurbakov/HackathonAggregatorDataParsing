from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import dbtools
import helpers

class Object(object):
    pass

class DataParsing:
    def __init__(self):
        self.options = Options()
        self.options.add_argument("--headless")

        #self.driver = webdriver.Firefox(firefox_options=self.options, executable_path="D:\projects\Diploma\Parsing\geckodriver.exe")  # No GUI
        self.driver = webdriver.Firefox(executable_path="D:\projects\Diploma\Parsing\geckodriver.exe")                         #GUI

    def scrap_source0(self):
        self.driver.get('https://devpost.com/hackathons')

        el = self.driver.find_element_by_css_selector(".load-more > a:nth-child(1)")
        while el.is_displayed():
            el.click()

        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # titles = list(soup.findAll("h2", {"class": "title"}))
        # locations = list(soup.findAll("p", {"class": "challenge-location"}))
        # descriptions = list(soup.findAll("p", {"class": "challenge-description"}))
        # time = list(soup.findAll("span", {"class": "value date-range"}))

        rows = list(soup.select("#container > div > div > div > div.results > div.challenge-results > div"))

        print "got rows"

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
            #self.driver.get(temp_ref)

            # temp_page = self.driver.page_source
            # temp_soup = BeautifulSoup(temp_page, 'html.parser')
            #
            # temp_description = temp_soup.find("article", {"id": "challenge-description"})

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

            # if hasattr(temp_description, "text"):
            #     descriptions.append(temp_description.text.replace("\n", "").replace('"', '').strip())
            # else:
            #     descriptions.append("")

            if hasattr(temp_time, "text"):
                time.append(helpers.format_date_source_0(temp_time.text.strip().encode('ascii', 'ignore')))
            else:
                time.append("")

            refs.append(temp_ref)

        print "got data"
        # file = open("data1.json", "w")
        # file.write('{\n\t"items":[\n')

        i = 0
        data = [None] * len(titles)

        while i < len(data):
            data[i] = Object()
            data[i].title = titles[i]
            data[i].location = locations[i]
            data[i].preview = preview[i]
            #data[i].description = descriptions[i].encode('ascii', 'ignore')
            data[i].time = time[i]
            data[i].ref = refs[i]
            data[i].area = ""
            data[i].source = source

            i = i + 1

        dbtools.insert_data(data)

        print "transferred data to database handler"

    def scrap_source1(self):
        self.read_info("https://mlh.io/seasons/na-2018/events")
        self.read_info("https://mlh.io/seasons/eu-2018/events")
        self.read_info("https://mlh.io/seasons/localhost-2018/events")

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

            # try:
            #     self.driver.get(temp_ref)
            # except:
            #     continue
            #
            # temp_page = self.driver.page_source
            # temp_soup = BeautifulSoup(temp_page, 'html.parser')
            #
            # temp_description = temp_soup.find("body")

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

            # if hasattr(temp_description, "text"):
            #     descriptions.append(temp_description.text.replace("\n", "").replace('"', '').strip().encode('ascii', 'ignore'))
            # else:
            #     descriptions.append("")

            time.append(temp_time)
            refs.append(temp_ref)

        i = 0
        data = [None] * len(titles)

        while i < len(data):
            data[i] = Object()
            data[i].title = titles[i]
            data[i].location = locations[i]
            data[i].preview = preview[i]
            # data[i].description = descriptions[i]
            data[i].time = time[i]
            data[i].ref = refs[i]
            data[i].area = ""
            data[i].source = source

            i = i + 1

        dbtools.insert_data(data)

# i = 0
#
# while 1:
#     temp = dbtools.Source(title=titles[i].encode('ascii', 'ignore'), location=locations[i].encode('ascii', 'ignore'), preview=preview[i].encode('ascii', 'ignore'),
#                           description=descriptions[i].encode('ascii', 'ignore'), time=time[i].encode('ascii', 'ignore'))
#
#     if i+1 >= len(rows):
#         break
#     i = i + 1
#
#     temp.save()
#     # file.write('\t\t{\n')
#     # file.write('\t\t\t"title":' + '"' + titles[i].encode('ascii', 'ignore') + '"' + ',\n')
#     # file.write('\t\t\t"location":' + '"' + locations[i].encode('ascii', 'ignore') + '"' + ',\n')
#     # file.write('\t\t\t"preview":' + '"' + preview[i].encode('ascii', 'ignore') + '"' + ',\n')
#     # file.write('\t\t\t"description:":' + '"' + descriptions[i].encode('ascii', 'ignore') + '"' ',\n')
#     # file.write('\t\t\t"time":' + '"' + time[i].encode('ascii', 'ignore') + '"\n')
#     #if i + 1 < len(rows):
#     #     file.write("\t\t},\n")
#     # else:
#     #     file.write("\t\t}\n")
#     #     break
#     #i = i + 1
# # file.write("\t]\n}")
# # file.close()


