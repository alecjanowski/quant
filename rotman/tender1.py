import signal
import requests # step 1
from time import sleep
import numpy as np

# This class definition allows us to print error messages and stop the program when needed
class ApiException(Exception):
    pass
# This signal handler allows for a graceful shutdown when CTRL+C is pressed

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
        print("bought 10k")
        mkt_order = resp.json()
        return mkt_order

def mkt_sell(session, ticker, quantity):
    mkt_sell_params = {'ticker': ticker, 'type': 'MARKET', 'quantity': quantity,'action': 'SELL'}
    resp = session.post('http://localhost:9999/v1/orders', params=mkt_sell_params)
    if resp.ok:
        print("sold 10k")
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

def get_limit(session):
    resp = session.get("http://localhost:9999/v1/limits")
    if resp.ok:
        limit = resp.json()
        return limit[0]['gross_limit'], limit[0]['net_limit']
    raise ApiException('Authorization error. Please check API key.')

def get_tenders(session):
    resp = session.get("http://localhost:9999/v1/tenders")
    if resp.ok:
        tenders = resp.json()
        if len(tenders) != 0:
            return tenders[0]
        else:
            return []
    raise ApiException('Authorization error. Please check API key.')

def last_bid_ask(s, last_prices):
    last = ticker_last(s)
    if((len(last_prices) <= 5)):
        last_prices.append(last)
    else:
        last_prices.pop(4)
        last_prices.insert(0, last)
    last_prices = reject_outliers(last_prices)

    return last_prices[(len(last_prices) - 1)]

def reject_outliers(data, m=2):
    new_list = []
    for i in range(len(data)):
        if abs(data[i] - np.mean(data)) <= m * np.std(data):
            new_list.append(data[i])
    return new_list

def ticker_last(session):
    payload = {'ticker': 'RITC'}
    resp = session.get('http://localhost:9999/v1/securities', params=payload)
    if resp.ok:
        me = resp.json()
        return me[0]['last']
    raise ApiException('Authorization error. Please check API key.')


def main():
    with requests.Session() as s: 
        s.headers.update(API_KEY)  
        tick = get_tick(s)
        gross_limit, net_limit = get_limit(s)
        print("Gross limit: " + str(gross_limit))
        print("Net limit: " + str(net_limit))

        last_prices = []
        
        while tick >= 0 and tick < 299 and not shutdown:
            etf_last = get_securities(s, 'RITC', 'last')
            bull_last = get_securities(s, 'BULL', 'last')
            bear_last = get_securities(s, 'BEAR', 'last')
            usd_last = get_securities(s, 'USD', 'last')
            etf_position = get_securities(s, 'RITC', 'position')

            last=last_bid_ask(s,last_prices)

            tender_offer = get_tenders(s)
            if tender_offer != []:
                # if "BULL" in tender_offer["caption"]:
                #     ticker = "BULL"
                # elif "BEAR" in tender_offer["caption"]:
                #     ticker = "BEAR"
                # else:
                #     ticker = "RITC"

                if tender_offer["action"] == "SELL":
                    if tender_offer["price"] > last:
                        resp = s.post("http://localhost:9999/v1/tenders/" + str(tender_offer["tender_id"]))
                        if resp.ok:
                            resp = resp.json()

                else:
                    if tender_offer["price"] < last:
                        resp = s.post("http://localhost:9999/v1/tenders/" + str(tender_offer["tender_id"]))
                        if resp.ok:
                            resp = resp.json()
            

            tick = get_tick(s)
        


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()