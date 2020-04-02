import signal
import requests # step 1
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

class ApiException(Exception):
    pass

def signal_handler(signum, frame):
    global shutdown
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    shutdown = True
#CHECK PORT AND API KEY!!!
API_KEY = {'X-API-key': 'apikey'} 
shutdown = False

def get_tick(session):
    resp = session.get('http://localhost:9999/v1/case')
    if resp.ok:
        case = resp.json()
        return case['tick']
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

def ticker_position(session, ticker):
    payload = {'ticker': ticker}
    resp = session.get('http://localhost:9999/v1/securities', params=payload)
    if resp.ok:
        me = resp.json()
        return me[0]['position']
    raise ApiException('Authorization error. Please check API key.')

def ticker_unrealized(session, ticker):
    payload = {'ticker': ticker}
    resp = session.get('http://localhost:9999/v1/securities', params=payload)
    if resp.ok:
        me = resp.json()
    
        return me[0]['unrealized']
    raise ApiException('Authorization error. Please check API key.')

def ticker_realized(session, ticker):
    payload = {'ticker': ticker}
    resp = session.get('http://localhost:9999/v1/securities', params=payload)
    if resp.ok:
        me = resp.json()
    
        return me[0]['realized']
    raise ApiException('Authorization error. Please check API key.')

def news(session):
    resp = session.get('http://localhost:9999/v1/news')
    if resp.ok:
        news = resp.json()
        text = news[0]['body']
        supply = 'supply' in text or 'surplus' in text 
        demand = 'demand' in text or 'shortage' in text
        print('__________NEWS' + str(news[0]['news_id']) + '___________\n\n')
        if(supply and not demand):
            print('SELL CL! Prices dropping')
        elif(demand and not supply):
            print('BUY CL! Prices rising')
        else:
            print('ya algo fucked up')
        print(text)
        print('\n\n__________NEWS___________')
        return 
    raise ApiException('Authorization error. Please check API key.')

def get_news_id(session):
    resp = session.get('http://localhost:9999/v1/news')
    if resp.ok:
        news = resp.json()
        return news[0]['news_id']
    raise ApiException('Authorization error. Please check API key.')

def main():
    INTERVAL = 2 #ticks
    clm = []
    hom = []
    rbm = []
    rcam = []
       
    clu = [0,0]
    hou =[0,0]
    rbu = [0,0]
    rcau = [0,0]

    cl_real = 0
    ho_real = 0 
    rb_real = 0
    rca_real = 0

    #tick is essentially the position in time from 0 to 960
    with requests.Session() as s: 
        s.headers.update(API_KEY)  
        last_tick = get_tick(s)
        ticker_position(s, 'HO-2F')
        news_id = 0

        ho_max = 0
        cl_max = 0
        rb_max = 0
        rca_max = 0
        
        last_clp = ticker_position(s, 'CL')
        last_hop = ticker_position(s, 'HO-2F')
        last_rbp = ticker_position(s, 'RB-2F')
        last_rcap = ticker_position(s, 'RCA')

        fig, axs = plt.subplots(2)
        plt.subplots_adjust(hspace=.5)
        plt.autoscale(enable=True, axis='both', tight=None)
        #uncomment to get all time steps
        while last_tick > 0 and last_tick < 960 and not shutdown: 
            tick = get_tick(s)
            comp = get_news_id(s)
       
            if(comp > news_id):
                news(s)
                news_id = comp          

            if(tick > last_tick):
             
                clp = ticker_position(s, 'CL')
                hop = ticker_position(s, 'HO-2F')
                rbp = ticker_position(s, 'RB-2F')
                rcap = ticker_position(s, 'RCA')
                
                if(last_clp != clp):
                    last_clp = clp
                    cl_real = ticker_realized(s, 'CL')
                    
                if(last_hop != hop):
                    last_hop = hop
                    ho_real = ticker_realized(s, 'HO-2F')
                
                if(last_rbp != rbp):
                    last_rbp = rbp
                    rb_real = ticker_realized(s, 'RB-2F')

                if(last_rcap != rcap):
                    last_rcap = rcap
                    rca_real = ticker_realized(s, 'RCA')

           
                ho_potential_profit = (ticker_realized(s, 'HO-2F') - ho_real) + ticker_unrealized(s, 'HO-2F')               
                
                axs[0].scatter(tick, ho_potential_profit)
                
                '''
                if(hop < 0):
                    axs[0].set_title("mkt BUY! " + str(hop) + " HO", fontsize=8)
                elif(hop > 0):
                    axs[0].set_title("mkt SELL! " + str(hop) + " HO", fontsize=8)
                else:
                    axs[0].set_title("HO .. wait for indication", fontsize=8)
            
                axs[0].set_xlim((tick-30), tick+10)
                axs[0].set_ylim((ho_potential_profit - 20000, ho_potential_profit + 20000))
                plt.pause(0.05)
                '''
             
                rb_potential_profit = (ticker_realized(s, 'RB-2F') - rb_real) + ticker_unrealized(s, 'RB-2F')               
                axs[1].scatter(tick, rb_potential_profit)
                if(rbp < 0):
                    axs[1].set_title("mkt BUY! " + str(rbp) + " RB", fontsize=8)
                elif(rbp > 0):
                    axs[1].set_title("mkt SELL! " + str(rbp) + " RB", fontsize=8)
                else:
                    axs[1].set_title("RB .. wait for indication", fontsize=8)
                axs[1].set_xlim((tick-30), tick+10)
                axs[1].set_ylim((rb_potential_profit - 20000, rb_potential_profit + 20000))
                plt.pause(0.05)

                #CL watch the tender offers
                #RCA bid under 50 but they will close at 50, usually at last price will get the purchase but I'd want to bid lower
                # < 50 will get the job done

                """
                if(last_tick % 5 == 0):
                    print(last_tick)

                last_tick = tick
                """
        

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()

