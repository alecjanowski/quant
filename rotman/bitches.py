from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import signal
import requests # step 1
from time import sleep
import numpy as np

def signal_handler(signum, frame):
    global shutdown
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    shutdown = True
#CHECK PORT AND API KEY!!!
API_KEY = {'X-API-key':"apikey"} 
shutdown = False


def StartBlink():
    ticktoupdate = Double()
    # VB2PY (UntranslatedCode) On Error GoTo ErrorhandSSler
    if Sheet2.Range('chart_reset') == Sheet2.Range('chart_check') and Sheet2.Range('Beginning_of_case') == 1:
        Sheet2.Range('chartdata').ClearContents()
    if IsError(Sheet2.Range('currenttick').Value) == True:
        pass
    else:
        ticktoupdate = Sheet2.Range('currenttick').Value
        if ticktoupdate == 0:
            pass
        elif ticktoupdate > 0:
            Sheet2.Cells[ticktoupdate + 1, 2].Value = Sheet1.Range('Portfolio_Delta')
    RunWhen = Now + TimeValue('00:00:01')
    Application.OnTime(RunWhen, 'StartBlink', VBGetMissingArgument(Application.OnTime, 2), True)
    return

def delete():
    Sheet2.Range('B2:B550').ClearContents()
    Call(StartBlink)

def StopBlink():
    RunWhen = Now + TimeValue('00:00:01')
    Application.OnTime(RunWhen, 'StartBlink', VBGetMissingArgument(Application.OnTime, 2), False)

def Enter_the_gates_of_garbage():
    Sum = Double()

    status = Variant()
    Sum = 0
    wk = ThisWorkbook.Sheets('Sheet1')
     
    calls = wk.Range(wk.Range('C47'), wk.Range('C56')).Value2
    Puts = wk.Range(wk.Range('C58'), wk.Range('C67')).Value2
    for i in vbForRange(1, UBound(calls)):
        Sum = Sum + calls(i, 1) + Puts(i, 1)
    if Sum > 800:
        status = API.AddOrder(IIf(wk.Cells(56, 4).Value2 < wk.Cells(58, 4).Value2, wk.Cells(56, 2).Value2, wk.Cells(58, 2).Value2), 100, 1, API.SELL, 0)
        status = API.AddOrder(IIf(wk.Cells(56, 4).Value2 < wk.Cells(58, 4).Value2, wk.Cells(56, 2).Value2, wk.Cells(58, 2).Value2), 100, 1, API.SELL, 0)
    elif Sum < - 800:
        status = API.AddOrder(IIf(wk.Cells(56, 4).Value2 > wk.Cells(58, 4).Value2, wk.Cells(56, 2).Value2, wk.Cells(58, 2).Value2), 100, 1, API.buy, 0)
        status = API.AddOrder(IIf(wk.Cells(56, 4).Value2 > wk.Cells(58, 4).Value2, wk.Cells(56, 2).Value2, wk.Cells(58, 2).Value2), 100, 1, API.buy, 0)

def buyStraddle():
    wk = Worksheet()

     

    status = Variant()

    mmx = Double()

    mxidx = Integer()

    mx = Double()
    wk = ThisWorkbook.Sheets('Sheet1')
     
    calls = wk.Range(wk.Range('D47'), wk.Range('D56')).Value2
    Puts = wk.Range(wk.Range('D58'), wk.Range('D67')).Value2
    Call(Enter_the_gates_of_garbage)
    mmx = 0
    mxidx = 0
    for i in vbForRange(1, UBound(calls)):
        if  ( calls(i, 1) + Puts(i, 1) )  > mmx:
            mmx = ( calls(i, 1) + Puts(i, 1) )
            mx = calls(i, 1) + Puts(i, 1)
            mxidx = i
    if mxidx <> 0:
        status = API.AddOrder(wk.Cells(mxidx + 46, 2).Value2, 100, 1, IIf(mx > 0, API.buy, API.SELL), 0)
        status = API.AddOrder(wk.Cells(mxidx + 57, 2).Value2, 100, 1, IIf(mx > 0, API.buy, API.SELL), 0)

def loopBuyStraddle():
    for i in vbForRange(1, 3):
        buyStraddle()

