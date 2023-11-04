try:
    import http
    import json
    import base64
    from breeze_connect import BreezeConnect
except Exception as e:
    print('error in utils.icici_connections : ', e)
# Breeze api connections ---------------------------
def breeze_connection(api, secrect, session):
        __icici = BreezeConnect(api_key=api)
        __icici.generate_session(api_secret=secrect, session_token=session)
        return __icici
class Breeze_api:
    __instance = None

    def __new__(cls, api_key, api_secret, api_session ):
        if cls.__instance is None:
            print('Connecting Breeze......')
            new_api_connection = breeze_connection(api_key, api_secret, api_session )
            cls.__instance = super(Breeze_api, cls).__new__(cls)
            cls.__instance = new_api_connection
            return cls.__instance
        else:
            print('WARNING : There\'s already an instance Breeze of connection')
            return cls.__instance

    def __init__(self, api_key, api_secret, api_session ):
        
        print('Connected to the Breeze!')
        pass

# Icici api connection ------------------------------
def connection(key, session):
    try:        
        conn = http.client.HTTPSConnection("api.icicidirect.com")
        # dic_pay = f'SessionToken'

        payload = "{\r\n    \"SessionToken\": \"111\",\r\n    \"AppKey\": \"444\"\r\n}"
        # payload ={SessionToken:16770876,AppKey:5s52IFU6681m7p2L00%231d!8b496188}
        headers = { "Content-Type": "application/json"}
        edit_payload = json.loads(payload)
        edit_payload['SessionToken'] = session
        edit_payload['AppKey'] = key
        # print(json.dumps(edit_payload))
        # print(json.loads(payload))
        json_payload = json.dumps(edit_payload)
        conn.request("GET", "/breezeapi/api/v1/customerdetails", json_payload, headers)
        res = conn.getresponse()
        data = res.read()
        data = data.decode("utf-8")
        connec = json.loads(data)
        total_session_token = connec['Success']['session_token']
        user_id, session_token = base64.b64decode(total_session_token.encode('ascii')).decode('ascii').split(":")
            # print(session_token, user_id)
        return user_id, session_token, total_session_token
    except Exception as e:
        print('Error in connection :', e)
class Icici_Connect:
    ''' It only return session token'''
    __instance = None

    def __new__(cls, api_key, session_token):
        '''api key, api session
        return api obj'''
        if cls.__instance is None:
            print('Connecting ......')
            new_api_connection = connection(api_key, session_token )
            cls.__instance = super(Icici_Connect, cls).__new__(cls)
            cls.__instance = new_api_connection
            return cls.__instance
        else:
            print('WARNING : There\'s already an instance of connection')
            return cls.__instance

    def __init__(self, api_key, session_token):
        # self.__api = api_key
        # self.__api_sec= api_secret
        # self.__api_session = api_session
        print('Connected to the internet!')
        pass