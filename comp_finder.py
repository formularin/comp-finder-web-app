from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
import time as t
import os

# various XPaths for competition info elements
REGISTRATION_REQUIREMENTS = '//*[@id="registration_requirements_text"]'
COMPETITORS_LIST = '//*[@id="competition-nav"]/div/a[3]'
COMPETITOR_TABLE_FOOTER = '//*[@id="competition-data"]/div/div[1]/div[2]/div[2]/table/tfoot/tr/td[1]'
ADDRESS_INPUT = '//input[@placeholder=\'Choose starting point, or click on the map...\']'
ESTIMATED_TIME = '//*[@id=\'section-directions-trip-#\']/div[2]/div[1]/div[1]/div[1]/span[1]'
DIRECTIONS_BUTTON = '//*[@id=\'pane\']/div/div[1]/div/div/div[4]/div[1]/div/button'
COMPETITION = '//div[@id=\'upcoming-comps\']/ul/li[@class=\'list-group-item not-past\']'
LOCATION = './/div[@class="location"]'
LINK = './/div[@class="competition-link"]/a'
DATE = './/span[@class="date"]'
VENUE = './/div[@class="venue-link"]/p'

# additional constants
CWD = os.path.dirname(os.path.abspath(__file__))
PAGE_URL = 'https://www.worldcubeassociation.org/competitions?&region=USA&display=list'


def wait_for_element(driver, selector, method):
    """Returns element after waiting for page load"""
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(
            eval(f'EC.presence_of_element_located((By.{method}, "{selector}"))')
        )
    finally:
        element = eval(f'driver.find_element_by_{method.lower()}("{selector}")')

    return element


class Competition:
    """Object to hold all information about a WCA competition
    
    Args:
        name (str) -- name of competition

        d (selenium.webdriver.Chrome) -- webdriver to be used for collecting further info

        is_last (bool) -- whether or not this is the last competition of the group

        location (str) -- place to know driving distance from

        do_driving_distance, do_venue_address, do_reached_competitor_limit (bool) -- whether or not to take these measurements

        **kwargs -- can contain keys of date, website_link, and venue
    """
    def __init__(self, name, d, is_last, location,
                 do_driving_distance, do_venue_address, do_reached_competitor_limit, 
                 **kwargs):
        # all attributes defined here can be found in the WCA competitions page
        # the @property methods find information that must be found on the competition's individual page.
        
        # required args:
        self.name = name

        # necessary for finding other info about competition
        self.driver = d

        # boolean telling whether or not to close webdriver
        self.is_last = is_last

        # address to find distance to comps from
        self.location = location

        # booleans on whether or not to find specific information
        self.do_driving_distance = do_driving_distance
        self.do_reached_competitor_limit = do_reached_competitor_limit
        self.do_venue_address = do_venue_address

        # possible **kwargs
        try:
            self.date = kwargs['date']
        except KeyError:
            pass
        
        try:
            self.url = kwargs['website_link']
        except KeyError:
            pass

        try:
            self.venue = kwargs['venue']
        except KeyError:
            pass


    @property
    def reached_competitor_limit(self):
        """tells if the competitor limit for the competition has been reached
        
        Returns:
            bool -- True if it has been reached, False if not
        """
        try:
            if self.driver.current_url != self.url:
                self.driver.get(self.url)
        except AttributeError:
            self.driver.get(PAGE_URL)
            self.url = self.driver.find_element_by_link_text(self.name).get_attribute('href')
            self.driver.get(self.url)
        
        # find the line where the competitor limit is stated
        competitor_limit_line = [
            line for line in self.driver.find_element_by_xpath(REGISTRATION_REQUIREMENTS).text.split('\n') 
                if 'There is a competitor limit of' in line
                ][0].strip()

        competitor_limit = int(competitor_limit_line.split(' ')[-2])
        # find the link to the competitor list
        competitor_list_url = self.driver.find_element_by_xpath(COMPETITORS_LIST).get_attribute('href')

        self.driver.get(competitor_list_url)

        # find bottom text of competitor table
        table_footer = self.driver.find_element_by_xpath(COMPETITOR_TABLE_FOOTER).text.strip()

        people = int(table_footer.split(' ')[-2])

        if people == competitor_limit:
            return True
        else:
            return False


    @property
    def venue_address(self):
        """Finds address to competition venue"""
        
        try:
            if self.driver.current_url != self.url:
                self.driver.get(self.url)
        except AttributeError:
            self.driver.get(PAGE_URL)
            self.url = self.driver.find_element_by_link_text(self.name).get_attribute('href')
            self.driver.get(self.url)

        # find the link on the page that goes to google maps
        link = [elem for elem in self.driver.find_elements_by_xpath('//a')
                if 'google.com/maps' in elem.get_attribute('href')
                ][0]
        
        return link.text
 

    @property
    def driving_distance(self):
        """Finds the driving distance from your location to the competition
        
        Returns:
            str -- hours h minutes min
        """
        
        try:
            if self.driver.current_url != self.url:
                self.driver.get(self.url)
        except AttributeError:
            self.driver.get(PAGE_URL)
            self.url = self.driver.find_element_by_link_text(self.name).get_attribute('href')
            self.driver.get(self.url)

        # link to venue on google maps
        link = self.driver.find_element_by_link_text(self.venue_address).get_attribute('href')

        self.driver.get(link)

        # click directions button
        directions_button = wait_for_element(self.driver, DIRECTIONS_BUTTON, 'XPATH')
        i = 0
        while i <= 10:
            try:
                directions_button.click()
                break
            except ElementNotVisibleException as e:
                if i == 10:
                    raise e
                else:
                    i += 1
            t.sleep(1)

        # send location to address input field
        input_field = wait_for_element(self.driver, ADDRESS_INPUT, 'XPATH')
        input_field.send_keys(self.location)
        input_field.send_keys(Keys.ENTER)

        # find estimated times
        times = []
        i = 0
        while True:
            try:
                xpath = ESTIMATED_TIME.replace('#', str(i))
                estimated_time_elem = wait_for_element(
                    self.driver, xpath, 'XPATH'
                )
                times.append(estimated_time_elem.text)
                i += 1
            except NoSuchElementException:
                break

        times_in_minutes = []
        for time in times:
            time_in_minutes = 0
            if 'h' in time:
                hours_digits = []
                for char in time:
                    try:
                        test_integer = int(char)
                        hours_digits.append(char)
                    except ValueError:
                        break
                hours = int(''.join(hours_digits))
                time_in_minutes += 60 * hours
            if 'min' in time:
                mins_digits = []
                for char in time:
                    try:
                        test_integer = int(char)
                        mins_digits.append(char)
                    except ValueError:
                        break
                mins = int(''.join(mins_digits))
                time_in_minutes += mins
            times_in_minutes.append(time_in_minutes)

        return times[times_in_minutes.index(min(times_in_minutes))]

    def run(self):
        """Returns dictionary containing all of the competition's information"""

        def try_expression(expression, self):
            try:
                return eval(expression)
            except Exception as e:
                return

        outputs = [
            try_expression(f'self.{info_type}', self) for info_type in
            [
                'name', 
                'date',
                'venue',
                'url',
            ]
                   ]

        while True:
            try:
                outputs.remove(None)
            except ValueError:
                break

        if self.do_venue_address:
            outputs.append(self.venue_address)
        if self.do_driving_distance:
            outputs.append(self.driving_distance)
        if self.do_reached_competitor_limit:
            outputs.append(self.reached_competitor_limit)

        if self.is_last:
            self.driver.quit()

        return [str(i).strip() for i in outputs]


