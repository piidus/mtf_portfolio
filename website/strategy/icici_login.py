try:
    from flask import request, render_template, make_response
    import time
    import json
    import hashlib
    from datetime import datetime
    import webbrowser
except Exception as e:
    print('Error in strategy/icicilogin.py  :', e)

class SessionKeyGenerator:
    '''
    It automate help to get icici session key
    '''

    def __init__(self, api_key,api_secrect, user_id, password) -> None:
        self.__api_key = api_key
        self.__api_secrect = api_secrect
        # self.__user_id = user_id
        # self.__pwd = password
        # self.browser = webdriver.Firefox()
        # self.__decoded_api_key = self.__api_key
   
    # def login(self):
    #     try:
    #         self.__api_login_path = f"https://api.icicidirect.com/apiuser/login?api_key={self.__decoded_api_key}"
        
    #         self.browser.get(self.__api_login_path)
    #     except WebDriverException:
    #         print(WebDriverException)
    #         return None
    #     time.sleep(3)
    def icici_login(self):
        # Set the header
        response = make_response()
        response.headers["X-My-Header"] = "My Header Value"

        # Open the new tab
        response.headers["Content-Type"] = "text/html"
        response.set_cookie("new_tab", "true")
        response.set_data("<script>window.open('https://www.google.com', '_blank');</script>")

        return response

        # api_key = self.__api_key
        # # username = request.form['username']
        # # password = request.form['password']
        # print(1)
        # # Create the payload as a JSON string
        # # App related Secret Key
         
        # payload = json.dumps({
        #     'secret_key' : self.__api_secrect
        #     # "username": username,
        #     # "password": password
        # }, separators=(',', ':'))
        # try:
        # # Time_stamp & checksum generation for request-headers
        #     time_stamp = datetime.utcnow().isoformat()[:19] + '.000Z'
        #     checksum = hashlib.sha256((time_stamp + payload + self.__api_secrect).encode("utf-8")).hexdigest()
        
        # # URL for the login endpoint
        #     login_url = f"https://api.icicidirect.com/apiuser/login?api_key=i8582*146#NX60853w32X3*56nd8x8l0"
        # except Exception as e:
        #     print(e)
        # # Headers for the POST request
        # headers = {
        #     'Content-Type': 'application/json',
        #     'Time-Stamp': time_stamp,
        #     'Checksum': checksum
        # }
        # try:
        # # Make the POST request
        #     response = requests.post(login_url, data=payload, headers=headers)
        # except Exception as e:
        #     print(e)
        # if response.status_code == 200:
        #     # Request was successful
        #     response_data = response.json()

        #     # Open the response in a new tab
        #     response_html = render_template('response.html', data=response_data)
        #     with open('response.html', 'w') as f:
        #         f.write(response_html)
        #     webbrowser.open('response.html')

        #     return "Response opened in a new tab."
        # else:
        #     # Request failed
        #     return "Request failed."



