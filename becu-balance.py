#!/usr/bin/env python
# --------------------------------------------------------------------
# becu_balance.py
#
# Author: Lain Musgrove (lain.proliant@gmail.com)
# Date: Tuesday September 19, 2023
# --------------------------------------------------------------------

import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebElement


# --------------------------------------------------------------------
def env(key: str) -> str:
    if key not in os.environ:
        raise ValueError("Undefined key: " + key)
    return os.environ[key]


# --------------------------------------------------------------------
def default_timeout():
    return int(os.environ.get("SELENIUM_TIMEOUT", "10"))


# --------------------------------------------------------------------
class Waiter:
    def __init__(self, browser: webdriver.Firefox, timeout=default_timeout()):
        self._wait = WebDriverWait(browser, timeout)

    def wait_for(self, css_selector: str) -> WebElement:
        return self._wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )

    def wait_until_ready(self):
        return self._wait.until(
            lambda driver: driver.execute_script("return document.readyState")
            == "complete"
        )


# --------------------------------------------------------------------
def main():
    options = Options()

    if os.environ.get("HEADLESS", None) is not None:
        options.add_argument("-headless")

    with webdriver.Firefox(options=options) as browser:
        browser.get("https://onlinebanking.becu.org/BECUBankingWeb/Login.aspx")

        waiter = Waiter(browser)
        username_input = waiter.wait_for("#ctlSignon_txtUserID")
        password_input = waiter.wait_for("#ctlSignon_txtPassword")
        login_button = waiter.wait_for("#ctlSignon_btnLogin")

        username_input.send_keys(env("BECU_USERNAME"))
        password_input.send_keys(env("BECU_PASSWORD"))
        login_button.click()

        waiter.wait_until_ready()

        if "invitation" in browser.current_url.lower():
            ask_later_button = waiter.wait_for("#ctlWorkflow_remind")
            ask_later_button.click()

        account_table = waiter.wait_for("#AccountsBorder table.dataTableXtended")
        rows = account_table.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if not cells:
                continue
            print(f"{cells[0].text}: {cells[2].text}")


# --------------------------------------------------------------------
if __name__ == "__main__":
    main()