def dumpGarbage():
    wk = Worksheet()

     

    status = Variant()
    wk = ThisWorkbook.Sheets('Sheet1')
     
    if wk.Cells(56, 3).Value2 <> wk.Cells(67, 3).Value2:
        status = API.AddOrder(wk.Cells(56, 2).Value2, WorksheetFunction.Min(Abs(wk.Cells(67, 3).Value2 - wk.Cells(56, 3).Value2), 100), 1, IIf(wk.Cells(56, 3).Value2 < wk.Cells(67, 3).Value2, API.buy, API.SELL), 0)
        status = API.AddOrder(wk.Cells(56, 2).Value2, WorksheetFunction.Min(Abs(wk.Cells(67, 3).Value2 - wk.Cells(56, 3).Value2), 100), 1, IIf(wk.Cells(56, 3).Value2 < wk.Cells(67, 3).Value2, API.buy, API.SELL), 0)
    if wk.Cells(47, 3).Value2 <> wk.Cells(58, 3).Value2:
        status = API.AddOrder(wk.Cells(58, 2).Value2, WorksheetFunction.Min(Abs(wk.Cells(58, 3).Value2 - wk.Cells(47, 3).Value2), 100), 1, IIf(wk.Cells(58, 3).Value2 < wk.Cells(47, 3).Value2, API.buy, API.SELL), 0)
        status = API.AddOrder(wk.Cells(58, 2).Value2, WorksheetFunction.Min(Abs(wk.Cells(58, 3).Value2 - wk.Cells(47, 3).Value2), 100), 1, IIf(wk.Cells(58, 3).Value2 < wk.Cells(47, 3).Value2, API.buy, API.SELL), 0)

def loopDumpGarbage():
    for i in vbForRange(1, 2):
        dumpGarbage()

def SellStraddle():
    wk = Worksheet()

     

    status = Variant()

    mmx = Double()

    mxidx = Integer()

    mx = Double()
    wk = ThisWorkbook.Sheets('Sheet1')
     
    calls = wk.Range(wk.Range('D47'), wk.Range('D56')).Value2
    Puts = wk.Range(wk.Range('D58'), wk.Range('D67')).Value2
    Enter_the_gates_of_garbage()
    mmx = 0
    mxidx = 0
    for i in vbForRange(1, UBound(calls)):
        if  ( calls(i, 1) + Puts(i, 1) )  < mmx:
            mmx = ( calls(i, 1) + Puts(i, 1) )
            mx = calls(i, 1) + Puts(i, 1)
            mxidx = i
    if mxidx <> 0:
        status = API.AddOrder(wk.Cells(mxidx + 46, 2).Value2, 100, 1, IIf(mx > 0, API.buy, API.SELL), 0)
        status = API.AddOrder(wk.Cells(mxidx + 57, 2).Value2, 100, 1, IIf(mx > 0, API.buy, API.SELL), 0)

def loopSellStraddle():
    for i in vbForRange(1, 3):
        SellStraddle()

def unloadworstStraddle():
    wk = Worksheet()

     

    status = Variant()

    mmx = Double()

    mxidx = Integer()

    mx = Double()
    wk = ThisWorkbook.Sheets('Sheet1')
     
    calls = wk.Range(wk.Range('D47'), wk.Range('D56')).Value2
    Puts = wk.Range(wk.Range('D58'), wk.Range('D67')).Value2
    mmx = 10000
    mxidx = 0
    for i in vbForRange(1, UBound(calls)):
        if wk.Cells(i + 46, 3).Value2 <> 0 and wk.Cells(i + 57, 3).Value2 <> 0:
            if Abs(calls(i, 1) + Puts(i, 1)) < mmx:
                mmx = Abs(calls(i, 1) + Puts(i, 1))
                mx = calls(i, 1) + Puts(i, 1)
                mxidx = i
    if mxidx <> 0:
        status = API.AddOrder(wk.Cells(mxidx + 46, 2).Value2, 100, 1, IIf(wk.Cells(mxidx + 46, 3).Value2 < 0, API.buy, API.SELL), 0)
        status = API.AddOrder(wk.Cells(mxidx + 57, 2).Value2, 100, 1, IIf(wk.Cells(mxidx + 57, 3).Value2 < 0, API.buy, API.SELL), 0)

