import numpy as np
from flask import Flask, request, jsonify, render_template
from joblib import load
output = "Welcome"
app = Flask(__name__)
model = load('pipe.h5')


@app.route('/')
def home():
    return render_template('disease_index.html',prediction_text='{}'.format(output))


@app.route('/y_predict',methods=['POST'])
def y_predict():
        '''
        For rendering results on HTML GUI
        '''
        x_test = [[int(x) for x in request.form.values()]]
        arr = np.array(x_test[0])
        # print(len(arr))
        # print(np.count_nonzero(arr))
        print(x_test)
        none_zero = np.count_nonzero(arr)
        # print(zero_els,'hello')
        if none_zero< 5:
            output = 'You have selected insufficient symptoms, select atleast five symptoms'
        else:        
           if (x_test[0][0] == 0):
              x_test[0][0] = 0
              x_test[0].insert(1, 0)
           elif (x_test[0][0] == 1):
              x_test[0][0] = 1
              x_test[0].insert(1, 0)
           else:
              x_test[0][0] = 0
              x_test[0].insert(1, 1)
              print(x_test)
           prediction = model.predict(x_test)
           print(prediction)
           output = prediction[0]    
           output = "Disease Predicted: " + output
        return render_template('disease_index.html', prediction_text='{}'.format(output))


@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    prediction = model.y_predict([np.array(list(data.values()))])
    output = prediction[0]
    return jsonify(output)

@app.route('/reset')
def reset():
    output = "Welcome"
    return render_template('disease_index.html',prediction_text='{}'.format(output))


if __name__ == "__main__":
    app.run(debug=True)