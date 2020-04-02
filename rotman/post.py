import requests # step 1
API_KEY = {'X-API-key': 'NEZYSF2S'} # step 2

def main():
    with requests.Session() as s:
        s.headers.update(API_KEY)
        mkt_buy_params = {'ticker': 'RTM', 'type': 'MARKET', 'quantity': 5,
        'action': 'BUY'}
        resp = s.post('http://localhost:9999/v1/orders', params=mkt_buy_params)
        print(resp)
        if resp.ok:
            mkt_order = resp.json()
            id = mkt_order['order_id']
            
            print('The market buy order was submitted and has ID', id)
        else:
        
            print('The order was not successfully submitted!')

if __name__ == '__main__':
    main()