def buy_call():
    buycall = String()

    hedgeamount = Single()
    buycall = Worksheets('Sheet1').Cells(16, 'k').Text
    hedgeamount = Worksheets('Sheet1').Cells(16, 'l').Text
    for i in vbForRange(1, 6):
        Call(Spread_Trade(buycall, 100, 'RTM2C45', - 100 * hedgeamount))

def loopUnloadStraddle():
    for i in vbForRange(1, 3):
        unloadworstStraddle()

def unload_one(ticker, amount, loop_amt):
     

    status = Variant()
     
    for i in vbForRange(1, loop_amt):
        status = API.AddOrder(ticker, - amount, 1, API.buy, 0)

def unload_calls():
     

    status = Variant()

    rng = Range()

    cell = Range()
     
    rng = Worksheets('Sheet1').Range('B47:C56')
    API.ClearQueuedOrders()
    Range['Hedge_ONOFF'] = 'Off'
    for i in vbForRange(1, rng.Rows.Count):
        if rng.Cells(i, 2).Value >= 100:
            for l in vbForRange(1, Int(rng.Cells(i, 2).Value / 100)):
                status = API.AddOrder(rng.Cells(i, 1).Text, - 100, 1, API.buy, 0)
            status = API.AddOrder(rng.Cells(i, 1).Text, - ( rng.Cells(i, 2).Value % 100 ), 1, API.buy, 0)
        elif rng.Cells(i, 2).Value <= - 100:
            for l in vbForRange(1, Int(rng.Cells(i, 2).Value / - 100)):
                status = API.AddOrder(rng.Cells(i, 1).Text, 100, 1, API.buy, 0)
            status = API.AddOrder(rng.Cells(i, 1).Text, ( Abs(rng.Cells(i, 2).Value) % 100 ), 1, API.buy, 0)
        elif rng.Cells(i, 2).Value > 0 and rng.Cells(i, 2).Value < 100:
            status = API.AddOrder(rng.Cells(i, 1).Text, - rng.Cells(i, 2).Value, 1, API.buy, 0)
        elif rng.Cells(i, 2).Value < 0 and rng.Cells(i, 2).Value > - 100:
            status = API.AddOrder(rng.Cells(i, 1).Text, - rng.Cells(i, 2).Value, 1, API.buy, 0)

def unload_calls_small():
     

    status = Variant()

    rng = Range()

    cell = Range()
     
    rng = Worksheets('Sheet2').Range('A28:C37')
    API.ClearQueuedOrders()
    Range['Hedge_ONOFF'] = 'Off'
    for i in vbForRange(1, rng.Rows.Count):
        if rng.Cells(i, 3).Value >= 100:
            for l in vbForRange(1, Int(rng.Cells(i, 3).Value / 100)):
                status = API.AddOrder(rng.Cells(i, 1).Text, - 100, 1, API.buy, 0)
        elif rng.Cells(i, 3).Value <= - 100:
            for l in vbForRange(1, Int(rng.Cells(i, 3).Value / - 100)):
                status = API.AddOrder(rng.Cells(i, 1).Text, 100, 1, API.buy, 0)
        elif rng.Cells(i, 3).Value > 0 and rng.Cells(i, 3).Value < 100:
            status = API.AddOrder(rng.Cells(i, 1).Text, - rng.Cells(i, 3).Value, 1, API.buy, 0)
        elif rng.Cells(i, 3).Value < 0 and rng.Cells(i, 3).Value > - 100:
            status = API.AddOrder(rng.Cells(i, 1).Text, - rng.Cells(i, 3).Value, 1, API.buy, 0)

def buy_ATM_straddle():
    Coll = Collection()

    Put_ = Collection()

     
    Coll.Add('RTM2C45', '45')
    Coll.Add('RTM2C46', '46')
    Coll.Add('RTM2C47', '47')
    Coll.Add('RTM2C48', '48')
    Coll.Add('RTM2C49', '49')
    Coll.Add('RTM2C50', '50')
    Coll.Add('RTM2C51', '51')
    Coll.Add('RTM2C52', '52')
    Coll.Add('RTM2C53', '53')
    Coll.Add('RTM2C54', '54')
    Put_.Add('RTM2P45', '45')
    Put_.Add('RTM2P46', '46')
    Put_.Add('RTM2P47', '47')
    Put_.Add('RTM2P48', '48')
    Put_.Add('RTM2P49', '49')
    Put_.Add('RTM2P50', '50')
    Put_.Add('RTM2P51', '51')
    Put_.Add('RTM2P52', '52')
    Put_.Add('RTM2P53', '53')
    Put_.Add('RTM2P54', '54')
    Enter_the_gates_of_garbage()
     
    # VB2PY (UntranslatedCode) On Error GoTo errend
    status = API.AddOrder(Coll(CStr(ThisWorkbook.Sheets('Sheet1').Cells(10, 4).Value2)), 100, 1, API.buy, 0)
    status = API.AddOrder(Put_(CStr(ThisWorkbook.Sheets('Sheet1').Cells(10, 4).Value2)), 100, 1, API.buy, 0)

