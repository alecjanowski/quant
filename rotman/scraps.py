def zeroOut()
    ticker_names = getCalls().extend(getPuts)
    name_pos = []
    for i in range(len(ticker_names)):
        name = ticker_names[i]
        position = get_securities(s, name, 'position')]
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
        

        
    #zero out rtm
    
    while(len(positions) != 0):

        if(position)
    
    while(len(dict) != 0):
        dict[0]
    for i in range(len(ticker_names)):
      name = "RTM"
      position = get_securities(s, name, 'position')
      if(position < 0)
        while(position < -100)
          position = position + 100
          mkt_buy(s, name, '100')
        mkt_buy(s, name, (position*-1))
      else:
        while(position > 100)
          position = position - 100
          mkt_sell(s, name, '100')
        mkt_sell(s, name, position)





        
def zeroOut()
    ticker_names = getCalls().extend(getPuts).append("RTM")
    for i in range(len(ticker_names)):
      name = ticker_names[i]
      position = get_securities(s, name, 'position')
      if(position < 0)
        while(position < -100)
          position = position + 100
          mkt_buy(s, name, '100')
        mkt_buy(s, name, (position*-1))
      else:
        while(position > 100)
          position = position - 100
          mkt_sell(s, name, '100')
        mkt_sell(s, name, position)