import json
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.remote.webelement import WebElement
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager

class Titter:
    def __init__(self, username, password):
      if not username or not password:
        raise("Please set TWITTER_USER_NAME and TWITTER_PASSWORD environment variables")

      self.username = username
      self.password = password
      self.host_domain = "https://twitter.com"
      self.cookie_path = "cookies.json"

      options = webdriver.ChromeOptions()
      options.add_argument('lang=en')

      self.driver = webdriver.Chrome(options=self.get_options())
      self.default_wait = WebDriverWait(self.driver, 20)
      # self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    def send_tweet(self, message: str) -> None:
      # retrieve cookies from a json file
      send_button: WebElement = None
      if Path(self.cookie_path).exists():
        self.driver.get(self.host_domain)
        for cookie in json.loads(Path(self.cookie_path).read_text()):
          self.driver.add_cookie(cookie)

        self.driver.refresh()
        send_button = self.get_element_until_it_visiable("//span[text()='发帖']")

      else:
        send_button = self.login()

      self.find_messagebox_and_send(message, send_button)

    def login(self) -> WebElement:
      if not self.username or not self.password:
        print("Please set TWITTER_USER_NAME and TWITTER_PASSWORD environment variables")
        return

      self.driver.get(self.host_domain)

      try:
        # find accept cookie button and click it
        accept_cookie_button = self.get_element_until_it_visiable("//span[text()='Accept all cookies']")
        if accept_cookie_button.is_displayed():
          accept_cookie_button.click()
      except:
        print("accept cookies button is not exist.")

      # click on the Login button
      login_button = self.get_element_until_it_visiable("//a[@data-testid='loginButton']")
      login_button.click()

      # fill user namge
      user_name_textbox = self.get_element_until_it_visiable("//input[@autocomplete='username']")
      user_name_textbox.send_keys(self.username)

      # find next button and click it
      self.driver.find_element(By.XPATH, "//span[text()='Next']").click()

      password_textbox = self.get_element_until_it_visiable("//input[@autocomplete='current-password']")
      password_textbox.send_keys(self.password)

      # find login button and click it
      self.driver.find_element(By.XPATH, "//span[text()='Log in']").click()

      send_message_button = self.get_element_until_it_visiable("//span[text()='发帖']")
      if send_message_button.is_displayed():
        # save cookies
        Path(self.cookie_path).write_text(
          json.dumps(self.driver.get_cookies(), indent=2)
        )
        print('get cookies successed.')
        return send_message_button
      else:
        print('login failed.')
        return None


    def get_options(self) -> ChromiumOptions:
      options = webdriver.ChromeOptions()
      options.add_argument('lang=en')
      user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
      options.add_argument(f'--user-agent={user_agent}')
      return options


    def get_element_until_it_visiable(self, xpath: str) -> WebElement:
      self.default_wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
      return self.driver.find_element(By.XPATH, xpath)

    def find_messagebox_and_send(self, message: str, send_message_button: WebElement) -> None:
      if send_message_button != None and send_message_button.is_displayed():
        data_block = self.get_element_until_it_visiable("//div[@data-contents='true']")
        if data_block.is_displayed():
          data_block.send_keys(message)
          # time.sleep(5)
          send_message_button.click()
          print('send message successed.')

      else:
        print("send message failed.")

    def get_custom_wait(self, seconds: int) -> WebDriverWait:
      return WebDriverWait(self.driver, seconds)