def sell_ATM_straddle():
    Coll = Collection()

    Put_ = Collection()

     
    Coll.Add('RTM2C45', '45')
    Coll.Add('RTM2C46', '46')
    Coll.Add('RTM2C47', '47')
    Coll.Add('RTM2C48', '48')
    Coll.Add('RTM2C49', '49')
    Coll.Add('RTM2C50', '50')
    Coll.Add('RTM2C51', '51')
    Coll.Add('RTM2C52', '52')
    Coll.Add('RTM2C53', '53')
    Coll.Add('RTM2C54', '54')
    Put_.Add('RTM2P45', '45')
    Put_.Add('RTM2P46', '46')
    Put_.Add('RTM2P47', '47')
    Put_.Add('RTM2P48', '48')
    Put_.Add('RTM2P49', '49')
    Put_.Add('RTM2P50', '50')
    Put_.Add('RTM2P51', '51')
    Put_.Add('RTM2P52', '52')
    Put_.Add('RTM2P53', '53')
    Put_.Add('RTM2P54', '54')
    Enter_the_gates_of_garbage()
     
    # VB2PY (UntranslatedCode) On Error GoTo errend
    status = API.AddOrder(Coll(CStr(ThisWorkbook.Sheets('Sheet1').Cells(10, 4).Value2)), 100, 1, API.SELL, 0)
    status = API.AddOrder(Put_(CStr(ThisWorkbook.Sheets('Sheet1').Cells(10, 4).Value2)), 100, 1, API.SELL, 0)

def unload_puts():
     

    status = Variant()

    rng = Range()

    cell = Range()
     
    rng = Worksheets('Sheet1').Range('B57:C67')
    API.ClearQueuedOrders()
    Range['Hedge_ONOFF'] = 'Off'
    for i in vbForRange(1, rng.Rows.Count):
        if rng.Cells(i, 2).Value >= 100:
            for l in vbForRange(1, Int(rng.Cells(i, 2).Value / 100)):
                status = API.AddOrder(rng.Cells(i, 1).Text, - 100, 1, API.buy, 0)
            status = API.AddOrder(rng.Cells(i, 1).Text, - ( rng.Cells(i, 2).Value % 100 ), 1, API.buy, 0)
        elif rng.Cells(i, 2).Value <= - 100:
            for l in vbForRange(1, Int(rng.Cells(i, 2).Value / - 100)):
                status = API.AddOrder(rng.Cells(i, 1).Text, 100, 1, API.buy, 0)
            status = API.AddOrder(rng.Cells(i, 1).Text, ( Abs(rng.Cells(i, 2).Value) % 100 ), 1, API.buy, 0)
        elif rng.Cells(i, 2).Value > 0 and rng.Cells(i, 2).Value < 100:
            status = API.AddOrder(rng.Cells(i, 1).Text, - rng.Cells(i, 2).Value, 1, API.buy, 0)
        elif rng.Cells(i, 2).Value < 0 and rng.Cells(i, 2).Value > - 100:
            status = API.AddOrder(rng.Cells(i, 1).Text, - rng.Cells(i, 2).Value, 1, API.buy, 0)

