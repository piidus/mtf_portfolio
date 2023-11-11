try:
    from flask import current_app
    from flask_login import current_user
    import os, datetime, math
    import pandas as pd
    from website.utils import Breeze_api
    from website.models import db, Algo
    # from historical_connection import history
    # from breeze_all import FnoOrderManagement   
except Exception as e:
    print('Import Error in strategy/Share Genious Strangle ::', e)

class ShareGeniousStrangle:
    '''
    Sale call, put on Open , Difference previous day high low
    '''
    def __init__(self, stock_name, expiry, lot, uid) -> None:
        self.__stock_name = stock_name
        self.__expiry_date = expiry
        self.__lot = lot
        self.__uid = uid
        self.__api =  self.breeze_connect()
        # self.__today_oepn, self.__high_low = self.previous_day_history()
    def breeze_connect(self):
        algo = Algo.query.filter_by(user_id = current_user.id).first()
        print(algo.session_time)
        Breeze_api(api_key=algo.api_key, api_secret=algo.api_secret, api_session=algo.api_sesion)