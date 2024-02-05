
try:
    from typing import Any
    import pandas as pd
    from sqlalchemy import create_engine, inspect, text
    from sqlalchemy.orm import sessionmaker
    import threading
    import datetime, time
    from website.config import SQLALCHEMY_BINDS
    from website.utils import sql_quaries, OHLCEngine, Icici_Connect, TradeDecesion
    from website.models import db, Advance_order, Algo, Trigger
    from flask_login import current_user

except Exception as e:
    print('Error in strategy/sharegenious.py  ::', e)
def order_management(userid, uid):
    '''
    First check uid already present or not!
    if uid not present create new order
    
    return uid 
    '''
    pass


class Sharegenious:
    __instance = None
    
    def __new__(cls, uid, userid, data = '', **kwargs):
        if cls.__instance is None:
            print('Create new Sharegenious Instance')
            cls.__instance = super(Sharegenious, cls).__new__(cls)
            print("Creating a new instance of MyClass")
            return cls.__instance
        else:
            print('Sharegenious already Instanciate-----------')
            return cls.__instance


    def __init__(self, userid,  uid, data='', **kwargs) -> None:
        self.__userid = userid
        self.__data = data
        self.__uid = uid
        self.__app = kwargs.get('app', None)
        self.__status = 0
        self.__ohlc_connection = self.establish_connection()
    
    def __str__(self) -> str:
        return f"Sharegenious uid :: {self.__uid}"

    def delete_instance(self):   
        self.__ohlc_connection.close_point()     
        return self
    
    def establish_connection(self):
        # find userid and session key
        algo = Algo.query.filter_by(user_id = self.__userid).first()
        print(algo.api_key, algo.api_sesion)
        userid, session_token, total_session_token = Icici_Connect(api_key=algo.api_key, api_session=algo.api_sesion)
        print(userid, session_token)
        ohlc = OHLCEngine(userid=userid, session_token=session_token)
        if ohlc == -1:
            return -1
        return ohlc
        
        
    def maintain_order_status(self, status = 1):
        '''
            status = 1 : resume trade
            status = 0 : pause trade
            status = -1 : delete trade 
            status = 3 : start trade
        '''
        if status == 3:
            # Set Advance order 
            adv = Advance_order(strategy = 'sharegenious', u_no = self.__uid, user_id = self.__userid)
            db.session.add(adv)
            db.session.commit()
            self.__isin = self.filter_isin()
            self.__history = self.calculate_history()
            self.__status = 1
            scrip_list = self.__history['token'].to_list()
            self.scrip_list = ["4.1!"+str(item) for item in scrip_list]
            conn = self.__ohlc_connection.start_point(scrip_code=self.scrip_list)
            if conn == -1:
                return -1
            start_first_time = self.test_function(status=self.__status, app=self.__app)
        elif status == 0: #pause trade
            print('it pause the trade')
            self.__status = 0
            self.__ohlc_connection.pause_point(script_code=self.scrip_list)
        elif status == 1:
            print('it resume trade')
            
            self.__status = 1
            scrip_list = self.__history['token'].to_list()
            self.scrip_list = ["4.1!"+str(item) for item in scrip_list]
            self.__ohlc_connection.start_point(scrip_code=self.scrip_list)
            self.test_function( status=self.__status,app= self.__app)
        print('----- Current status ::', self.__status)

    def filter_ltp(self, ohlc, app):
        '''
        First take ohlc and found value cross high price

        '''
        # print(self.__data)
        for key, row in ohlc.items():
            target_value = float(row[0])
            filtered_row = self.__history[(self.__history['stockcode'] == key) & (self.__history['high'] < target_value)]
            if not filtered_row.empty :
                print(filtered_row, target_value)
                # print(filtered_row['token'].values[0])
                # final_value = value + (value * (percent / 100))
                target = round(filtered_row['last_high'].values[0] + (filtered_row['last_high'].values[0] * (15 /100)),2)
                user_id = self.__uid[:1]
                print(user_id)
                # Save the data in for loop
                save_data = {'strategy': 'sharegenious', 'symbol': key, 'token': filtered_row['token'].values[0], 'target' : target,
                             'full_name': filtered_row['fullname'].values[0], 'isin': filtered_row['isin'].values[0],
                             'stop_loss': filtered_row['low'].values[0], 'ex1': filtered_row['t_date_low'].values[0], 'ex2': user_id}
                try:
                    TradeDecesion(app=app, db=db, uid=self.__uid).save_in_loop(model=Trigger, data=save_data)
                except Exception as e:
                    print('error in save in loop')
                else:
                    # df.drop(df[df['token'] == 252].index)
                    self.__history = self.__history.drop(self.__history[self.__history['token'] == filtered_row['token'].values[0]].index)
                
            else:
                print('no Trigger')
        

    
    
    
    def test_function(self, status, app):        
        
        if status == 1:
            print('thread activate')
            print(self.__status,type(self.__status), datetime.datetime.now(), self.__instance)
            print(threading.activeCount())
            ohlc =self.__ohlc_connection.OHLC
            # print((ohlc))
            self.filter_ltp(ohlc = ohlc.copy(), app=app)
            time.sleep(5)
            t = threading.Thread(target=self.test_function, args=(self.__status, app))
            t.start()
        else:
            
            print('problem')
            

        # print(self.__isin)
    def db_connection(self):
        database_url = SQLALCHEMY_BINDS['stock']
        engine = create_engine(database_url)
        return engine

    def filter_isin(self):
        self.engine = self.db_connection()
        inspector = inspect(self.engine)
        table_names = inspector.get_table_names()
        # print(table_names)
        new_list = [i.lower()  for i in self.__data['isin'] if i.lower() in table_names]
        triggered_list = Trigger.query.filter(Trigger.date == datetime.datetime.now().date(), Trigger.strategy == 'sharegenious')
        triggered_token = [triger.isin.lower() for triger in triggered_list]
        print(('*'*100), triggered_token)
        # first_list = [name for name in first_list if name not in second_list]
        new_list_ = [isin for isin in new_list if isin not in triggered_token]
        # print(new_list_)
        print(len(new_list), len(new_list_), len(table_names)), len(self.__data['isin'])
        return new_list_


        # # Create a session
        # Session = sessionmaker(bind=engine)
        # session = Session()
    def calculate_history(self):
        session = sessionmaker(bind=self.engine)
        session = session()
        print('-----query start')
        # find 20 day low
        first_query = sql_quaries.complex_sql(table_names=self.__isin, ohlc='low', period=20)
        lowest_low = session.execute(text(first_query)).fetchall()
        lowest_low = pd.DataFrame(lowest_low)
        # print(lowest_low.head())
        id_list = list(lowest_low['id_low'])
        # find previous 20 day high from lowest low id
        second_query = sql_quaries.complex_sql(table_names=self.__isin, ohlc='high', period=20, shorting='DESC', by_id = id_list)
        previous_high = session.execute(text(second_query)).fetchall()
        previous_high = pd.DataFrame(previous_high)
        # print(previous_high.head())
        # find last few days high to check is it already triggred or not
        third_query = sql_quaries.simple_quary(table_names=self.__isin, id_list=id_list, ohlc='high')
        # print(third_query)
        last_high = session.execute(text(third_query)).fetchall()
        last_high = pd.DataFrame(last_high)
        # print(last_high)

        merged_df = lowest_low.merge(previous_high, how='inner', on='table_name')
        merged_df = merged_df.merge(last_high, how='inner', on='table_name')
        filtered_df = merged_df[merged_df['high'] > merged_df['last_high']].reset_index(drop=True)
        # filtered_df = filtered_df[filtered_df['t_date_low']]
        filtered_df['difference'] = ((filtered_df['high'] - filtered_df['last_high'])/filtered_df['high'])
        filtered_df = filtered_df.sort_values(by='difference', ascending=True).reset_index(drop=True)
        pd.options.display.max_columns = None
        # print(merged_df)
        # print(self.__data)
        # Convert 'isin' column in df1 to lowercase
        self.__data['lower_isin'] = self.__data['isin'].str.lower()
        # Merge df1 and df2 on the lowercase 'isin' and 'table_name' columns
        m1 = filtered_df.merge(self.__data, how='left', left_on='table_name', right_on='lower_isin')
        # Drop the redundant 'isin_lower' column
        m1 = m1.drop(columns=['lower_isin'])
        m1 = m1.rename(columns={'shortcode':'stockcode'})
        print('--------------------------------------------')
        print(m1)
        m1.to_csv(path_or_buf='website/static/data/csv/history.csv')
        
        session.close()
        return m1
    