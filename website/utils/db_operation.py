class TradeDecesion:
    '''it takes all trade decesion and execute 
        mandatory app, uid,
        advance : Advance model
        order : Order model
        right : call/put
        strike: strike
    '''
    def __init__(self, app, db, uid, **kwargs) -> None:
        self.__app = app
        self.__db = db
        self.__uid = uid
        self.__advance_model = kwargs.get('advance', None)
        self.__order_model = kwargs.get('order', None)
    
    def check_database(self,  model:object, filter_criteria:dict):
        '''in thread check database return row'''
        try:
            with self.__app.app_context():
                try:
                    session = self.__db.session()
                    query = session.query(model)

                    for column_name, filter_value in filter_criteria.items():
                        column = getattr(model, column_name, None)
                        if column is not None:
                            query = query.filter(column == filter_value)

                    search_data = query.first()
                    session.close()
                    # print(search_data.u_no)
                except Exception as e:
                    print('in utils QueryExternal:', e)
                else:
                    if search_data:
                        return search_data
        except Exception as e:
            print('Exception in __check_database:', e)