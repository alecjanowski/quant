import signal
import requests # step 1
from time import sleep

# This class definition allows us to print error messages and stop the program when needed
class ApiException(Exception):
    pass

# This signal handler allows for a graceful shutdown when CTRL+C is pressed
def signal_handler(signum, frame):
    global shutdown
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    shutdown = True
#CHECK PORT AND API KEY!!!
API_KEY = {'X-API-key':"NEZYSF2S"} 
shutdown = False

# This helper method returns the current 'tick' of the running case
def get_tick(session):
    resp = session.get('http://localhost:9999/v1/case')
    if resp.ok:
        case = resp.json()
        return case['tick']
    raise ApiException('Authorization error. Please check API key.')

def ticker_bid_ask(session, ticker):
    payload = {'ticker': ticker}
    resp = session.get('http://localhost:9999/v1/securities/book', params=payload)
    if resp.ok:
        book = resp.json()
        return book['bids'][0]['price'], book['asks'][0]['price']
    raise ApiException('Authorization error. Please check API key.')

def get_securities(session, ticker, key):
    payload = {'ticker': ticker}
    resp = session.get('http://localhost:9999/v1/securities', params=payload)
    if resp.ok:
        security = resp.json()
        return security[0][key]
    raise ApiException('Authorization error. Please check API key.')

def get_order_detail(session, ticker, id):
    payload = {'ticker': ticker}
    resp = session.get("http://localhost:9999/v1/orders/" + str(id), params=payload)
    if resp.ok:
        order = resp.json()
        return order
    raise ApiException('Authorization error. Please check API key.')

def mkt_buy(session, ticker, quantity):
    mkt_buy_params = {'ticker': ticker, 'type': 'MARKET', 'quantity': quantity,'action': 'BUY'}
    resp = session.post('http://localhost:9999/v1/orders', params=mkt_buy_params)
    if resp.ok:
        mkt_order = resp.json()
        return mkt_order

def mkt_sell(session, ticker, quantity):
    mkt_sell_params = {'ticker': ticker, 'type': 'MARKET', 'quantity': quantity,'action': 'SELL'}
    resp = session.post('http://localhost:9999/v1/orders', params=mkt_sell_params)
    if resp.ok:
        mkt_order = resp.json()
        return mkt_order

def enqueue_cost_after_order(session, queue):
    unrealizedPL = get_securities(session, 'RITC', 'unrealized')
    ask = get_securities(session, 'RITC', 'ask')
    position = get_securities(session, 'RITC', 'position')
    if position != 0:
        cost = ask - unrealizedPL/position
        queue.append(cost)
        return queue
    else:
        queue.append(get_securities(session, 'RITC', 'last'))
        return queue




def main():
    with requests.Session() as s: 
        s.headers.update(API_KEY)  
        tick = get_tick(s)
        
        i = 0
        queue_sell = []
        queue_buy = []
        sell_counter = 0
        buy_counter = 0
        # while i < 100:
        while tick > 0 and tick < 299 and not shutdown:
            etf_last = get_securities(s, 'RITC', 'last')
            bull_last = get_securities(s, 'BULL', 'last')
            bear_last = get_securities(s, 'BEAR', 'last')
            usd_last = get_securities(s, 'USD', 'last')
            position = get_securities(s, 'RITC', 'position')

            if len(queue_sell) != 0:
                if queue_sell[0] > etf_last + 0.3:
                    if position < 0:
                        mkt_buy(s, 'RITC', -position)
                    else:
                        mkt_buy(s, 'RITC', 1000)
                    del queue_sell[0]
            if len(queue_buy) != 0:
                if queue_buy[0] + 0.3 < etf_last:
                    if position > 0:
                        mkt_sell(s, 'RITC', position)
                    else:
                        mkt_sell(s, 'RITC', 1000)
                    del queue_buy[0]

            #If ETF is overpriced, short ETF and buy ETF at a cheaper price later
            if etf_last * usd_last > bull_last + bear_last + 0.3:
                if position > 0:
                    mkt_sell(s, 'RITC', position)
                else:
                    mkt_sell(s, 'RITC', 1000)
                queue_sell = enqueue_cost_after_order(s, queue_sell)
                sell_counter += 1
                
    
            #If ETF is underpriced, buy ETF and sell ETF at a higher price later
            elif etf_last * usd_last + 0.3 < bull_last + bear_last:
                if position < 0:
                    mkt_buy(s, 'RITC', -position)
                    print(mkt_buy)
                else:
                    mkt_buy(s, 'RITC', 1000)
                queue_buy = enqueue_cost_after_order(s, queue_buy)
                buy_counter += 1
                

            tick = get_tick(s)
            i += 1
        


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()









    


