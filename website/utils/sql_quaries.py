def complex_sql(table_names:list, ohlc:str, period:int, shorting ='ASC', **kwargs):
    counting = 0
    extra_filter = kwargs.get('by_id', None)
    
    statement = ''
    for table_name in table_names:
        
        # print(counting)
        if extra_filter != None:
            # print(extra_filter)
            filtered_value = (extra_filter[counting])
            # print(filtered_value)
            extra_filter_statement =  f"WHERE id <= {filtered_value}"
        else:
            extra_filter_statement = 'WHERE id IS NOT NULL'

        making_sql = f'''        
                    (SELECT table_name, id as id_{ohlc}, {ohlc}, t_date as t_date_{ohlc}
                    FROM (SELECT '{table_name}' AS table_name, id, {ohlc}, t_date
                        FROM {table_name}
                        {extra_filter_statement}

                        ORDER BY id DESC 
                        LIMIT {period}) AS t{counting} 
                        ORDER BY {ohlc} {shorting}
                    LIMIT 1)
                ''' 
        # print(making_sql)
        statement +=  making_sql
        counting += 1
        if counting == len(table_names):
            statement += ';'
        else:
            statement += "\n UNION ALL \n "
    
    return statement
        
def simple_quary(table_names:list, id_list:list, ohlc:str):
    counting = 0
    statement = ''
    for table_name in table_names:
        making_sql = f'''
                    (SELECT '{table_name}' as table_name, id as last_id, {ohlc} as last_{ohlc}
                        FROM {table_name}
                        WHERE id >= {id_list[counting]}
                        ORDER BY {ohlc} DESC
                        LIMIT 1
                    )
                    '''
        statement +=  making_sql
        counting += 1
        if counting == len(table_names):
            statement += ';'
        else:
            statement += "\n UNION ALL \n "
    return statement