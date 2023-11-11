try:
    from flask import current_app
    from flask_login import current_user
    import os, datetime, math
    import pandas as pd
    import threading
    from website.utils import Breeze_api, Icici_Connect, OHLCEngine, TradeDecesion
    from website.models import db, Algo, Advance_order
    
    # from historical_connection import history
    # from breeze_all import FnoOrderManagement   
except Exception as e:
    print('Import Error in strategy/Share Genious Strangle ::', e)

class ShareGeniousStrangle:
    '''
    Sale call, put on Open , Difference previous day high low
    Connect Breeze Api> Check History>
    '''
    def __init__(self, stock_name, expiry, lot, uid, app) -> None:
        self.__stock_name = stock_name
        self.__expiry_date = expiry
        self.__lot = int(lot)
        self.__uid = uid
        self.__app = app
        self.token = {'NIFTY' : ['NIFTY 50', 50],
                    'CNXBAN' : ['NIFTY BANK', 15],
                    'NIFFIN' : ['NIFTY FIN SERVICE']}
        self.__breeze_api =  self.breeze_connect() # First Connect to api
        self.__user_id, self.__icici_token, self.__icici_full_token = [i for i in self.icici_api()]
        self.history()
        # self.__today_oepn, self.__high_low = self.previous_day_history()
    def icici_api(self):
        algo = Algo.query.filter_by(user_id = current_user.id).first()
        return Icici_Connect(api_key=algo.api_key, api_session=algo.api_sesion)
    def breeze_connect(self):
        algo = Algo.query.filter_by(user_id = current_user.id).first()
        # print(algo.session_time)
        try:
            return Breeze_api(api_key=algo.api_key, api_secret=algo.api_secret, api_session=algo.api_sesion)
        except Exception as e:
            print(e)

    def history(self):
        # print(self.__icici_api, self.__icici_full_token)
        from_date = (datetime.datetime.now() -datetime.timedelta(days=6)).strftime('%Y-%m-%dT%H:%M:%S.000Z')
        to_date = (datetime.datetime.now().replace(hour=17) - datetime.timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S.000Z')
        history_ = self.__breeze_api.get_historical_data(interval="1day",
                            from_date= from_date,
                            to_date= to_date,
                            stock_code=self.__stock_name,  #CNXBAN
                            exchange_code="NSE")
        if history_['Status'] == 200:
            data = pd.DataFrame(history_['Success'])
            data = data[['datetime', 'open', 'high', 'low', 'close']].tail(1)
            high_low = (data['high'].astype(dtype='float').values - data['low'].astype(dtype='float').values)[0]
            print(high_low)
            
            threading.Timer(interval=1, function=self.get_ohlc, args=[self.__app, db, Advance_order, Algo  ]).start()
            # Fetch ltp
            
    def get_ohlc(self, app, db, adv_table, algo_table):
        # ohlc = OHLCEngine(userid=self.__user_id, session_token= self.__icici_token)
        # stock_token = self.token[self.__stock_name][0]

        # ltp = ohlc.engine(stock_list=stock_token)
        # print(ltp)
        print(self.__uid)
        pre_order =  TradeDecesion(app, db, self.__uid).check_database(model=adv_table, filter_criteria={'u_no': self.__uid, 'status':'due'})
        print(pre_order.symbol)