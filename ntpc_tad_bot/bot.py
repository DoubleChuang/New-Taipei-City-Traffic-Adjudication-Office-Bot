import os
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta

from ntpc_tad_bot.logger import error_logger, logger
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class NTPC_TAD_Bot:
    def __init__(self):
        self._url = "https://npm.cpami.gov.tw"
        self._case_status = ""
        
        self._chrome = webdriver.Remote(
            os.getenv("CHROME_REMOTE_URL"),
            desired_capabilities=DesiredCapabilities.CHROME)

        # ## for screen display
        # _chrome_opt = Options()
        # _chrome_opt.add_argument("--disable-notifications")
        # # _chrome_opt.add_argument('--headless')  # enable headless mode
        # _chrome_opt.add_argument('--disable-gpu') # disable GPU, avoid system error or web error
        # self._chrome = webdriver.Chrome(
        #     './chromedriver', chrome_options=_chrome_opt)

    def wait_loading(self, wait_sec: float = 2.0):
        # Wait for the page to load
        time.sleep(wait_sec)
    
    def capture_screen(self, screen_path):
        if screen_path is not None:
            screen_path = Path(screen_path)

            if screen_path.is_dir():
                screen_path = screen_path / 'screen.png'
            
            screen_path = screen_path.with_suffix('.png')
            
            self._chrome.save_screenshot(f'{screen_path}')

    def query_case_status(self, case_id: str = "1113365", accident_date: str = "1110912"): # remove default value
        try:
            self._chrome.get("https://www.tadaes.ntpc.gov.tw/APSQ/APSQ02.aspx")
            
            self._chrome.find_element_by_id("ContentPlaceHolder1_TextBox1").clear()
            self._chrome.find_element_by_id("ContentPlaceHolder1_TextBox1").click()
            self._chrome.find_element_by_id("ContentPlaceHolder1_TextBox1").send_keys(accident_date)
            
            self._chrome.find_element_by_id("ContentPlaceHolder1_TextBox2").clear()
            self._chrome.find_element_by_id("ContentPlaceHolder1_TextBox2").click()
            self._chrome.find_element_by_id("ContentPlaceHolder1_TextBox2").send_keys(case_id)
            
            self._chrome.find_element_by_id("ContentPlaceHolder1_Button1").click()
            
            self.wait_loading()
            
            current_status = self._chrome.find_element_by_xpath('//*[@id="ContentPlaceHolder1_Labela2"]').text
            return current_status
        except Exception as e:
            err_msg = f"failed to query case status: {e}"
            error_logger.error(err_msg)
            return err_msg
    
    def run(self, case_id: str, accident_date: str, final_screen_path: str):
        logger.info("1. query_case_status")
        self._case_status = self.query_case_status(case_id, accident_date)
        self.capture_screen(final_screen_path)
        logger.info("Done !!")

    def notify_line(self, token: str):
        if not token: return
       
        # message you want to send
        tpe_date = datetime.now(tz=timezone(timedelta(hours=+8))).strftime("%Y/%m/%d")
        
        message = f'''
        NTPC_TAD_Bot {tpe_date}
        {self._case_status}
        '''

        # HTTP headers and message
        headers = {"Authorization": f"Bearer {token}"}
        data = { 'message': message }

        # Image want to sens
        # image = open('my_image.jpg', 'rb')
        # files = { 'imageFile': image }

        # send line notify by Line API
        requests.post(
            "https://notify-api.line.me/api/notify",
            headers = headers,
            data = data,
            # files = files
        )
        

    def teardown(self):
        if self._chrome is not None:
            self._chrome.quit()
