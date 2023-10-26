try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import WebDriverException
    import time
except Exception as e:
    print('Error in strategy/icicilogin.py  :', e)

class SessionKeyGenerator:
    '''
    It automate help to get icici session key
    '''

    def __init__(self, api_key, user_id, password) -> None:
        self.__api_key = api_key
        # self.__api_secrect = api_secrect
        self.__user_id = user_id
        self.__pwd = password
        self.browser = webdriver.Firefox()
        self.__decoded_api_key = self.__api_key
   
    def login(self):
        try:
            self.__api_login_path = f"https://api.icicidirect.com/apiuser/login?api_key={self.__decoded_api_key}"
        
            self.browser.get(self.__api_login_path)
        except WebDriverException:
            print(WebDriverException)
            return None
        time.sleep(3)


