import sys
import os

cwd = os.getcwd()
sys.path.append(cwd)

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from comp_finder.competition import Competition, wait_for_element
import time


PAGE_URL = 'https://www.worldcubeassociation.org/competitions?&region=USA&display=list'
cwd = os.getcwd()

# Various XPaths for competition info elements
COMPETITION = '//div[@id=\'upcoming-comps\']/ul/li[@class=\'list-group-item not-past\']'
LOCATION = './/div[@class="location"]'
LINK = './/div[@class="competition-link"]/a'
DATE = './/span[@class="date"]'
VENUE = './/div[@class="venue-link"]/p'

def find_comps(output, states, location):
    """finds local comps every 30 mins"""
    while True:

        # create webdriver without physical window
        op = ChromeOptions()
        op.add_argument('headless')
        driver = Chrome(f'{cwd}/chromedriver', options=op)


        driver.get(PAGE_URL)

        # finds all list elements for competitions on competitions page
        time.sleep(5)
        competitions_elements = driver.find_elements_by_xpath(COMPETITION)

        # list to be filled with Competition objects
        competitions = []

        for elem in competitions_elements:
            comp_location = elem.find_element_by_xpath(LOCATION).text
            
            # checks if competition is in any of the local states
            if comp_location.split(', ')[-1] in states:
                # find various info about competition

                comp_name = elem.find_element_by_xpath(LINK).text
                comp_date = elem.find_element_by_xpath(DATE).text
                comp_venue = elem.find_element_by_xpath(VENUE).text
                comp_link = elem.find_element_by_xpath(LINK).get_attribute('href')

                competitions.append(
                    Competition(comp_name, comp_date, location, 
                                    comp_link, comp_venue, driver)
                    )

        with open(output, 'w+') as f:
            f.write('\n\n'.join([str(i) for i in competitions]))

        driver.quit()

        time.sleep(1800)


