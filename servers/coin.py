'''
    coin.py
        This module retrieves, cleans, and normalizes cryptocurrency data from the coinranking API.
        The API can be found at https://api.coinranking.com/
'''
import pandas as pd
import numpy as np
import requests
import json
import sys

class Coin():
    valid_timeframes = ['24h', '7d', '30d', '1y', '5y']
    coin_id = { 'BTC': 1 }

    def __init__(self, coin_name='BTC', timeframe='30d', base='USD'):
        '''
            Constructor. sets the URL, Name, data, price matrix, and normalized prices
            of the given coin on creation
        '''
        self.update_coin_ids()
        if self.is_valid_coin(coin_name) and self.is_valid_timeframe(timeframe):
            try:
                self.timeframe = timeframe
                self.base = base
                self.coin_name = coin_name
                self.coin_url = self.generate_coin_url()
                self.data = self.get_historic_prices()
                self.price_matrix = self.get_price_matrix(30)
                self.normalized_prices = self.normalize_prices(self.price_matrix)
            except Exception as e:
                print("Exception Initializing Coin:: " + str(e))
        else:
            print('Invalid Argument(s) Detected.')

    def generate_coin_url(self):
        '''
            Generates a URL for retrieving historical coin data
        '''
        c_url = f'''https://api.coinranking.com/v1/public/coin/{self.coin_id[self.coin_name]}/history/{self.timeframe}?base={self.base}'''
        return c_url

    def get_stats(self):
        '''
            Returns an object with all active information on the coin object.
        '''
        statz = {'coin_name': self.coin_name, 'coin_id': self.coin_id[str(self.coin_name)],
                    'history_timeframe': self.timeframe,
                    'price_matrix': self.get_price_matrix, 'normalized_prices': self.normalized_prices}
        return statz

    def get_dataframe(self):
        '''
            Returns a pandas dataframe with available historical data and any requested indicators
        '''
        # TODO: add indicators as columns to dataframe
        return self.data

    def get_historic_prices(self):
        '''
            GETs historic price data for the given coin from the CoinRanking.com API
        '''
        try:
            r = requests.get(self.coin_url)
            coin = json.loads(r.text)['data']['history']
            df = pd.DataFrame(coin)
            df['price'] = pd.to_numeric(df['price'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms').dt.date
        except Exception as e:
            print("Exception Getting Historic Prices:: "+str(e))
            return -1
        return df.groupby('timestamp').mean()

    def get_price_matrix(self, seq_len):
        '''
            Converts the price series into a nested list where every item of the list contains
            the historic prices of seq_len number of days
            Function borrowed from: https://gist.github.com/ogyalcin/d893ddb1d49d389ffcfa94cb47e6f5bc#file-rnn_2-py
        '''
        try:
            price_matrix = []
            price_data = self.data['price']
            #print(str(range(len(price_data)-seq_len+1)))
            for index in range(len(price_data)-seq_len+1):
                print(f'adding {self.data[index:index+seq_len]}')
                price_matrix.append(price_data[index:index+seq_len])
            return price_matrix
        except Exception as e:
            print("Exception Getting Price Matrix:: " + str(e))

    def update_coin_ids(self):
        '''
            Function which updates the key/value pairs in self.coin_id to the latest
            information available from the Coinranking.com API
        '''
        c_url = 'https://api.coinranking.com/v1/public/coins'
        try:
            r = requests.get(c_url)
            coinz = json.loads(r.text)['data']['coins']
            for ele in coinz:
                self.coin_id[str(ele['symbol'])] = ele['id']
            return 0
        except Exception as e:
            print("Exception Updating Coin IDs: " + str(e))
            return -1

    def set_timeframe(self, new_tf):
        '''
            Modifies the timeframe parameter of the coin history
        '''
        self.timeframe = new_tf
        reload_data()
        return 0

    def set_base(self, new_base):
        '''
            Modifies the base currency parameter of the coin history
        '''
        self.base = new_base
        reload_data()
        return 0

    def reload_data(self):
        '''
            Updates coin information after parameter changes have been made
        '''
        try:
            self.coin_url = generate_coin_url()
            self.data = self.get_historic_prices()
            self.price_matrix = self.get_price_matrix(30)
            self.normalized_prices = self.normalize_prices(self.price_matrix)
        except Exception as e:
            print("Exception Reloading Data:: "+str(e))
            return -1
        return 0

    def normalize_prices(self, price_data):
        '''
            Normalizes each value to reflect the percentage changes from starting point
            Function borrowed from: https://gist.github.com/ogyalcin/d893ddb1d49d389ffcfa94cb47e6f5bc#file-rnn_2-py
        '''
        normalized_data = []
        try:
            for window in price_data:
                # TODO: check what's actually coming into window[0]
                print(float(window[0]))
                fw0_var = float(window[0]) if float(window[0]) != 0.0 else 1.0
                normalized_window = [((float(p) / fw0_var) - 1) for p in window]
                normalized_data.append(normalized_window)
            return normalized_data
        except Exception as e:
            print("Exception Normalizing Prices:: " +str(e))
            return -1


    # should I move this train_test_split elsewhere in the code?
    ## Options Include: app.py, coin.py, net.py
    def train_test_split_(self, train_size=0.9, shuffle=False, return_row=True):
        '''
            Makes a custom train test split where the last part is kept as the training set.
            Function borrowed from: https://gist.github.com/ogyalcin/d893ddb1d49d389ffcfa94cb47e6f5bc#file-rnn_2-py
        '''
        try:
            self.price_matrix = np.array(self.price_matrix)
            row = int(round(train_size * len(self.price_matrix)))
            train = self.price_matrix[:row, :]
            if shuffle==True:
                np.random.shuffle(train)
            X_train, y_train = train[:row,:-1], train[:row,-1]
            X_test, y_test = self.price_matrix[row:,:-1], self.price_matrix[row:,-1]
            X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
            X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
            if return_row:
                return row, X_train, y_train, X_test, y_test
            else:
                return X_train, y_train, X_test, y_test
        except Exception as e:
            print("Exception Splitting Train and Test Data: " + str(e))
            return -1

    def is_valid_coin(self, coin):
        '''
            Returns True if the provided string is one of the keys in self.coin_id
        '''
        # judging by coinranking's coin list, coins can be 2-5 characters in length
        # all upper-case, Alphabetical. Some coins include an asterisk (*)
        # TODO: regex that checks that input matches the above description
        return True if coin in self.coin_id.keys() else False

    def is_valid_timeframe(self, tf):
        '''
            Returns True if the provided string is present in the list self.valid_timeframes
        '''
        return True if tf in self.valid_timeframes else False





def main():
    if len(sys.argv) != 4:
        print('Incorrect arguments provided.')
        print('Format is:: python <script_name.py> <coin_abbrv> <timeframe> <base_currency>')
        print('  Example:: python coin.py BTC 30d USD')
        return -1
    else:
        new_coin = Coin(sys.argv[1], sys.argv[2], sys.argv[3])
        print(str(new_coin.get_stats()))
    return 0





if __name__ == '__main__':
    main()

















    #### EOF
