from flask import Flask, render_template, request, jsonify,redirect,url_for
from Algorithms.im import *

app = Flask(__name__)

ohoy()
@app.route('/')
def index ():
    return render_template('chat.html')

@app.route('/process', methods=['POST'])
def process_data():
    data = request.get_json()
    kb = data.get('kb')
    measures = data.get('measures')
    witnesses = data.get('witnesses')
    res_depth = data.get('res_depth')
    

    print(data)
    print(measures)
    print(witnesses)
    res = run_measures(kb,measures,witnesses,res_depth)

    # Do something with the received data
    # ...

    response = {'message': res}
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)