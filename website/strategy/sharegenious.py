try:
    from typing import Any
    import pandas as pd
    from sqlalchemy import create_engine, inspect, text
    from sqlalchemy.orm import sessionmaker
    from website.config import SQLALCHEMY_BINDS
    from website.utils import sql_quaries

except Exception as e:
    print('Error in strategy/sharegenious.py  ::', e)

class Sharegenious:
    def __init__(self, userid, data) -> None:
        self.__userid = userid
        self.__data = data
        self.__isin = self.filter_isin()
        self.calculate_history()

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
        filtered_df = merged_df[merged_df['high'] >= merged_df['last_high']].reset_index(drop=True)
        # filtered_df = filtered_df[filtered_df['t_date_low']]
        filtered_df['difference'] = ((filtered_df['high'] - filtered_df['last_high'])/filtered_df['high'])
        filtered_df = filtered_df.sort_values(by='difference', ascending=True).reset_index(drop=True)
        pd.options.display.max_columns = None
        print(merged_df)
        print(filtered_df)
        session.close()
        return filtered_df
    