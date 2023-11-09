try:
    import http
    import json
    import base64
    import socketio
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
            print('WARNING : There\'s already an Breeze instance of connection')
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
        return [user_id, session_token, total_session_token]
    except Exception as e:
        print('Error in connection :', e)
class Icici_Connect:
    ''' It only return session token'''
    __instance = None

    def __new__(cls, api_key, api_session):
        '''api key, api session
        return api obj'''
        if cls.__instance is None:
            print('Connecting pyton api......')
            new_api_connection = connection(api_key, api_session )
            cls.__instance = super(Icici_Connect, cls).__new__(cls)
            cls.__instance = new_api_connection
            # print(cls.__instance)
            return cls.__instance
        else:
            print('WARNING : There\'s already an python instance of connection', cls.__instance[1])
            return cls.__instance

    def __init__(self, api_key, api_session):
        
        print('Connected to the internet!')
        pass

SIO = ''
class Ohlc:
    def __init__(self, userid, token) -> None:
        self.__userid = userid
        self.__token = token
        try:
            self.ohlc_connection()
        except Exception as e:
            print(e)
        # self.__user_id, self.__session_token, self.__total_token 
    # # Get ltp function
    def ohlc_connection(self):
        # Python Socket IO Client
        try:
            sio = socketio.Client()
            auth = {"user": self.__user_id, "token": self.__session_token}
            sio.connect("https://breezeapi.icicidirect.com/", socketio_path='ohlcvstream', headers={"User-Agent":"python-socketio[client]/socket"}, 
                        auth=auth, transports="websocket", wait_timeout=3)
            return sio
        except Exception as e:
            print(e)

# Channel name i.e 1SEC,1MIN,5MIN,30MIN


dic = {}

#CallBack functions to receive feeds
def on_ticks(ticks):
    # print(ticks)
    splited = ticks.split(',')
    stock_name = splited[1]
    stock_price = splited[3]
    time_ = splited[-2]
    dic[stock_name]=[stock_price, time_]
    print(f"name : {stock_name}, ltp : {stock_price}, time : {time_}")
    
def start_point(conn, script_code, ontick, channel_name = "1SEC"):
    #Connect to receive feeds
    conn.emit('join', script_code)
    conn.on(channel_name, ontick)
    
def pause_point(conn, script_code):
    print("Unwatch from the stock")
    conn.emit("leave", script_code)
def close_point(conn):
    print("Disconnect from the server")
    conn.emit("disconnect", "transport close")
