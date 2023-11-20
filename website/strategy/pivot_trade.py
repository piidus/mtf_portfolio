try:
    import pandas as pd
    import datetime
    from website.utils import Breeze_api
    from website.models import Algo
except Exception as e:
    print('Error in Import - strategy/pivot_trade '. e)

class PivotTrading:

    def __init__(self, userid) -> None:
        self.__userid = userid
    
    def demoprint(self):
        print(self.__userid)
    def calculate_pivot(self, stockname):
        '''
        history for last day> Calculate pivot
        '''
        algo = Algo.query.filter_by(user_id = self.__userid).first()

        # Connection api for history
        self.__api = Breeze_api(api_key=algo.api_key, api_secret=algo.api_secret, api_session=algo.api_sesion)
                                 
        from_date = (datetime.datetime.now() -datetime.timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%S.000Z')
        to_date = (datetime.datetime.now().replace(hour=17) - datetime.timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S.000Z')
        history_ = self.__api.get_historical_data(interval="1day",
                            from_date= from_date,
                            to_date= to_date,
                            stock_code=stockname,  #CNXBAN
                            exchange_code="NSE")
        if history_['Status'] == 200:
            data = pd.DataFrame(history_['Success'])
            data = data[['datetime', 'open', 'high', 'low', 'close']].tail(2) # Get Last Data
            data = data.head(1)
            converted_data : dict = {'open': 'float', 'high': 'float', 'low': 'float', 'close':'float'}
            data = data.astype(converted_data)
            # Calculate Pivot 
            self.pivot_calculation(open=data['open'].values[0], high=data['high'].values[0], low=data['low'].values[0], close=data['close'].values[0])
        print(data)
    
    def pivot_calculation(self, open, high, low, close):
        # print(open, high, low, close)
        # P = (O + H + L + C) / 4
        p = round(((open+high+low+close)/4), 2)
        # BC = (H + L) / 2
        bc = round((high + low)/2, 2)
        # TC = (P - BC) + P
        tc = round((p - bc) + p , 2)
        # R1 = P + (P − L) = 2×P − L
        r1 = round((p + (p - low)), 2)
        # S1 = P − (H − P) = 2×P − H
        s1 = round((p - (high - p)), 2)
        # R2 = P + (H − L)
        r2 = round((p + (high - low)), 2)
        # S2 = P − (H − L)
        s2 = round((p - (high - low)),2)
        # R3 = H + 2×(P − L) = R1 + (H − L)
        r3 = round( high + 2*(p - low), 2)
        # S3 = L − 2×(H − P) = S1 − (H − L)
        s3 = round((low - 2 * high - p) , 2)
        
        pivot_points = r3, r2, r1, bc, p, tc, s1, s2, s3, high, low
        return list(pivot_points)
        
