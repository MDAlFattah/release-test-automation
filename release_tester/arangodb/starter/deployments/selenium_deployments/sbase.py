#!/usr/bin/env python3
""" base class for arangodb starter deployment selenium frontend tests """
from abc import abstractmethod, ABC
import time

from selenium.webdriver.common.keys import Keys

class SeleniumRunner(ABC):
    "abstract base class for selenium UI testing"
    def __init__(self, webdriver):
        """ hi """
        self.web = webdriver

    def disconnect(self):
        """ byebye """
        self.web.close()

    def connect_server(self, frontend_instance, database, cfg):
        """ login... """
        self.web.get("http://" + frontend_instance.get_public_plain_url() + "/_db/_system/_admin/aardvark/index.html")
        assert "ArangoDB Web Interface" in self.web.title
        elem = self.web.find_element_by_id("loginUsername")
        elem.clear()
        elem.send_keys("root")
        elem.send_keys(Keys.RETURN)
        time.sleep(13)
        elem = self.web.find_element_by_id("goToDatabase").click()

        assert "No results found." not in self.web.page_source