def find_comps(states, location, information_types):
    """Returns Competition objects for competition in states
    
    Potential Information Types (must be in this order):
        date
        venue
        website_link
        venue_address
        driving_distance
        reached_competitor_limit
    """

    # create webdriver without physical window
    op = ChromeOptions()
    op.add_argument('headless')
    driver = Chrome(f'{CWD}/chromedriver', options=op)

    driver.get(PAGE_URL)

    # finds all list elements for competitions on competitions page
    t.sleep(5)
    competitions_elements = driver.find_elements_by_xpath(COMPETITION)

    # list to be filled with Competition objects
    competitions = []

    for i, elem in enumerate(competitions_elements):
        comp_location = elem.find_element_by_xpath(LOCATION).text
        
        # checks if competition is in any of the local states
        if comp_location.split(', ')[-1] in states:
            # find various info about competition

            information = []

            comp_name = elem.find_element_by_xpath(LINK).text
            if 'date' in information_types:
                comp_date = elem.find_element_by_xpath(DATE).text
                information.append(comp_date)
            if 'venue' in information_types:
                comp_venue = elem.find_element_by_xpath(VENUE).text
                information.append(comp_venue)
            if 'website_link' in information_types:
                comp_link = elem.find_element_by_xpath(LINK).get_attribute('href')
                information.append(comp_link)

            competitions.append(
                    Competition(
                        comp_name, driver, False, location,

                        bool('driving_distance' in information_types), 
                        bool('venue_address' in information_types), 
                        bool('reached_competitor_limit' in information_types),

                        **dict(zip(
                            [i for i in ['date', 'venue', 'website_link'] if i in information_types], 
                            information
                            )))
                    )
        
    try:
        competitions[-1].is_last = True

        information_types.insert(0, 'name')
        
        comp_strings = [competition.run() for competition in competitions]
        
        categories = [' '.join([x.capitalize() for x in i.split('_')]) for i in information_types]
        output = [information_types, comp_strings]

        return output

    except IndexError:

        return 'None'
