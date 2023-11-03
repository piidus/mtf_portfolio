try:
    import pandas as pd
    import math
    from .icici_connections import Breeze_api
except Exception as e:
    print('error in utils.iciciuils', e)
    
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