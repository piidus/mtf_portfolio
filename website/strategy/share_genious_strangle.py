try:
    from flask import current_app
    from flask_login import current_user
    import os, datetime, math
    import pandas as pd
    import threading
    from website.utils import Breeze_api, Icici_Connect, OHLCEngine, TradeDecesion, option_ltp, round_to_multiple, FnoOrderManagement
    from website.models import db, Algo, Advance_order, Order, OptionTable
    
    # from historical_connection import history
    # from breeze_all import FnoOrderManagement   
except Exception as e:
    print('Import Error in strategy/Share Genious Strangle ::', e)

class ShareGeniousStrangle:
    '''
    Sale call, put on Open , Difference previous day high low
    Connect Breeze Api> Check History for previous h-l> check open price >
    check option price
    '''
    def __init__(self, stock_name, expiry, lot, uid, app) -> None:
        self.__stock_name = stock_name
        self.__expiry_date = expiry
        self.__lot = int(lot)
        self.__uid = uid
        self.__app = app
        self.token = {'NIFTY' : ['NIFTY 50', 50],
                    'CNXBAN' : ['NIFTY BANK', 15],
                    'NIFFIN' : ['NIFTY FIN SERVICE', 40]}
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
            self.__high, self.__low= data['high'].astype(dtype='float').values[0] , data['low'].astype(dtype='float').values[0]
            
            user_id = current_user.id
            threading.Timer(interval=1, function=self.get_ohlc, args=[self.__app, db, Advance_order, Order ,OptionTable,  user_id ]).start()
            # Fetch ltp
            
    def get_ohlc(self, app, db, adv_table, order_table, option_table, userid):
        ohlc = OHLCEngine(userid=self.__user_id, session_token= self.__icici_token)
        stock_token = self.token[self.__stock_name][0]
        print(stock_token)
        # pre_order(stock_token)
        self.__today_oepn =  ohlc.engine(stock_list=[stock_token])
        self.__today_oepn = 19574 #self.__today_oepn[self.__stock_name][0]
        self.__today_oepn = float(self.__today_oepn)
        print( 'open today ::',self.__today_oepn, type(self.__today_oepn))
        # # print(self.__uid)
        # # check option value
        call_strike = self.call_put_decesion(app, db, adv_table, order_table, option_table, userid)
        pre_order =  TradeDecesion(app, db, self.__uid).check_database(model=adv_table, filter_criteria={'u_no': self.__uid, 'status':'due'})
        # print(pre_order.symbol)
    
        
    def call_put_decesion(self, app, db, adv_table, order_table, option_table,  userid):
        self.__high_low = self.__high - self.__low
        mid_point = round(self.__high_low/2)
        call_value = self.__today_oepn+mid_point
        put_value = self.__today_oepn-mid_point
        print(call_value, put_value)
        self.call_strike, self.quantity = round_to_multiple(stock_name=self.__stock_name, strike_price=call_value, direction='up')
        self.put_strike, self.quantity = round_to_multiple(stock_name=self.__stock_name, strike_price=put_value, direction='down')
        # print(call_strike, put_strike)
        # Check call put ltp difference
        call_ltp, _ = option_ltp(api=self.__breeze_api,stock_code=self.__stock_name, expiry_date=self.__expiry_date, right='call', strike=self.call_strike)
        put_ltp, _ = option_ltp(api= self.__breeze_api, stock_code=self.__stock_name, expiry_date=self.__expiry_date, right='put', strike=self.put_strike)
        print(call_ltp, put_ltp)
        # Check difference of ltp 
        # Example values
        
        # trade = FnoOrderManagement(api=self.__breeze_api)
        # Check if the difference is less than 2/3
        if abs(call_ltp - put_ltp) < 1/3 * max(call_ltp, put_ltp):
            print("The difference is less than 2/3.")
            self.trade(app, db, order_table, userid)
            
        else:
            # Get the high value
            high_value = max(call_ltp,  put_ltp)
            
            # Calculate 2/3 of the high value
            two_thirds_high_value = 1/3 * high_value
            if call_ltp > put_ltp:
                print('find put')
                # find nearest put
                _, put_df_ = option_ltp(api=self.__breeze_api, stock_code=self.__stock_name, expiry_date=self.__expiry_date, right='put')
                put_df_ = put_df_[put_df_['ltp'] >=call_ltp * 2/3]
                put_strike_ = round(put_df_.head(1)['strike_price'].values[0])
                print(put_strike_)
                self.put_strike = put_strike_
                self.trade(app, db, order_table, userid)
            
            
            else:
                (print('find call'))
                _, call_df_ = option_ltp(api=self.__breeze_api, stock_code=self.__stock_name, expiry_date=self.__expiry_date, right='call')
                call_df_ = call_df_[call_df_['ltp']>=put_ltp * 2/3]
                call_strike_= round(call_df_.tail(1)['strike_price'].values[0])
                print(call_strike_)
                self.call_strike = call_strike_
                self.trade(app, db, order_table, option_table,  userid)
                

            
            print(f"The difference is not less than 1/3. The high value is {high_value}, and 2/3 of the high value is {two_thirds_high_value}.")
    def trade(self, app, db, order_table, option_table, userid):
        order_api = FnoOrderManagement(api=self.__breeze_api) # first activate api
        
        try:
            call_id = order_api.place_order(stock_code=self.__stock_name, expiry_date=self.__expiry_date, quantity=self.quantity, right='call', strike_price=self.call_strike)
            try:
                search_data = {'ShortName': self.__stock_name, 'ExpiryDate': self.__expiry_date,'StrikePrice': self.call_strike }
                print(search_data)
                
                db_operate = TradeDecesion(app, db, self.__uid).check_database(model=OptionTable, filter_criteria=search_data)
                print(db_operate.Token)
            except Exception as e:
                print(e)
            save_data = {'u_no' : self.__uid, 'exchange_id' : call_id, 'exchange_code' : 'NFO', 'stock_name' : self.__stock_name, 'stock_token': db_operate.Token,
                                        'order_type' : 'sell', 'quantity' : self.quantity, 'expiry' : self.__expiry_date, 'strike_price' : self.call_strike, 
                                        'right' : 'call', 'user_id' : userid}
            
            save_order = TradeDecesion(app, db, self.__uid).save_in_loop(model=Order,data = save_data)
            put_id = order_api.place_order(stock_code=self.__stock_name, expiry_date=self.__expiry_date, quantity=self.quantity, right='put', strike_price=self.put_strike)
            # call strangle trade
        except Exception as e:
            print('Error in call-put of correct difference', e)
        else:
            print(call_id, put_id)