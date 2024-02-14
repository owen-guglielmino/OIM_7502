import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick  # optional may be helpful for plotting percentage
import numpy as np
import pandas as pd
import seaborn as sb  # optional to set plot theme
import yfinance as yf

sb.set_theme()  # optional to set plot theme

DEFAULT_START = dt.date.isoformat(dt.date.today() - dt.timedelta(365))
DEFAULT_END = dt.date.isoformat(dt.date.today())


class Stock:
    def __init__(self, symbol, start=DEFAULT_START, end=DEFAULT_END):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.data = self.get_data(self.symbol, self.start, self.end)

    def get_data(self, symbol, start, end):
        """method that downloads data and stores in a DataFrame
           uncomment the code below wich should be the final two lines
           of your method"""
        if not start:
            start = DEFAULT_START
        if not end:
            end = DEFAULT_END

        data = yf.download(symbol, start=start, end=end)
        data.index = pd.to_datetime(data.index)
        self.data = data
        self.calc_returns(data)

        return data

    def calc_returns(self, data):
        """method that adds change and return columns to data"""
        # Change from day to day + 1
        data['change'] = data['Close'].diff()

        # Instantaneous return
        data['instant_return'] = np.log(data['Close'].shift(1).round(4))

    def plot_return_dist(self):
        """method that plots instantaneous returns as histogram"""
        sb.set(style='whitegrid')
        plt.figure(figsize=(10, 6))
        sb.histplot(self.data['instant_return'].dropna(), bins=25, kde=True, color='green')

    def plot_performance(self):
        """method that plots stock object performance as percent """
        self.data['percent_change'] = self.data['Close'].pct_change().cumsum() * 100

        plt.figure(figsize=(10, 6))
        plt.plot(self.data.index, self.data['percent_change'], label='Percent Change', color='green')
        plt.title(f'Stock Performance: {self.symbol}')
        plt.xlabel('Date')
        plt.ylabel('Percent Change')


def main():
    # uncomment (remove pass) code below to test
    test = Stock(symbol=['NVDA'])  # optionally test custom data range
    print(test.data)
    test.plot_performance()
    test.plot_return_dist()


if __name__ == '__main__':
    main()