def unload_puts_small():
     

    status = Variant()

    rng = Range()

    cell = Range()
     
    rng = Worksheets('Sheet2').Range('A39:C48')
    API.ClearQueuedOrders()
    Range['Hedge_ONOFF'] = 'Off'
    for i in vbForRange(1, rng.Rows.Count):
        if rng.Cells(i, 3).Value >= 100:
            for l in vbForRange(1, Int(rng.Cells(i, 3).Value / 100)):
                status = API.AddOrder(rng.Cells(i, 1).Text, - 100, 1, API.buy, 0)
        elif rng.Cells(i, 3).Value <= - 100:
            for l in vbForRange(1, Int(rng.Cells(i, 3).Value / - 100)):
                status = API.AddOrder(rng.Cells(i, 1).Text, 100, 1, API.buy, 0)
        elif rng.Cells(i, 3).Value > 0 and rng.Cells(i, 3).Value < 100:
            status = API.AddOrder(rng.Cells(i, 1).Text, - rng.Cells(i, 3).Value, 1, API.buy, 0)
        elif rng.Cells(i, 3).Value < 0 and rng.Cells(i, 3).Value > - 100:
            status = API.AddOrder(rng.Cells(i, 1).Text, - rng.Cells(i, 3).Value, 1, API.buy, 0)

def clear():
     
     
    API.ClearQueuedOrders()

def CallSpread():
     

    status = Variant()

    offsetCallsRow = Double()

    offsetPutsRow = Double()

    mmx = Double()

    mxidx = Integer()

    mx = Double()

    spread_idx = Integer()

    spread_out = Double()
    wk = ThisWorkbook.Sheets('Sheet1')
     
    calls = wk.Range(wk.Range('D47'), wk.Range('D56')).Value2
    Puts = wk.Range(wk.Range('D58'), wk.Range('D67')).Value2
    offsetCallsRow = 46
    offsetPutsRow = 57
    mmx = 0
    mxidx = 0
    for i in vbForRange(1, UBound(calls)):
        if Abs(calls(i, 1)) > mmx:
            mmx = Abs(calls(i, 1))
            mx = calls(i, 1)
            mxidx = i
    status = API.AddOrder(wk.Cells(mxidx + offsetCallsRow, 2).Value2, 100, 1, IIf(mx > 0, API.buy, API.SELL), 0)
    if mx > 0:
        spread_out = - wk.Cells(40, 11).Value2
        for i in vbForRange(1, wk.Cells(39, 11).Value2):
            curr = mxidx - i
            if curr > 0 and curr < UBound(calls):
                if calls(curr, 1) < spread_out:
                    spread_out = calls(curr, 1)
                    spread_idx = curr
            curr = mxidx + i
            if curr > 0 and curr < UBound(calls):
                if calls(curr, 1) < spread_out:
                    spread_out = calls(curr, 1)
                    spread_idx = curr
        if spread_out < - wk.Cells(40, 11).Value2 and spread_idx > 0 and spread_idx < 11:
            status = API.AddOrder(wk.Cells(spread_idx + offsetCallsRow, 2).Value2, 100, 1, IIf(mx < 0, API.buy, API.SELL), 0)
        else:
            status = API.AddOrder(wk.Cells(offsetCallsRow + mxidx + IIf(mxidx < UBound(calls), 1, - 1), 2).Value2, 100, 1, IIf(mx < 0, API.buy, API.SELL), 0)
    else:
        spread_out = wk.Cells(40, 11).Value2
        for i in vbForRange(1, wk.Cells(39, 11).Value2):
            curr = mxidx - i
            if curr > 0 and curr < UBound(calls):
                if spread_out == 0:
                    spread_out = calls(curr, 1)
                    spread_idx = curr
                elif calls(curr, 1) > spread_out:
                    spread_out = calls(curr, 1)
                    spread_idx = curr
            curr = mxidx + i
            if curr > 0 and curr < UBound(calls):
                if spread_out == 0:
                    spread_out = calls(curr, 1)
                    spread_idx = curr
                elif calls(curr, 1) > spread_out:
                    spread_out = calls(curr, 1)
                    spread_idx = curr
        if spread_out > - wk.Cells(40, 11).Value2 and spread_idx > 0 and spread_idx < 11:
            status = API.AddOrder(wk.Cells(spread_idx + offsetCallsRow, 2).Value2, 100, 1, IIf(mx < 0, API.buy, API.SELL), 0)
        else:
            status = API.AddOrder(wk.Cells(offsetCallsRow + mxidx + IIf(mxidx < UBound(calls), 1, - 1), 2).Value2, 100, 1, IIf(mx < 0, API.buy, API.SELL), 0)
    #'status = API.AddOrder(wk.Cells(mxidx + 24, 2).Value2, 100, 1, IIf(mx > 0, API.buy, API.SELL), 0)
    #'''Call Enter_the_gates_of_garbage

