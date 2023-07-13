from RPA.Browser.Selenium import Selenium
from SeleniumLibrary.errors import ElementNotFound
from selenium import webdriver
from utils.locators import Locators_NYT
import utils.helpers as helpers
import time
import datetime


class NYT_RPA:
    def __init__(
        self, screenshot_directory, implicit_wait=30, timeout=30, speed=0, auto_close=True, **config
    ):
        self.browser = Selenium(timeout=timeout, auto_close=auto_close)

        self.browser.set_selenium_implicit_wait(implicit_wait)
        self.browser.set_screenshot_directory(path=screenshot_directory)
        self.browser.set_selenium_speed(speed)
        helpers.logger.info(self.browser.get_selenium_implicit_wait())
        helpers.logger.info(self.browser.get_selenium_speed())
        helpers.logger.info(self.browser.get_selenium_timeout())

        self.init_url = config.get("init_url", "http://www.nytimes.com/")
        self.start_date = config.get("start_date", "")
        self.end_date = config.get("end_date", "")

        self.sections = config.get("sections", "")
        self.types = config.get("types", "")
        self.sort_by = config.get("sortBy", "newest")


    def close_browser(self):
        if self.browser:
            self.browser.capture_page_screenshot()
            self.browser.close_all_browsers()


    def get_news_from(self, search_phrase: str, max_retries=3):
        if search_phrase is None or search_phrase == "":
            helpers.logger.error("search_phrase cannot be empty.")
            return None
        if self.start_date is None or self.start_date == "":
            helpers.logger.error("start_date cannot be empty.")
            return None
        if self.end_date is None or self.end_date == "":
            helpers.logger.error("end_date cannot be empty.")
            return None

        # Retry strategy
        retry_count = 0
        while retry_count < max_retries:
            try:
                self.open_the_website(self.init_url)
                self.basic_search(search_phrase)
                if self.set_parameters_for_search(
                    self.start_date, self.end_date, self.sections, self.types
                ) == 2:
                    return 2  # Empty result
                self.sort_news(self.sort_by)
                self.expand_result()
                return self.extract_info(search_phrase)
            except Exception as e:
                self.close_browser()
                helpers.logger.error(e)
                helpers.logger.info(f"Error with RPA: {str(e)}")
                helpers.logger.info(f"Retrying: ({retry_count}/{max_retries})")
                retry_count += 1
        if retry_count >= max_retries:
            helpers.logger.error("Max retries exceeded. Unable to download the image.")


    def open_the_website(self, url: str):
        # https://github.com/GoogleChrome/chrome-launcher/blob/main/docs/chrome-flags-for-tools.md
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--blink-settings=imagesEnabled=false")
        chrome_options.add_argument("--disable-features=CSSLayoutNG")
        chrome_options.add_argument("--disable-popup-blocking")

        self.browser.open_available_browser(url, options=chrome_options)
        self.browser.wait_until_page_contains_element(Locators_NYT.ICON_PAGE_LOADED)
        try:
            time.sleep(5)
            self.browser.wait_and_click_button(Locators_NYT.GDPR_REJECT)
        except:
            pass
        return True


    def basic_search(self, search_phrase: str):
        if self.browser.does_page_contain_element(Locators_NYT.ICON_BASIC_SEARCH):
            self.browser.click_element(Locators_NYT.ICON_BASIC_SEARCH)
            self.browser.input_text_when_element_is_visible(
                Locators_NYT.TXT_BASIC_SEARCH, search_phrase
            )
            self.browser.click_button_when_visible(Locators_NYT.BTN_BASIC_SEARCH)
            self.browser.wait_until_page_contains_element(Locators_NYT.BTN_ADV_DATE)
            return True
        elif self.browser.does_page_contain_element(Locators_NYT.ICON_BASIC_SEARCH_MOBILE):
            # mobile version
            self.browser.click_element(Locators_NYT.ICON_BASIC_SEARCH)
            self.browser.input_text_when_element_is_visible(
                Locators_NYT.TXT_BASIC_SEARCH_MOBILE, search_phrase
            )
            self.browser.click_button_when_visible(Locators_NYT.BTN_BASIC_SEARCH_MOBILE)
            self.browser.wait_until_page_contains_element(Locators_NYT.BTN_ADV_DATE_MOBILE)
            return True
        else:
            raise Exception("basic_search not found.")


    def set_parameters_for_search(self, start_date, end_date, sections, types):
        self.browser.click_button_when_visible(Locators_NYT.BTN_ADV_DATE)
        self.browser.click_button_when_visible(Locators_NYT.BTN_ADV_SPFC_DATE)

        helpers.logger.info(start_date)
        helpers.logger.info(end_date)
        time.sleep(1)
        self.browser.input_text_when_element_is_visible(Locators_NYT.TXT_ADV_START_DATE, start_date)
        self.browser.input_text_when_element_is_visible(Locators_NYT.TXT_ADV_END_DATE, end_date)
        self.browser.press_keys(Locators_NYT.TXT_ADV_END_DATE, "ENTER")

        time.sleep(1)
        if self.browser.is_element_enabled(Locators_NYT.BTN_ADV_SECTION):
            helpers.logger.info(sections)
            if sections and len(sections) > 0:
                time.sleep(1)
                self.browser.click_button_when_visible(Locators_NYT.BTN_ADV_SECTION)
                self.browser.wait_until_element_is_visible(Locators_NYT.LIST_ADV_SECTION)
                for section in sections:
                    loc = Locators_NYT.CHKBOX_ADV_SECTION.replace("$$Q$$", section.title())
                    if self.browser.does_page_contain_element(loc):
                        self.browser.select_checkbox(loc)

        time.sleep(1)
        if self.browser.is_element_enabled(Locators_NYT.BTN_ADV_TYPE):
            helpers.logger.info(types)
            if types and len(types) > 0:
                time.sleep(1)
                self.browser.click_button_when_visible(Locators_NYT.BTN_ADV_TYPE)
                self.browser.wait_until_element_is_visible(Locators_NYT.LIST_ADV_TYPE)
                for element in types:
                    loc = Locators_NYT.CHKBOX_ADV_TYPE.replace("$$Q$$", element.title())
                    if self.browser.does_page_contain_element(loc):
                        self.browser.select_checkbox(loc)

        time.sleep(1)
        helpers.logger.info(self.browser.find_element(Locators_NYT.LBL_RESULTS).text)
        if "Showing 0 results for:" in self.browser.find_element(Locators_NYT.LBL_RESULTS).text:
            return 2

        return True


    def sort_news(self, sort: str = "newest"):
        # best, newest, oldest
        helpers.logger.info(sort)
        self.browser.select_from_list_by_value(Locators_NYT.SLC_ADV_SORT, sort)


    def expand_result(self):
        try:
            self.browser.wait_until_page_contains_element(Locators_NYT.BTN_EXP_RSLT, timeout=3)
        except Exception:
            return True

        while self.browser.does_page_contain_button(Locators_NYT.BTN_EXP_RSLT):
            self.browser.click_button_when_visible(Locators_NYT.BTN_EXP_RSLT)
            time.sleep(2)
            try:
                self.browser.wait_until_page_contains_element(Locators_NYT.BTN_EXP_RSLT, timeout=3)
            except Exception:
                return True
        return True


    def extract_info(self, search_phrase: str):
        collected_news = []

        list_of_news = self.browser.find_elements(Locators_NYT.LIST_NEWS_CONTAINER)
        helpers.logger.info("News to collect: " + str(len(list_of_news)))
        for news in list_of_news:
            # Basic info
            title = self.find_element_safe(locator=Locators_NYT.TITLE_NEWS, parent=news)
            date = self.find_element_safe(locator=Locators_NYT.DATE_NEWS, parent=news)
            description = self.find_element_safe(locator=Locators_NYT.DESCRIPTION_NEWS, parent=news)

            # Image
            try:
                image_url = self.browser.find_element(locator=Locators_NYT.PICTURE_NEWS, parent=news)
                image_url = self.browser.get_element_attribute(image_url, "src")
                picture_filename = (
                    "output/"
                    + helpers.clean_string_for_filename(title)
                    + "_"
                    + datetime.datetime.now().strftime("%Y%m%d")
                    + ".png"
                )
                helpers.download_image(image_url, picture_filename)
            except ElementNotFound:
                picture_filename = "Not found."

            # Calculated
            count_search_phrase = helpers.count_search_phrase(search_phrase, title + " " + description)
            contains_money = helpers.contains_money(title + " " + description)

            # Fill the container and append to the list
            news_container = {
                "title": title,
                "date": date,
                "description": description,
                "picture_filename": picture_filename,
                "count_search_phrase": count_search_phrase,
                "contains_money": contains_money,
            }
            helpers.logger.info(news_container)
            collected_news.append(news_container)
        return collected_news


    def find_element_safe(self, locator, parent):
        try:
            web_element = self.browser.find_element(locator=locator, parent=parent)
            return web_element.text
        except ElementNotFound:
            return "Not found."