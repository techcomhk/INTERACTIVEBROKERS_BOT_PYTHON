import pandas as pd
from indicat import indicators
from handle_data import handler
import datetime as dt



class strategy:
    
    def __init__(self, plan):
        self.handle = handler()
        self.indicators = indicators()
        self.plan = plan



    def master(self, id, df, cond= 'and'):
        self.df = df
        result = []

        
        if cond == 'and':
            for i in self.plan[id]['strat'].keys():
                if i == 'strat1':
                    result.append(self.strategy1(id, 'strat1'))
                elif i == 'strat2':
                    result.append(self.strategy2(id, 'strat2'))


            res = [i[0] for i in result]
            strat = {i:ii for i, ii in enumerate(result)}


            if 'False' in res:
                return 'False', strat

            return 'True', strat


        elif cond == 'or':
            for i in self.plan[id]['strat'].keys():
                if i == 'strat1':
                    result.append(self.strategy1(id, 'strat1'))
                elif i == 'strat2':
                    result.append(self.strategy2(id, 'strat2'))


            res = [i[0] for i in result]
            strat = {i:ii for i, ii in enumerate(result)}


            if 'True' in res:
                return 'True', strat

            return 'False', strat



    def dataframe(self, id, strat, period=50):
    
        asset = self.plan[id]['asset']
        timeframe = self.plan[id]['strat'][strat]

        # try:
        df = self.df[(self.df.asset == asset) & (self.df.tf == timeframe)]
        # except:
        #     df = self.handle.candle_data(asset, timeframe, period+1)
        #     df = df.iloc[:-1]

        return df
    


    def strategy1(self, id, strat, df=pd.DataFrame(), period=5): 
        if len(df) == 0:
            df = self.dataframe(id, strat, period)

        strat = self.indicators.rsi(df, period)


        if strat[1] < 30 and strat[0] > strat[1] and self.plan[id]['direction'] == 'buy':
            return 'True', (strat, df)

        elif strat[1] > 70 and strat[0] < strat[1] and self.plan[id]['direction'] == 'sell':
            return 'True', (strat, df)

        return 'False', (strat, df)



    def strategy2(self, id, strat, df=pd.DataFrame(), period=20):
        if len(df) == 0:
            df = self.dataframe(id, strat, period)

        strat = self.indicators.MA(df, period)

        if df.iloc[-1].close > strat and self.plan[id]['direction'] == 'buy':
            return 'True', (strat, df)

        elif df.iloc[-1].close < strat and self.plan[id]['direction'] == 'sell':
            return 'True', (strat, df)

        return 'False', (strat, df)