#you're gonna love my nuts
from scipy.stats import norm
import signal
import requests # step 1
from time import sleep
import numpy as np
import requests
from math import exp as Exp
from math import log as Log
from math import sqrt as Sqrt
Abs = abs
# This class definition allows us to print error messages and stop the program when needed
class ApiException(Exception):
    pass

# This helper method returns the current 'tick' of the running case
def get_tick(session):
    resp = session.get('http://localhost:9999/v1/case')
    if resp.ok:
        case = resp.json()
        return case['tick']
    raise ApiException('Authorization error. Please check API key.')
def signal_handler(signum, frame):
    global shutdown
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    shutdown = True
#CHECK PORT AND API KEY!!!
API_KEY = {'X-API-key':"apikey"} 
shutdown = False

def get_securities(session, ticker, key):
    payload = {'ticker': ticker}
    resp = session.get('http://localhost:9999/v1/securities', params=payload)
    if resp.ok:
        security = resp.json()
        return security[0][key]
    raise ApiException('Authorization error. Please check API key.')

def mkt_sell(session, ticker, quantity):
  mkt_buy_params = {'ticker': ticker, 'type': 'MARKET', 'quantity': quantity,'action': 'SELL'}
  resp = session.post('http://localhost:9999/v1/orders', params=mkt_buy_params)
  if resp.ok:
    print("SOLD 10K")
    mkt_order = resp.json()
    return mkt_order
#mkt_sell(s, 'RITC', 1000)

def mkt_buy(session, ticker, quantity):
  mkt_buy_params = {'ticker': ticker, 'type': 'MARKET', 'quantity': quantity,'action': 'BUY'}
  resp = session.post('http://localhost:9999/v1/orders', params=mkt_buy_params)
  if resp.ok:
    print("BOUGHT 10K")
    mkt_order = resp.json()
    return mkt_order
#mkt_buy(s, 'RITC', 1000)

def get_time_remaining(session):
    resp = session.get('http://localhost:9999/v1/case')
    if resp.ok:
        case = resp.json()
        return (case['ticks_per_period'] - case['tick'])
    raise ApiException('Authorization error. Please check API key.')

def ImpVol(Spot, Strike, Time, rate, test_price, IsCall):
    vol = 0.1
    Iteration = 0
    while 1:
        Price = BS_price(Spot, Strike, Time, rate, vol, IsCall)
        d_sigma = ( test_price - Price )  /  ( vega(Spot, Time, d_one(Spot / Strike, vol, Time)) + 0.0001 )
        if d_sigma > 0.1:
            d_sigma = 0.1
        elif d_sigma < - 0.1:
            d_sigma = - 0.1
        vol = vol + d_sigma
        if vol < 0.00001:
            vol = 0.00001
        Iteration = Iteration + 1
        if not (Abs(Price - test_price) > 0.000001 and Iteration < 25):
            break
    fn_return_value = vol
    return fn_return_value

def d_one(Moneyness, vol, Time):
    #Moneyness = Spot/Strike
    fn_return_value = ( Log(Moneyness, 10) + 0.5 * vol * vol * Time )  /  ( vol * Sqrt(Time) )
    return fn_return_value

def vega(Spot, Time, d1):
    fn_return_value = Spot * Sqrt(Time) / Sqrt(2 * math.pi) * Exp(- 0.5 * d1 * d1)
    return fn_return_value

def getCallTitles():
  callTitles = ["RTM2C45",
                  "RTM2C46",
                  "RTM2C47",
                  "RTM2C48",
                  "RTM2C49",
                  "RTM2C50",
                  "RTM2C51",
                  "RTM2C52",
                  "RTM2C53",
                  "RTM2C54"]
  return callTitles

def getPutTitles():
  putTitles = ["RTM2P45",
                "RTM2P46",
                "RTM2P47",
                "RTM2P48",
                "RTM2P49",
                "RTM2P50",
                "RTM2P51",
                "RTM2P52",
                "RTM2P53",
                "RTM2P54"]
  return putTitles

def getCallDiffs():
  callTitles = getCallTitles()
  calls = [calcINum(title) for title in callTitles]
  return calls

def getPutDs():
  putTitles = getPutTitles()
  Puts = [calcINum(title) for title in putTitles]
  return Puts

def getCallPositions(s):
  callTitles = getCallTitles()
  callPos = [get_securities(s, name, ‘position’) for name in callTitles]
  return callPos

