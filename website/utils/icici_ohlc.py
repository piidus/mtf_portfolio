try:
    from flask import session
    import http
    import json
    import base64
    import socketio
    import datetime, time
    
except Exception as e:
    print('error in utils.icici_Ohlc : ', e)
SIO = None
OHLC = {}
def ohlc_connection(userid, session_token):
        # Python Socket IO Client
        try:
            sio = socketio.Client()
            auth = {"user": userid, "token": session_token}
            sio.connect("https://breezeapi.icicidirect.com/", socketio_path='ohlcvstream', headers={"User-Agent":"python-socketio[client]/socket"}, 
                        auth=auth, transports="websocket", wait_timeout=3)
            return sio
        except Exception as e:
            print(e)
class OhlcPython:
    ''' It only return session token'''
    
    __instance = None

    def __new__(cls, userid, session_token):
        '''api key, api session
        return api obj'''
        if cls.__instance is None:
            print('Connecting OHLC api......')
            new_api_connection = ohlc_connection(userid, session_token )
            cls.__instance = super(OhlcPython, cls).__new__(cls)
            cls.__instance = new_api_connection
            return cls.__instance
        else:
            print('WARNING : There\'s already an OHLC connection', cls.__instance)
            return cls.__instance

    def __init__(self, userid, session_token):
        
        print('Connected to the OHLC!')

class OHLCEngine:
    def __init__(self,userid, session_token) -> None:
        self.conn = OhlcPython(userid, session_token)
        # self.stock_list = ["4.1!"+item for item in stocklist]
        self.OHLC = {}
        # self.start_point()
        # print(self.stock_list)
#         # self.engine(stock_list=stocklist)
    
#     #CallBack functions to receive feeds
    def on_ticks(self,  ticks):
        # print(ticks)
        splited = ticks.split(',')
        stock_name = splited[1]
        stock_price = splited[3]
        time_ = splited[-2]
        self.OHLC[stock_name] = [stock_price, time_]
        # print(f"name : {stock_name}, ltp : {stock_price}, time : {time_}")

    def start_point(self,scrip_code,  channel_name = "1SEC"):
        #Connect to receive feeds
        self.conn.emit('join', scrip_code)
        self.conn.on(channel_name, self.on_ticks)
       
    def pause_point(self, script_code):
        print("Unwatch from the stock")
        self.conn.emit("leave", script_code)

    def close_point(self):
        print("Disconnect from the server")
        self.conn.emit("disconnect", "transport close")
    
    def engine(self, stock_list):
        scrip_code = ["4.1!" + item for item in list(stock_list)]
        # print(scrip_code)
        self.start_point(scrip_code)
        time.sleep(5)
        # print(self.OHLC)
        self.pause_point(script_code=scrip_code)
        return self.OHLC

    
# #CallBack functions to receive feeds
# def on_ticks(ticks):
#     # print(ticks)
#     splited = ticks.split(',')
#     stock_name = splited[1]
#     stock_price = splited[3]
#     time_ = splited[-2]
#     OHLC[stock_name] = [stock_price, time_]
#     print(f"name : {stock_name}, ltp : {stock_price}, time : {time_}")
    
# def start_point(script_code:list, conn,  ontick=on_ticks, channel_name = "1SEC"):
#     #Connect to receive feeds
#     conn.emit('join', script_code)
#     conn.on(channel_name, ontick)
    
# def pause_point(conn, script_code):
#     print("Unwatch from the stock")
#     conn.emit("leave", script_code)
# def close_point(conn):
#     print("Disconnect from the server")
#     conn.emit("disconnect", "transport close")
# def start_connection(userid, token):
#     '''
#     IT start SIO
#     '''
#     global SIO
#     try:
#         sio = ohlc_connection(userid=userid, session_token=token) #First start the 
#         SIO = sio
#     except Exception as e:
#         print('Error in start point ::', e)
#     else:   
#         return True

# def fetch_ltp(stock_list:list):
#     start_point(script_code=stock_list, conn=SIO)
#     stock_list = ["4.1!"+item for item in stock_list]
#     end_time = 1
#     while end_time>0:
#         time.sleep(len(stock_list+1))
#         pause_point(conn=SIO, script_code=stock_list)
#         print(OHLC)
#         end_time -=1
#     return json({'conne': 'ok'})

    
    

# def ohlc_connection(userid, session_token):
#         # Python Socket IO Client
#         try:
#             sio = socketio.Client()
#             auth = {"user": userid, "token": session_token}
#             sio.connect("https://breezeapi.icicidirect.com/", socketio_path='ohlcvstream', headers={"User-Agent":"python-socketio[client]/socket"}, 
#                         auth=auth, transports="websocket", wait_timeout=3)
#             return sio
#         except Exception as e:
#             print(e)