"""

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

main():

    with requests.Session() as s: 
            s.headers.update(API_KEY) 
            last_tick = get_tick(s) 
            ritc_max= 0
            
            while last_tick > 0 and last_tick < 300 and not shutdown:
                tick = get_tick(s)
                if(tick > last_tick):
                
                bull_pos = ticker_position(s, 'BULL')
                bear_pos = ticker_position(s, 'BEAR')
                RITC_pos = ticker_position(s, 'RITC')


                potential_profit = (ticker_realized(s, 'HO-2F') - ho_real) + ticker_unrealized(s, 'HO-2F')               
                ritc_max = max(abs(potential_profit), abs(ho_max))

                if (ho_potential_profit < (.8*ho_max)):
                    if(hop < 0):
                        mkt_buy(s, '', )
                    
                    elif(hop > 0):
                        mkt_sell(s,'', )

                last_tick = tick
"""
#OPENING MY POSITION
    #the central question is whether or not the price is going to be more expensive or less expensive in future
    #tenders are going to be for CRUDE OIL
    

    #BID low for RCA???

    #CLOSING MY POSITION
    #tell me when to buy if position is negative
    #tell me when to sell if position is positive
"""
    if(len(clu) == 2):
        clu.pop(1)
        clu.insert(0, ticker_unrealized(s, 'CL'))
    else:
        clu.insert(0, ticker_unrealized(s, 'CL'))
    if(len(hou) == 2):
        hou.pop(1)
        hou.insert(0, ticker_unrealized(s, 'HO-2F'))
    else:
        hou.insert(0, ticker_unrealized(s, 'HO-2F'))
    if(len(rbu) == 2):
        rbu.pop(1)
        rbu.insert(0, ticker_unrealized(s, 'RB-2F'))
    else:
        rbu.insert(0, ticker_unrealized(s, 'RB-2F'))
    if(len(rcau) == 2):
        rcau.pop(1)
        rcau.insert(0, ticker_unrealized(s, 'RCA'))
    else:
        rcau.insert(0, ticker_unrealized(s, 'RCA'))
    

    if(len(clm) == 10):
        clm.pop(9)
        clm.insert(0, (clu[0] - clu[1]))
    else:
        clm.insert(0, (clu[0] - clu[1]))
    if(len(hom) == 10):
        hom.pop(9)
        hom.insert(0, (hou[0] - hou[1]))    
    else:
        hom.insert(0, (hou[0] - hou[1]))
    if(len(rbm) == 10):
        rbm.pop(9)
        rbm.insert(0, (rbu[0] - rbu[1]))
    else:
        rbm.insert(0, (rbu[0] - rbu[1]))
    if(len(rcam) == 10):
        rcam.pop(9)
        rcam.insert(0,(rcau[0] - rcau[1]))
    else:
        rcam.insert(0,(rcau[0] - rcau[1]))

    print(sum(hom))
    if((hop < 0) and (sum(hom) > 2) and (hou[0] > 0)):
        print("mkt BUY! " + str(hop) + " HO  ...")
    elif((hop > 0) and (sum(hom) < -2) and (hou[0] > 0)):
        print("mkt SELL! " + str(hop) + " HO  ...")
"""
'''
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

def lmt_sell(session, ticker, quantity):
mkt_sell_params = {'ticker': ticker, 'type': 'LIMIT', 'quantity': quantity,'action': 'SELL'}
resp = session.post('http://localhost:9999/v1/orders', params=mkt_sell_params)
if resp.ok:
mkt_order = resp.json()
id = mkt_order['order_id']
return 1
else:
#order not submitted
return 0

def lmt_buy(session, ticker, quantity):
mkt_buy_params = {'ticker': ticker, 'type': 'LIMIT', 'quantity': quantity, 'action': 'BUY'}
resp = session.post('http://localhost:9999/v1/orders', params=mkt_buy_params)
if resp.ok:
mkt_order = resp.json()
id = mkt_order['order_id']
return 1
else:
#order not submitted
return 0

'''