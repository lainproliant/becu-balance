#!/usr/bin/env python
# --------------------------------------------------------------------
# becu_balance.py
#
# Author: Lain Musgrove (lain.proliant@gmail.com)
# Date: Tuesday September 19, 2023
# --------------------------------------------------------------------

import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.chrome import ChromeDriver
from selenium.webdriver.remote.webdriver import WebElement


# --------------------------------------------------------------------
def env(key: str) -> str:
    if key not in os.environ:
        raise ValueError("Undefined key: " + key)
    return os.environ[key]


# --------------------------------------------------------------------
class Waiter:
    def __init__(self, browser: ChromeDriver, timeout=10):
        self._wait = WebDriverWait(browser, timeout)

    def wait_for(self, css_selector: str) -> WebElement:
        return self._wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )


# --------------------------------------------------------------------
def main():
    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    browser.get("https://onlinebanking.becu.org/BECUBankingWeb/Login.aspx")

    waiter = Waiter(browser)
    usernameInput = waiter.wait_for('#ctlSignon_txtUserID')
    passwordInput = waiter.wait_for('#ctlSignon_txtPassword')
    loginButton = waiter.wait_for('#ctlSignon_btnLogin')

    usernameInput.send_keys(env("BECU_USERNAME"))
    passwordInput.send_keys(env("BECU_PASSWORD"))
    loginButton.click()

    account_table = waiter.wait_for('#AccountsBorder table.dataTableXtended')
    rows = account_table.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if not cells:
            continue
        print(f"{cells[0].text}: {cells[2].text}")


# --------------------------------------------------------------------
if __name__ == "__main__":
    main()
