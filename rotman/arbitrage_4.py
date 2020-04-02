import signal
import requests # step 1
from time import sleep
import numpy as np

# This class definition allows us to print error messages and stop the program when needed
class ApiException(Exception):
    pass

# This signal handler allows for a graceful shutdown when CTRL+C is pressed
def signal_handler(signum, frame):
    global shutdown
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    shutdown = True
#CHECK PORT AND API KEY!!!
API_KEY = {'X-API-key':"apikey"} 
shutdown = False

# This helper method returns the current 'tick' of the running case
def get_tick(session):
    resp = session.get('http://localhost:9999/v1/case')
    if resp.ok:
        case = resp.json()
        return case['tick']
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
    mkt_buy_params = {'ticker': ticker, 'type': 'MARKET', 'quantity': quantity,'action': 'SELL'}
    resp = session.post('http://localhost:9999/v1/orders', params=mkt_buy_params)
    if resp.ok:
        mkt_order = resp.json()
        return mkt_order

def mkt_sell_limit(session, ticker, quantity, price):
    mkt_sell_params = {'ticker': ticker, 'type': 'LIMIT', 'price' : price,'quantity': quantity,'action': 'SELL'}
    resp = session.post('http://localhost:9999/v1/orders', params=mkt_sell_params)
    if resp.ok:
        mkt_order = resp.json()
        return mkt_order

def mkt_buy_limit(session, ticker, quantity, price):
    mkt_sell_params = {'ticker': ticker, 'type': 'LIMIT', 'price' : price,'quantity': quantity,'action': 'BUY'}
    resp = session.post('http://localhost:9999/v1/orders', params=mkt_sell_params)
    if resp.ok:
        mkt_order = resp.json()
        return mkt_order

def get_limit(session):
    resp = session.get("http://localhost:9999/v1/limits")
    if resp.ok:
        limit = resp.json()
        return limit[0]['gross_limit'], limit[0]['net_limit']
    raise ApiException('Authorization error. Please check API key.')

def cancel_all_orders(session):
    mkt_sell_params = {'all' : 1}
    resp = session.post('http://localhost:9999/v1/commands/cancel', params=mkt_sell_params)
    if resp.ok:
        mkt_order = resp.json()
        return mkt_order


def get_tenders(session):
    resp = session.get("http://localhost:9999/v1/tenders")
    if resp.ok:
        tenders = resp.json()
        if len(tenders) != 0:
            return tenders[0]
        else:
            return []
    raise ApiException('Authorization error. Please check API key.')

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
    
    #print(last_bids[0], last_asks[0])
    return last_bids[0], last_asks[0]

def main():
    with requests.Session() as s: 
        s.headers.update(API_KEY)  
        tick = get_tick(s)
        last_bids = []
        last_asks = []
        gross_limit, net_limit = get_limit(s)
        print("Gross limit: " + str(gross_limit))
        print("Net limit: " + str(net_limit))

        while tick > 0 and tick < 299 and not shutdown:
            cancel_all_orders(s)
            etf_last = get_securities(s, 'RITC', 'last')
            bull_last = get_securities(s, 'BULL', 'last')
            bear_last = get_securities(s, 'BEAR', 'last')
            usd_last = get_securities(s, 'USD', 'last')
            etf_position = get_securities(s, 'RITC', 'position')
            bull_position = get_securities(s, 'BULL', 'position')
            bear_position = get_securities(s, 'BEAR', 'position')


            last_bid, last_ask = last_bid_ask(s,last_bids, last_asks)

            tender_offer = get_tenders(s)
            if tender_offer != []:
                # if "BULL" in tender_offer["caption"]:
                #     ticker = "BULL"
                # elif "BEAR" in tender_offer["caption"]:
                #     ticker = "BEAR"
                # else:
                #     ticker = "RITC"

                if tender_offer["action"] == "SELL":
                    if tender_offer["price"] > (last_ask + .1):
                        resp = s.post("http://localhost:9999/v1/tenders/" + str(tender_offer["tender_id"]))
                        if resp.ok:
                            resp = resp.json()
                            

                else:
                    if tender_offer["price"] < (last_bid - .1):
                        resp = s.post("http://localhost:9999/v1/tenders/" + str(tender_offer["tender_id"]))
                        if resp.ok:
                            resp = resp.json()
                            

            
            # If ETF is overpriced, buy stocks, create ETF, and sell ETF
            # I
            if etf_last * usd_last > bull_last + bear_last + 0.1:
                #mkt_buy_limit(s, 'BULL', 10000, bull_last - .01)
                #mkt_buy_limit(s, 'BEAR', 10000, bear_last - .01)
                #print("Create ETF")
                mkt_sell_limit(s, 'RITC', 10000, etf_last + .01)
                mkt_sell_limit(s, 'RITC', 10000, etf_last + .01)
                mkt_sell_limit(s, 'RITC', 10000, etf_last + .01)
    
            #If ETF is underpriced, buy ETF, redeem ETF, and sell stocks
            elif etf_last * usd_last + 0.1 < bull_last + bear_last:
                mkt_buy_limit(s, 'RITC', 10000, etf_last - .01)
                mkt_buy_limit(s, 'RITC', 10000, etf_last - .01)
                mkt_buy_limit(s, 'RITC', 10000, etf_last - .01)
                #print("Redeem ETF")
                #mkt_sell_limit(s, 'BULL', 10000, bull_last + .01)
                #mkt_sell_limit(s, 'BEAR', 10000, bear_last + .01)

            else:
                if(etf_position <= -20000 or etf_position >= 20000):
                    if(etf_position < 0):
                        mkt_buy_limit(s, 'RITC', 10000, etf_last - .00)
                        mkt_buy_limit(s, 'RITC', 10000, etf_last - .00)
                    else:
                        mkt_sell_limit(s, 'RITC', 10000, etf_last + .00)
                        mkt_sell_limit(s, 'RITC', 10000, etf_last + .00)
                elif(etf_position <= -10000 or etf_position >= 10000):
                    if(etf_position < 0):
                        mkt_buy_limit(s, 'RITC', 10000, etf_last - .00)
                    else:
                        mkt_sell_limit(s, 'RITC', 10000, etf_last + .00)
                elif(etf_position <= -5000 or etf_position >= 5000):
                    if(etf_position < 0):
                        mkt_buy_limit(s, 'RITC', 5000, etf_last - .00)
                    else:
                        mkt_sell_limit(s, 'RITC', 5000, etf_last + .00)
                elif(etf_position <= -1000 or etf_position >= 1000):
                    if(etf_position < 0):
                        mkt_buy_limit(s, 'RITC', 1000, etf_last - .00)
                    else:
                        mkt_sell_limit(s, 'RITC', 1000, etf_last + .00)

                if(bull_position <= -5000 or bull_position >= 5000):
                    if(bull_position < 0):
                        mkt_buy_limit(s, 'BULL', 5000, bull_last - .00)
                    else:
                        mkt_sell_limit(s, 'BULL', 5000, bull_last + .00)

                if(bear_position <= -5000 or bear_position >= 5000):
                    if(bear_position < 0):
                        mkt_buy_limit(s, 'BEAR', 5000, bear_last - .00)
                    else:
                        mkt_sell_limit(s, 'BEAR', 5000, bear_last + .00)

            tick = get_tick(s)
        


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()