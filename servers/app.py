from flask import Flask
import jsonify


app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Crypto Trader's Dashboard!"
    #return render_template('index.html')

@app.route('/api/v1/predict/', methods=['POST'])
def predict():
    '''
        API takes a coin_id or coin_name and returns a prediction for the next day's price.
    '''
    return jsonify({'coin_id': 1, 'coin_name': 'BTC',
                    'current_price': 1234.56, 'tomorrows_prediction': 2345.67})


####################################################################
####################           LAUNCH           ####################
####################################################################





def main():
    app.run(port=1337, debug=True)



if __name__ == '__main__':
    main()













########### EOF
