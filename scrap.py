from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.add_argument("--headless")

driver = webdriver.Firefox(firefox_options=options, executable_path="D:\projects\Diploma\Parsing\geckodriver.exe") #No GUI
#driver = webdriver.Firefox(executable_path="D:\projects\Diploma\Parsing\geckodriver.exe")                         #GUI

driver.get('https://devpost.com/hackathons')


el = driver.find_element_by_css_selector(".load-more > a:nth-child(1)")
while el.is_displayed():
    el.click()

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# titles = list(soup.findAll("h2", {"class": "title"}))
# locations = list(soup.findAll("p", {"class": "challenge-location"}))
# descriptions = list(soup.findAll("p", {"class": "challenge-description"}))
# time = list(soup.findAll("span", {"class": "value date-range"}))

rows = list(soup.select("#container > div > div > div > div.results > div.challenge-results > div"))

titles = []
locations = []
descriptions = []
time = []

for row in rows:
    temp_title = row.find("h2", {"class": "title"})
    temp_location = row.find("p", {"class": "challenge-location"})
    temp_description = row.find("p", {"class": "challenge-description"})
    temp_time = row.find("span", {"class": "value date-range"})

    if hasattr(temp_title, "text"):
        titles.append(temp_title.text.strip())
    else:
        titles.append("")

    if hasattr(temp_location, "text"):
        locations.append(temp_location.text.strip())
    else:
        locations.append("")

    if hasattr(temp_description, "text"):
        descriptions.append(temp_description.text.strip())
    else:
        descriptions.append("")

    if hasattr(temp_time, "text"):
        time.append(temp_time.text.strip())
    else:
        time.append("")

file = open("data.json", "w")
file.write('{\n\t"items":[\n')
i = 0
while 1:
    file.write('\t\t{\n')
    file.write('\t\t\t"title":' + '"' + titles[i].encode('ascii', 'ignore') + '"' + ',\n')
    file.write('\t\t\t"location":' + '"' + locations[i].encode('ascii', 'ignore') + '"' + ',\n')
    file.write('\t\t\t"description":' + '"' + descriptions[i].encode('ascii', 'ignore') + '"' + ',\n')
    file.write('\t\t\t"time":' + '"' + time[i].encode('ascii', 'ignore') + '"\n')
    if i + 1 < len(rows):
        file.write("\t\t},\n")
    else:
        file.write("\t\t}\n")
        break
    i = i + 1
file.write("\t]\n}")
file.close()
