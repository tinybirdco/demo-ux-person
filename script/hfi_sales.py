import pandas as pd
import requests
import json
from datetime import datetime

def send_to_tb(ds: str, token: str, messages: list):
    params = {
        'name': ds,
        'token': token,
        'wait': 'false',
    }
    data = '\n'.join(json.dumps(m) for m in messages)
    r = requests.post('https://api.tinybird.co/v0/events', 
                  params=params, 
                  data=data
                 )

def send_hfi(datasource="sales",
             events=5000,
             silent=True
             ):
    
    with open ("./.tinyb") as tinyb:
        token = json.load(tinyb)['token']
        
    df=pd.read_csv('./datasources/fixtures/transactions_train.csv')
    print(df.iloc[0])    
        
    nd = []
    
    for i in range(len(df)):
        message = {
            'datetime': datetime.utcnow().isoformat(),
            'customer_id': df.customer_id.iloc[i],
            'article_id': int(df.article_id.iloc[i]),
            'price': round(df.price.loc[i]*1000,2)
          }
        
        nd.append(message) 
        
        if len(nd) == events:
            send_to_tb(datasource, token, nd)
            nd = []
        if not(silent):
            print(message) 
    
    send_to_tb(datasource, token, nd)
    nd = []

if __name__ == '__main__':
    send_hfi()
