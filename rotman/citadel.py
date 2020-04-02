
def mkt_buy(session, ticker, quantity):
    mkt_buy_params = {'ticker': ticker, 'type': 'MARKET', 'quantity': quantity,'action': 'BUY'}
    print(mkt_buy_params)
    resp = session.post('http://localhost:9999/v1/orders', params=mkt_buy_params)
    print("RESP: ", resp)
    if resp.ok:
        print("FUCL YEA")
        mkt_order = resp.json()
        id = mkt_order['order_id']
        return 1
    else:
        #order not submitted
        return 0

def mkt_sell(session, ticker, quantity):
    mkt_sell_params = {'ticker': ticker, 'type': 'MARKET', 'quantity': quantity,'action': 'SELL'}
    resp = session.post('http://localhost:9999/v1/orders', params=mkt_sell_params)
    if resp.ok:
        mkt_order = resp.json()
        id = mkt_order['order_id']
        return 1
    else:
        #order not submitted
        return 0

def ticker_position(session, ticker):
    payload = {'ticker': ticker}
    resp = session.get('http://localhost:9999/v1/securities', params=payload)
    if resp.ok:
        me = resp.json()
        return me[0]['position']
    raise ApiException('Authorization error. Please check API key.')

def ticker_bid_ask(session, ticker):
    payload = {'ticker': ticker}
    print('ticker session:', session)
    resp = session.get('http://localhost:9999/v1/securities/book', params=payload)
    print('resp', resp)
    if resp.ok:
        book = resp.json()
     
        if(len(book['bids']) == 0 and len(book['asks']) == 0):
            return [], []
        elif(len(book['bids']) == 0):
            return [], book['asks'][0]['price']
        elif(len(book['asks']) == 0):
            return book['bids'][0]['price'], []
        else:
            return book['bids'][0]['price'], book['asks'][0]['price']
    raise ApiException('Authorization error. Please check API key.')

def main():
    with requests.Session() as s: 
            s.headers.update(API_KEY) 
            last_tick = get_tick(s) 
            ritc_max= 0
            
            while last_tick > 0 and last_tick < 300 and not shutdown:
                tick = get_tick(s)
                if(tick > last_tick):
                
                    RITC_pos = ticker_position(s, 'RITC')

                    #get current bull, bear, RITC prices 

                    potential_profit = #fill in profit eq abs(RITC) - abs(bull + bear)               
                    ritc_max = max(abs(potential_profit), abs(ho_max))

                    if (potential_profit < (.8*ho_max)):
                        if(RITC_pos < 0):
                            mkt_buy(s, '', )
                        
                    elif(RITC_pos > 0):
                        mkt_sell(s,'', )

                last_tick = tick


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()