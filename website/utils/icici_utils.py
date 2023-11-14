try:
    import http
    import pandas as pd
    import math, datetime, json
    from .icici_connections import Breeze_api, Icici_Connect
except Exception as e:
    print('error in utils.iciciuils', e)


# Get Expiry Dates  
def expiry_dates(api_key, api_secrect, api_session, stock_name, strike_pric):
    try:
        api = Breeze_api(api_key=api_key, api_secret=api_secrect, api_session=api_session)
        # print(api)
        option_data = api.get_option_chain_quotes(stock_code=stock_name,
                        exchange_code="NFO",
                        product_type="options",
                        strike_price=int(strike_pric),
                        right="call")
        df = pd.DataFrame(option_data['Success'])
        if df.empty:
            raise ValueError('Enter correct amount')
        # List of Expiry dates
        df['expiry_date'] = pd.to_datetime(df['expiry_date']).dt.date
        df = df['expiry_date'].tolist()
        data_to_insert = df
        # print(df)
        return data_to_insert
    except Exception as e:
        print(e)

# STRIKE PRICE HIGH LOW 
def round_to_multiple(stock_name, strike_price, direction= ''):
    
    '''RETURN : strike price and quantity'''
    strike_price = int(strike_price)
    token_quantity = {'NIFTY': 50,
                      'CNXBAN': 15,
                      'NIFFIN': 40}
    quantity = token_quantity[stock_name]
    if stock_name in ['NIFTY', 'NIFIN']:
        multiple = 50
    elif stock_name in ['CNXBAN']:
        multiple = 100
    direction = direction
    if direction == 'nearest':
        rounded_strike =  multiple * round(strike_price / multiple)
    elif direction == 'up':
        rounded_strike =  multiple * math.ceil(strike_price / multiple)
        
    elif direction == 'down':
        rounded_strike =  multiple * math.floor(strike_price / multiple)
    else:
        rounded_strike =  multiple * round(strike_price / multiple)
    
    return rounded_strike, quantity

def option_ltp(api, stock_code,  expiry_date, right='', strike = ''):
        
        data = api.get_option_chain_quotes(stock_code=stock_code,
                    exchange_code="NFO",
                    product_type="options",
                    expiry_date=expiry_date,
                    strike_price = strike,
                    right=right)
        ltp = data['Success'][0]['ltp']
        df = pd.DataFrame(data['Success'])
        df = df[df['ltp'] > 0]
        df = df[['strike_price', 'ltp']]
        # print(df)
        return ltp, df

class FnoOrderManagement:
    def __init__(self, api) -> None:
        try:
            self.api = api
        except Exception as e:
            print('Error in Api connect', e)
    # else:
    def squareoff(self, stock_code, expiry_date, right, strike_price):
        data = self.api.square_off(exchange_code="NFO",
                        product="options",
                        stock_code= stock_code, #"NIFTY",
                        expiry_date= expiry_date, #"2023-09-28T06:00:00.000Z",
                        right=right, #"Call",
                        strike_price=strike_price, #"20250",
                        action="buy",
                        order_type="market",
                        validity="day",
                        stoploss="0",
                        quantity="50",
                        price="0",
                        validity_date=datetime.datetime.now().replace(hour=16, minute=0, second=0,microsecond=0).isoformat()+'.000Z',
                        trade_password="",
                        disclosed_quantity="0")
        print('------------ option squareoff details------------')
        print(data)
    def place_order(self, stock_code, expiry_date, quantity, right, strike_price, order_type="market"):
        try:
            data = self.api.place_order(stock_code=stock_code, #'NIFTY'
                        exchange_code="NFO",
                        product="options",
                        action="sell",
                        order_type=order_type,
                        stoploss="",
                        quantity=quantity,
                        price="",
                        validity="day",
                        validity_date=datetime.datetime.now().replace(hour=16, minute=0, second=0,microsecond=0).isoformat()+'.000Z',
                        disclosed_quantity="0",
                        expiry_date=expiry_date,
                        right= right, #"call",
                        strike_price=strike_price)
            if data['Status'] == 200:
                print('------------ option order details------------')
                print(data['Success'])
                order_id = data['Success']['order_id']
                print(order_id)
                return order_id
            else: 
                print(data)
        except Exception as e:
            print(e)
    def tradelist(self):
        trade_list = self.api.get_trade_list(from_date=datetime.datetime.now().replace(hour=9, minute=0, second=0,microsecond=0).isoformat(),
                        to_date=datetime.datetime.now().replace(microsecond=0).isoformat(),
                        exchange_code="NFO",
                        product_type="",
                        action="",
                        stock_code="")
        print(trade_list)
        data = trade_list['Success']
        print(data)
        if len(data) != 0 :
            df = pd.DataFrame(data)
            print(df)
        return df
    def margin(self):
        total = self.api.get_margin(exchange_code="NFO")
        limit = total['Success']['cash_limit']
        print(limit)

    def order_details(self, order_id):
        D = self.api.get_order_detail(exchange_code="NFO",
                        order_id=order_id)
        print(D)