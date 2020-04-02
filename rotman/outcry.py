import signal
import requests # step 1
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style


#LAST YEAR GDP  #PROJECTED GDP #MANUFACTURED GOODS #SERVICES #RAW MATERIALS  #SUM OF LAST THREE  #MARGIN
#RIT VAL = sum of (projected - last year) + 1000


class ApiException(Exception):
    pass

def signal_handler(signum, frame):
    global shutdown
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    shutdown = True
#CHECK PORT AND API KEY!!!
API_KEY = {'X-API-key': 'NEZYSF2S'} 
shutdown = False

def news(session):
    resp = session.get('http://localhost:9999/v1/news')
    if resp.ok:
        news = resp.json()
        text = news[0]['body']
        
        print(text)
        print('\n\n__________NEWS___________')
        return 
def get_news_id(session):
    resp = session.get('http://localhost:9999/v1/news')
    if resp.ok:
        news = resp.json()
        return news[0]['news_id']
    raise ApiException('Authorization error. Please check API key.')

def get_tick(session):
    resp = session.get('http://localhost:9999/v1/case')
    if resp.ok:
        case = resp.json()
        return case['tick']
    raise ApiException('Authorization error. Please check API key.')

with requests.Session() as s: 
    s.headers.update(API_KEY) 
    last_tick = get_tick(s)
    news_id = 0

    while last_tick > 0 and last_tick < 1800 and not shutdown: 
        comp = get_news_id(s)

        if(comp > news_id):
            news(s)
            news_id = comp   

        last_tick = get_tick(s) 

            


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()