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
    return jsonify({'coin_id': 1337, 'coin_name': 'BTC',
                    'current_price': 1234.56, 'tomorrows_prediction': 2345.67})


####################################################################
####################           LAUNCH           ####################
####################################################################

if __name__ == '__main__':
    #app.run(host="0.0.0.0",port=PORT, debug=DEBUG)
    app.run(port=1337, debug=True)













########### EOF