def getPutPositions(s):
  putTitles = getPutTitles()
  putPos = [get_securities(s, name, ‘position’) for name in putTitles]
  return putPos

def Enter_the_gates_of_garbage(session):
    status = 0
    Sum = 0

    callPos = getCallPositions(session)
    putPos = getPutPositions(session)
    # SUMMING UP POSITIONS FOR CALLS
    Sum = sum(callPos) + sum(putPos)
    #for i in range(len(calls)):
    #Sum = Sum + calls[i] + Puts[i]

    if Sum > 800:
        if(getCalls()[-1] < getPuts()[0]):
          mkt_sell(s, "RTM2C54", 100)
          mkt_sell(s, "RTM2C54", 100)
        else:
          mkt_sell(s, "RTM2P45", 100)
          mkt_sell(s, "RTM2P45", 100)
        #if(wk.Cells(56, 4).Value2 < wk.Cells(58, 4).Value2, wk.Cells(56, 2).Value2, wk.Cells(58, 2).Value2):
        #status = API.AddOrder(IIf(wk.Cells(56, 4).Value2 < wk.Cells(58, 4).Value2, wk.Cells(56, 2).Value2, wk.Cells(58, 2).Value2), 100, 1, API.SELL, 0)
        #status = API.AddOrder(IIf(wk.Cells(56, 4).Value2 < wk.Cells(58, 4).Value2, wk.Cells(56, 2).Value2, wk.Cells(58, 2).Value2), 100, 1, API.SELL, 0)
    elif Sum < -800:
        if(getCalls()[-1] < getPuts()[0]):
          mkt_buy(s, "RTM2C54", 100)
          mkt_buy(s, "RTM2C54", 100)
        else:
          mkt_buy(s, "RTM2P45", 100)
          mkt_buy(s, "RTM2P45", 100)
        #status = API.AddOrder(IIf(wk.Cells(56, 4).Value2 > wk.Cells(58, 4).Value2, wk.Cells(56, 2).Value2, wk.Cells(58, 2).Value2), 100, 1, API.buy, 0)
        #status = API.AddOrder(IIf(wk.Cells(56, 4).Value2 > wk.Cells(58, 4).Value2, wk.Cells(56, 2).Value2, wk.Cells(58, 2).Value2), 100, 1, API.buy, 0)

def getDays(s):
  return get_time_remaining(s)//30.0 + 1

def getMaturityTime(s):
  return getDays(s)/240

def getStrikePrice(stockName):
  return int(stockName[-2:])

def getVolatility():
  ## TODO:
  #below it's done

def getD1(stockName, s):
    return (1/(getVolatility()*Sqrt(getMaturityTime())))*(LN(currentStockPrice(s)/getStrikePrice(stockName))+((getVolatility()**2)/2)*getMaturityTime())

def getD2(stockName, s):
    return getD1(stockName, s) - getVolatility()*Sqrt(getMaturityTime())

def currentStockPrice(s):
    return get_securities(s, "RTM", ‘last’)

def getDeltaSum(s):
  deltas = []
  #Does this work? 
  deltas.append(getStockPosition)
  gsum = 0
  for stockName in getCallTitles():
    gsum += ImpVol(s, currentStockPrice(s), getStrikePrice(stockName), getMaturityTime(), 0, calcFNum(stockName),1)
  for stockName in getPutTitles():
    gsum += ImpVol(s, currentStockPrice(s), getStrikePrice(stockName), getMaturityTime(), 0, calcFNum(stockName),0)
  allTitles = getCallTitles() + getPutTitles()
  for stockName in getCallTitles:
    interim = (1/(gsum*Sqrt(getMaturityTime())))*(Log(currentStockPrice(s)/getStrikePrice(stockName), math.e)+((gsum**2)/2)*getMaturityTime())
    newDel = get_securities(s, stockName, "position")*norm.cdf(interim)*100
    deltas.append(newDel)
  for stockName in getPutTitles:
    interim = (1/(gsum*Sqrt(getMaturityTime())))*(Log(currentStockPrice(s)/getStrikePrice(stockName), math.e)+((gsum**2)/2)*getMaturityTime())
    newDel = get_securities(s, stockName, "position")*(norm.cdf(interim) - 1) *100
    deltas.append(newDel)
  deltaSum = sum(deltas)
  return deltaSum

def calcENum(stockName):
  isCall = 1 if 'C' in stockName else 0 
  return BS_price(currentStockPrice(), getStrikePrice(stockName), getMaturityTime(), 0, getVolatility(), isCall)

