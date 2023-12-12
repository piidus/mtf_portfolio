try:
    from typing import Any
    import pandas as pd
    from sqlalchemy import create_engine, inspect, text
    from sqlalchemy.orm import sessionmaker
    import threading
    import datetime, time
    from website.config import SQLALCHEMY_BINDS
    from website.utils import sql_quaries, OHLCEngine, Icici_Connect
    from website.models import db, Advance_order, Algo
    

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
    
    def __new__(cls, uid, userid, data = ''):
        if cls.__instance is None:
            print('Create new Sharegenious Instance')
            cls.__instance = super(Sharegenious, cls).__new__(cls)
            print("Creating a new instance of MyClass")
            return cls.__instance
        else:
            print('Sharegenious already Instanciate-----------')
            return cls.__instance


    def __init__(self, userid,  uid, data='') -> None:
        self.__userid = userid
        self.__data = data
        self.__uid = uid
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
        
        ohlc = OHLCEngine(userid=userid, session_token=session_token)
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
            self.__ohlc_connection.start_point(scrip_code=self.scrip_list)
            start_first_time = self.test_function(status=self.__status)
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
            self.test_function( status=self.__status)
        print('----- Current status ::', self.__status)

    def filter_ltp(self, ohlc):
        '''
        First take ohlc and found value cross high price

        '''
        print(self.__data)
        for key, row in ohlc.items():
            target_value = float(row[0])
            filtered_row = self.__history[(self.__history['stockcode'] == key) & (self.__history['high'] < target_value)]
            if not filtered_row.empty :
                print(filtered_row, target_value)
            else:
                pass
        
        pass

    
    
    
    def test_function(self, status):        
        
        if status == 1:
            print('thread activate')
            print(self.__status,type(self.__status), datetime.datetime.now(), self.__instance)
            print(threading.activeCount())
            ohlc =self.__ohlc_connection.OHLC
            print(type(ohlc))
            self.filter_ltp(ohlc = ohlc.copy())
            time.sleep(5)
            t = threading.Thread(target=self.test_function, args=(self.__status,))
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
        print(len(new_list), len(table_names)), len(self.__data['isin'])
        return new_list


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
        # Create a dictionary mapping 'isin' values to 'token' values in df1
        isin_token_mapping = dict(zip(self.__data['isin'].str.lower(), self.__data['token']))
        # Create a new 'token' column in df2 by mapping lowercase 'isin' values to 'token' values
        filtered_df['token'] = filtered_df['table_name'].str.lower().map(isin_token_mapping)
        # Create a dictionary mapping 'isin' values to 'stock_code' values in df1
        isin_stockcode_mapping = dict(zip(self.__data['isin'].str.lower(), self.__data['Stock Code']))
        # Create a new 'token' column in df2 by mapping lowercase 'isin' values to 'token' values
        filtered_df['stockcode'] = filtered_df['table_name'].str.lower().map(isin_stockcode_mapping)
        # print(filtered_df)
        del merged_df, isin_token_mapping
        session.close()
        return filtered_df
    