def putspread():
     

    status = Variant()

    offsetCallsRow = Double()

    offsetPutsRow = Double()

    mmx = Double()

    mxidx = Integer()

    mx = Double()

    spread_idx = Integer()

    spread_out = Double()
    wk = ThisWorkbook.Sheets('Sheet1')
     
    calls = wk.Range(wk.Range('D47'), wk.Range('D56')).Value2
    Puts = wk.Range(wk.Range('D58'), wk.Range('D67')).Value2
    offsetCallsRow = 46
    offsetPutsRow = 57
    mmx = 0
    mxidx = 0
    for i in vbForRange(1, UBound(Puts)):
        if Abs(Puts(i, 1)) > mmx:
            mmx = Abs(Puts(i, 1))
            mx = Puts(i, 1)
            mxidx = i
    status = API.AddOrder(wk.Cells(mxidx + offsetPutsRow, 2).Value2, 100, 1, IIf(mx > 0, API.buy, API.SELL), 0)
    spread_out = 0
    if mx > 0:
        spread_out = - wk.Cells(40, 11).Value2
        for i in vbForRange(1, wk.Cells(39, 11).Value2):
            if i <> 0:
                curr = mxidx - i
                if curr > 0 and curr < UBound(Puts):
                    if Puts(curr, 1) < spread_out:
                        spread_out = Puts(curr, 1)
                        spread_idx = curr
                curr = mxidx + i
                if curr > 0 and curr < UBound(Puts):
                    if Puts(curr, 1) < spread_out:
                        spread_out = Puts(curr, 1)
                        spread_idx = curr
        if spread_out < - wk.Cells(40, 11).Value2 and spread_idx > 0 and spread_idx < 11:
            status = API.AddOrder(wk.Cells(spread_idx + offsetPutsRow, 2).Value2, 100, 1, IIf(mx < 0, API.buy, API.SELL), 0)
        else:
            status = API.AddOrder(wk.Cells(offsetPutsRow + mxidx + IIf(mxidx < UBound(Puts), 1, - 1), 2).Value2, 100, 1, IIf(mx < 0, API.buy, API.SELL), 0)
    else:
        spread_out = wk.Cells(40, 11).Value2
        for i in vbForRange(1, wk.Cells(39, 11).Value2):
            if i != 0:
                curr = mxidx - i
                if curr > 0 and curr < UBound(Puts):
                    if Puts(curr, 1) > spread_out:
                        spread_out = Puts(curr, 1)
                        spread_idx = curr
                curr = mxidx + i
                if curr > 0 and curr < UBound(Puts):
                    if Puts(curr, 1) > spread_out:
                        spread_out = Puts(curr, 1)
                        spread_idx = curr
        if spread_out > wk.Cells(40, 11).Value2 and spread_idx > 0 and spread_idx < 11:
            status = API.AddOrder(wk.Cells(spread_idx + offsetPutsRow, 2).Value2, 100, 1, IIf(mx < 0, API.buy, API.SELL), 0)
        else:
            status = API.AddOrder(wk.Cells(offsetPutsRow + mxidx + IIf(mxidx < UBound(Puts), 1, - 1), 2).Value2, 100, 1, IIf(mx < 0, API.buy, API.SELL), 0)
    #'status = API.AddOrder(wk.Cells(mxidx + 24, 2).Value2, 100, 1, IIf(mx > 0, API.buy, API.SELL), 0)
    #'''Call Enter_the_gates_of_garbage

def loopPutSpread():
    for i in vbForRange(1, 4):
        putspread()

def loopCallSpread():
    for i in vbForRange(1, 4):
        CallSpread()

def hedge_onclick():
     

    status = Variant()

    Delta = Double()
     
    Delta = ThisWorkbook.Sheets('Sheet1').Cells(45, 4).Value2
    if Delta > 0:
        status = API.AddOrder('RTM', Application.Min(Abs(Delta), 10000), 1, API.buy, 0)
    else:
        status = API.AddOrder('RTM', Application.Min(Abs(Delta), 10000), 1, API.SELL, 0)

def change_throttle():
    Application.RTD.ThrottleInterval = 500


def main():
    with requests.Session() as s: 
            s.headers.update(API_KEY) 
            last_tick = get_tick(s) 
            ritc_max= 0
            
            while last_tick > 0 and last_tick < 600 and not shutdown:
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