def calcFNum(stockName, s):
    return get_securities(s, stockName, ‘last’)

def calcINum(stockName, s):
    return calcENum(stockName) - calcFNum(stockName, s)

def zeroOut(session)
    ticker_names = getCallTitles().extend(getPutTitles())
    name_pos = []
    for i in range(len(ticker_names)):
        name = ticker_names[i]
        position = get_securities(session, name, 'position')]
        name_pos.append((name,position))
        name_pos = sorted(name_pos.items(), key=lambda x: x[1])

    while(len(name_pos) != 0):
        first_name = name_pos[0][0]
        first_pos = name_pos[0][1]
        last_name = name_pos[len(name_pos) - 1][0]
        last_pos = name_pos[len(name_pos) - 1][1]

        if(first_pos < 0):
            if(abs(first_pos) >= 100)
                mkt_buy(s, first_name, 100)
                name_pos.pop(0)
                name_pos.insert(0, (first_name, (first_pos + 100))
            else:
                mkt_buy(s, first_name, (-1*first_pos))
                name_pos.pop(0)
        else:
            if(abs(first_pos) >= 100)
                mkt_sell(s, first_name, 100)
                name_pos.pop(0)
                name_pos.append((first_name, first_pos - 100))
            else:
                mkt_sell(s, first_name, first_pos)
                name_pos.pop(0)
        
        if(last_pos < 0):
            if(abs(last_pos) >= 100)
                mkt_buy(s, last_name, 100)
                name_pos.pop(len(name_pos)-1)
                name_pos.append((last_name, (last_pos + 100))
            else:
                mkt_buy(s, last_name, (-1*last_pos))
                name_pos.pop(len(name_pos)-1)
        else:
            if(abs(last_pos) >= 100)
                mkt_sell(s, last_name, 100)
                name_pos.pop(len(name_pos)-1)
                name_pos.append((last_name, last_pos - 100))
            else:
                mkt_sell(s, last_name, last_pos)
                name_pos.pop(len(name_pos)-1)

      name = "RTM"
      position = get_securities(s, name, 'position')
      if(position < 0)
        while(position < -100)
          position = position + 100
          mkt_buy(session, name, '100')
        mkt_buy(session, name, (position*-1))
      else:
        while(position > 100)
          position = position - 100
          mkt_sell(session, name, '100')
        mkt_sell(session, name, position)
def buyStraddle(s,callMis, putMis, callTitles, putTitles):
  temp = list(range(len(callMis)))
  z = list(zip(callMis,temp))
  bestIndex = max(z)[1]

  mkt_buy(s, callTitles[bestIndex], 100)
  mkt_buy(s, putTitles[bestIndex], 100)

def sellStraddle(s,callMis, putMis, callTitles, putTitles):
  temp = list(range(len(callMis)))
  z = list(zip(callMis,temp))
  bestIndex = min(z)[1]

  mkt_sell(s, callTitles[bestIndex], 100)
  mkt_sell(s, putTitles[bestIndex], 100)


def callSpread(s,callMis, callTitles):
  avg = np.average(callMis)
  diffs = callMis - avg
  absolute = np.absolute(diffs)

  temp = list(range(len(absolute)))
  z = list(zip(absolute,temp))
  bestIndex = max(z)[1]

  if(callMis[bestIndex] < avg):
    mkt_sell(s, callTitles[bestIndex], 100)
    mkt_sell(s, callTitles[bestIndex], 100)
    mkt_sell(s, callTitles[bestIndex], 100)
    mkt_sell(s, callTitles[bestIndex], 100)

    above = -1000
    below = -1000
    if((bestIndex - 1) >= 0):
      above = callMis[bestIndex - 1]
    if((bestIndex + 1) <= 9):
      below = callMis[bestIndex + 1]

    properIndex = max(above, below)
    mkt_buy(s, callTitles[properIndex], 100)
    mkt_buy(s, callTitles[properIndex], 100)
    mkt_buy(s, callTitles[properIndex], 100)
    mkt_buy(s, callTitles[properIndex], 100)
  else:
    mkt_buy(s, callTitles[bestIndex], 100)
    mkt_buy(s, callTitles[bestIndex], 100)
    mkt_buy(s, callTitles[bestIndex], 100)
    mkt_buy(s, callTitles[bestIndex], 100)

    above = 1000
    below = 1000
    if((bestIndex - 1) >= 0):
      above = callMis[bestIndex - 1]
    if((bestIndex + 1) <= 9):
      below = callMis[bestIndex + 1]

    properIndex = min(above, below)
    mkt_sell(s, callTitles[properIndex], 100)
    mkt_sell(s, callTitles[properIndex], 100)
    mkt_sell(s, callTitles[properIndex], 100)
    mkt_sell(s, callTitles[properIndex], 100)

def putSpread(s, putMis, putTitles):
  avg = np.average(putMis)
  diffs = putMis - avg
  absolute = np.absolute(diffs)

  temp = list(range(len(absolute)))
  z = list(zip(absolute,temp))
  bestIndex = max(z)[1]

  if(putMis[bestIndex] < avg):
    mkt_sell(s, putTitles[bestIndex], 100)
    mkt_sell(s, putTitles[bestIndex], 100)
    mkt_sell(s, putTitles[bestIndex], 100)
    mkt_sell(s, putTitles[bestIndex], 100)

    above = -1000
    below = -1000
    if((bestIndex - 1) >= 0):
      above = callMis[bestIndex - 1]
    if((bestIndex + 1) <= 9):
      below = callMis[bestIndex + 1]

    properIndex = max(above, below)
    mkt_buy(s, putTitles[properIndex], 100)
    mkt_buy(s, putTitles[properIndex], 100)
    mkt_buy(s, putTitles[properIndex], 100)
    mkt_buy(s, putTitles[properIndex], 100)
  else:
    mkt_buy(s, putTitles[bestIndex], 100)
    mkt_buy(s, putTitles[bestIndex], 100)
    mkt_buy(s, putTitles[bestIndex], 100)
    mkt_buy(s, putTitles[bestIndex], 100)

    above = 1000
    below = 1000
    if((bestIndex - 1) >= 0):
      above = callMis[bestIndex - 1]
    if((bestIndex + 1) <= 9):
      below = callMis[bestIndex + 1]

    properIndex = min(above, below)
    mkt_sell(s, putTitles[properIndex], 100)
    mkt_sell(s, putTitles[properIndex], 100)
    mkt_sell(s, putTitles[properIndex], 100)
    mkt_sell(s, putTitles[properIndex], 100)


def isStraddleCondition(callMis, putMis):
  if((np.var(callMis) > .0095) or (np.var(putMis) > .0095)):
    return False
  if(((np.average(callMis) >= .25) or (np.average(callMis) <= -.25))):
    return True
  elif(((np.average(putMis) >= .25) or (np.average(putMis) <= -.25))):
    return True
  else:
    return False

def isSpreadCondition(callMis, putMis):
  if((np.var(callMis) <= .0095) or (np.var(putMis) <= .0095)):
    return False
  else:
    return True

def getVelocity(veloTicks, tick, calls, puts, stockName = None):
    if tick not in veloTicks:
        if stockName: 
            if "C" in stockName:
                veloTicks[tick] = calls[getCallTitles.index(stockName)]
            else:
                veloTicks[tick] = puts[getPutTitles.index(stockName)] 
        else:
            dict[tick] = (sum(calls)/len(calls) + sum(puts)/len(puts))/2
        if (tick - 5) in veloTicks:
            return veloTicks[tick] - veloTicks[tick - 5] / 5
        else:
            return 1
    return 1

def get_volatility(session): 
    news_content = session.get('http://localhost:9999/v1/news')
    index = 0
    for char in str(news_content):
        if char == '%':
            percent_index = index
            break
        index += 1
        
    dash_index = 0
    if_one_number = False
    while True:
        index -= 1
        if news_content[index] == '-':
            dash_index = index
        if news_content[index] == ' ':
            if dash_index == 0:
                if_one_number = True
            space_index = index
            break
    if if_one_number:
        return(int(news_content[space_index+1:percent_index]) / 100)
    else:
        lower_bound = int(news_content[space_index+1:dash_index])
        upper_bound = int(news_content[dash_index+1:percent_index])
        return ((lower_bound + upper_bound) / 200)

def get_delta_limit(session):
    #news_content = session.get('http://localhost:9999/v1/news')
    news_content = "The delta limit for this sub-heat is 10,000"
    if "delta limit" in str(news_content):
        print(int(news_content[37:].replace(',', '')))

def hedge_delta(current_delta, delta_limit):
    if current_delta > delta_limit / 2:
        while current_delta > delta_limit / 2:  
            if current_delta < 10000:
                mkt_sell(s, 'RTM', current_delta)
            else:
                mkt_sell(s, 'RTM', 10000)
                current_delta -= 10000
    
    elif current_delta < -delta_limit / 2:
        while current_delta < -delta_limit / 2:  
            if -current_delta < 10000:
                mkt_buy(s, 'RTM', -current_delta)
            else:
                mkt_buy(s, 'RTM', 10000)
                current_delta += 10000
    else:
        pass

def main():
    with requests.Session() as s: 
            s.headers.update(API_KEY) 
            last_tick = get_tick(s) 
            ritc_max= 0
            delta = 0
            delta_limit = get_delta_limit(s)


            callTitles = getCallTitles()
            putTitles = getPutTitles()
            currentVol = .2
            
            veloTicks = dict()
            holding = False
            straddles = False

            while last_tick > 0 and last_tick < 600 and not shutdown:
                tick = get_tick(s)
                velo = 1
                callMis = getCallDiffs()
                putMis = getPutDiffs()
                callPosition = getCallPositions(s)
                putPosition = getPutPositions(s)

                delta = getDeltaSum(s)

                hedge_delta(delta, delta_limit)

                forecastVol = get_volatility(s)
                if(tick%75 == 1 and tick > 10):
                  currentVol = forecastVol

                straddleMarket = isStraddleCondition(callMis, putMis)
                spreadMarket = isSpreadMarket(callMis, putMis)
                if(straddleMarket):
                  velo = getVelocity(veloTicks, tick, calls, puts)
                elif(spreadMarket):

                  avg = np.average(callMis)
                  diffs = callMis - avg
                  absolute = np.absolute(diffs)
                  temp = list(range(len(absolute)))
                  z = list(zip(absolute,temp))
                  bestIndexCall = max(z)[1]
                  avg2 = np.average(putMis)
                  diffs2 = putMis - avg2
                  absolute2 = np.absolute(diffs2)
                  temp2 = list(range(len(absolute2)))
                  z2 = list(zip(absolute2,temp2))
                  bestIndexPut = max(z2)[1]

                  if(abs(callMis[bestIndexCall]) > abs(putMis[bestPutIndex])):
                    velo = getVelocity(veloTicks, tick, calls, puts, callTitles[bestIndexCall])
                  else:
                    velo = getVelocity(veloTicks, tick, calls, puts, putTitles[bestIndexPut])
                else:
                  velo = getVelocity(veloTicks, tick, calls, puts)
                  
                if(holding):
                  if(straddles):
                    if((not(straddleMarket) and velo <= .07) or ((np.average(callMis) < 0) and (np.sum(callPosition) + np.sum(putPosition) > 0) and velo <= .07) or ((np.average(callMis) > 0) and (np.sum(callPosition) + np.sum(putPosition) < 0) and velo <= .07)):
                      zeroOut(s)
                      holding = False
                  else:
                    if(not(spreadMarket) and velo < .1):
                      zeroOut(s)
                      holding = False
                else:
                  if(isStraddleMarket and velo <= .07):
                    if(np.average(callMis) > 0):
                      buyStraddle(s, callMis, putMis, callTitles, putTitles)
                      buyStraddle(s, callMis, putMis, callTitles, putTitles)
                      buyStraddle(s, callMis, putMis, callTitles, putTitles)
                      buyStraddle(s, callMis, putMis, callTitles, putTitles)
                      buyStraddle(s, callMis, putMis, callTitles, putTitles)
                      Enter_the_gates_of_garbage(s)
                      buyStraddle(s, callMis, putMis, callTitles, putTitles)
                      buyStraddle(s, callMis, putMis, callTitles, putTitles)
                      Enter_the_gates_of_garbage(s)
                      buyStraddle(s, callMis, putMis, callTitles, putTitles)
                      hedge_delta(delta, delta_limit)
                      straddles = True
                    else:
                      sellStraddle(s, callMis, putMis, callTitles, putTitles)
                      sellStraddle(s, callMis, putMis, callTitles, putTitles)
                      sellStraddle(s, callMis, putMis, callTitles, putTitles)
                      sellStraddle(s, callMis, putMis, callTitles, putTitles)
                      sellStraddle(s, callMis, putMis, callTitles, putTitles)
                      Enter_the_gates_of_garbage(s)
                      sellStraddle(s, callMis, putMis, callTitles, putTitles)
                      sellStraddle(s, callMis, putMis, callTitles, putTitles)
                      Enter_the_gates_of_garbage(s)
                      sellStraddle(s, callMis, putMis, callTitles, putTitles)
                      hedge_delta(delta, delta_limit)
                      straddles = True

                    holding = True
                  elif(isSpreadMarket and velo < .1):
                    avg = np.average(callMis)
                    diffs = callMis - avg
                    absolute = np.absolute(diffs)
                    temp = list(range(len(absolute)))
                    z = list(zip(absolute,temp))
                    bestIndexCall = max(z)[1]
                    avg2 = np.average(putMis)
                    diffs2 = putMis - avg2
                    absolute2 = np.absolute(diffs2)
                    temp2 = list(range(len(absolute2)))
                    z2 = list(zip(absolute2,temp2))
                    bestIndexPut = max(z2)[1]

                    if(abs(callMis[bestIndexCall]) > abs(putMis[bestPutIndex])):
                      callSpread(s,callMis, callTitles)
                    else:
                      putSpread(s, putMis, putTitles)
                    holding = True
                    hedge_delta(delta, delta_limit)
                    straddles = False

                if(tick > last_tick):
                    if(tick%75 == 73):
                      if((forecastVol >= currentVol + .02) and not(holding)):
                        buyStraddle(s, callMis, putMis, callTitles, putTitles)
                        buyStraddle(s, callMis, putMis, callTitles, putTitles)
                        buyStraddle(s, callMis, putMis, callTitles, putTitles)
                        buyStraddle(s, callMis, putMis, callTitles, putTitles)
                        buyStraddle(s, callMis, putMis, callTitles, putTitles)
                        Enter_the_gates_of_garbage(s)
                        buyStraddle(s, callMis, putMis, callTitles, putTitles)
                        buyStraddle(s, callMis, putMis, callTitles, putTitles)
                        Enter_the_gates_of_garbage(s)
                        buyStraddle(s, callMis, putMis, callTitles, putTitles)
                        hedge_delta(delta, delta_limit)
                        sleep(3)
                      elif((forecastVol <= currentVol - .02) and not(holding)):
                        sellStraddle(s, callMis, putMis, callTitles, putTitles)
                        sellStraddle(s, callMis, putMis, callTitles, putTitles)
                        sellStraddle(s, callMis, putMis, callTitles, putTitles)
                        sellStraddle(s, callMis, putMis, callTitles, putTitles)
                        sellStraddle(s, callMis, putMis, callTitles, putTitles)
                        Enter_the_gates_of_garbage(s)
                        sellStraddle(s, callMis, putMis, callTitles, putTitles)
                        sellStraddle(s, callMis, putMis, callTitles, putTitles)
                        Enter_the_gates_of_garbage(s)
                        sellStraddle(s, callMis, putMis, callTitles, putTitles)
                        hedge_delta(delta, delta_limit)
                        sleep(3)
                      elif((forecastVol >= currentVol + .05) and (np.sum(callPosition) + np.sum(putPosition) < 0)):
                        zeroOut(s)
                        buyStraddle(s, callMis, putMis, callTitles, putTitles)
                        buyStraddle(s, callMis, putMis, callTitles, putTitles)
                        buyStraddle(s, callMis, putMis, callTitles, putTitles)
                        buyStraddle(s, callMis, putMis, callTitles, putTitles)
                        buyStraddle(s, callMis, putMis, callTitles, putTitles)
                        Enter_the_gates_of_garbage(s)
                        buyStraddle(s, callMis, putMis, callTitles, putTitles)
                        buyStraddle(s, callMis, putMis, callTitles, putTitles)
                        Enter_the_gates_of_garbage(s)
                        buyStraddle(s, callMis, putMis, callTitles, putTitles)
                        hedge_delta(delta, delta_limit)
                        sleep(3)
                      elif((forecastVol <= currentVol - .05) and (np.sum(callPosition) + np.sum(putPosition) > 0)):
                        zeroOut(s)
                        sellStraddle(s, callMis, putMis, callTitles, putTitles)
                        sellStraddle(s, callMis, putMis, callTitles, putTitles)
                        sellStraddle(s, callMis, putMis, callTitles, putTitles)
                        sellStraddle(s, callMis, putMis, callTitles, putTitles)
                        sellStraddle(s, callMis, putMis, callTitles, putTitles)
                        Enter_the_gates_of_garbage(s)
                        sellStraddle(s, callMis, putMis, callTitles, putTitles)
                        sellStraddle(s, callMis, putMis, callTitles, putTitles)
                        Enter_the_gates_of_garbage(s)
                        sellStraddle(s, callMis, putMis, callTitles, putTitles)
                        hedge_delta(delta, delta_limit)
                        sleep(3)
                    last_tick = get_tick(s)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()