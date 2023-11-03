try:
    import pandas as pd
    import math
    from breeze_connect import BreezeConnect
except Exception as e:
    print('error in utils.icici_connections : ', e)
# Breeze api connections ---------------------------
def breeze_connection(api, secrect, session):
        __icici = BreezeConnect(api_key=api)
        __icici.generate_session(api_secret=secrect, session_token=session)
        return __icici
class Breeze_api:
    __instance = None

    def __new__(cls, api_key, api_secret, api_session ):
        if cls.__instance is None:
            print('Connecting Breeze......')
            new_api_connection = breeze_connection(api_key, api_secret, api_session )
            cls.__instance = super(Breeze_api, cls).__new__(cls)
            cls.__instance = new_api_connection
            return cls.__instance
        else:
            print('WARNING : There\'s already an instance Breeze of connection')
            return cls.__instance

    def __init__(self, api_key, api_secret, api_session ):
        
        print('Connected to the Breeze!')
        pass
