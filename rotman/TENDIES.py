import signal
import requests # step 1
from time import sleep
import numpy as np

#LAST YEAR GDP  #PROJECTED GDP #MANUFACTURED GOODS #SERVICES #RAW MATERIALS  #SUM OF LAST THREE  #MARGIN
#RIT VAL = sum of (projected - last year) + 1000

class ApiException(Exception):
    pass

def signal_handler(signum, frame):
    global shutdown
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    shutdown = True
#CHECK PORT AND API KEY!!!
API_KEY = {'X-API-key': 'apikey'} 
shutdown = False

def ticker_bid_ask(session, ticker):
    payload = {'ticker': ticker}
    resp = session.get('http://localhost:9999/v1/securities/book', params=payload)

    if resp.ok:
        book = resp.json()
        return book['bids'][0]['price'], book['asks'][0]['price']

    raise ApiException('Authorization error. Please check API key.')

def ticker_last(session):
    payload = {'ticker': 'RITC'}
    resp = session.get('http://localhost:9999/v1/securities', params=payload)
    if resp.ok:
        me = resp.json()
        return me[0]['last']
    raise ApiException('Authorization error. Please check API key.')

def get_tick(session):
    resp = session.get('http://localhost:9999/v1/case')
    if resp.ok:
        case = resp.json()
        return case['tick']
    raise ApiException('Authorization error. Please check API key.')

def reject_outliers(data, m=2):
    new_list = []
    for i in range(len(data)):
        if abs(data[i] - np.mean(data)) <= m * np.std(data):
            new_list.append(data[i])
    return new_list

def last_bid_ask(s, last_bids, last_asks):
    bid, ask = ticker_bid_ask(s, "RITC")
    if((len(last_bids) <= 5) and (len(last_asks) <= 5)):
        last_bids.append(bid)
        last_asks.append(ask)
    else:
        last_bids.pop(4)
        last_asks.pop(4)
        last_bids.insert(0, bid)
        last_asks.insert(0, ask)
    last_bids = reject_outliers(last_bids)
    last_asks = reject_outliers(last_asks)
    
    print(last_bids[0], last_asks[0])
    return last_bids[0], last_asks[0]
    
def main():
    last_bids = []
    last_asks = []

    with requests.Session() as s: 
        s.headers.update(API_KEY) 
        last_tick = get_tick(s)

        while last_tick > 0 and last_tick < 1800 and not shutdown: 
            last_bid_ask(s,last_bids, last_asks)
            last_tick = get_tick(s) 
            
if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()