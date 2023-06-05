from flask import Flask, render_template, request, jsonify,redirect,url_for
from Algorithms.im import *
from Algorithms.EWitnesses import *

app = Flask(__name__)


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

@app.route('/createD', methods=['POST'])
def createDeductionWitness():
    data = request.get_json()
    wit = data.get('witness')
    name = data.get('name')
    witness_map[name] = Deduction_Theorem(witness_map[wit]).check

    res = "test"

    # Do something with the received data
    # ...

    response = {'message': res}
    print (witness_map)
    return jsonify(response)

@app.route('/createC1', methods=['POST'])
def createCut1Witness():
    data = request.get_json()
    wit1 = data.get('witness1')
    wit2 = data.get('witness2')
    f = data.get("languageSubset")
    name = data.get('name')

    witness_map[name] = Cut1(witness_map[wit1],witness_map[wit2],f).check

    res = "test"

    # Do something with the received data
    # ...

    response = {'message': res}
    return jsonify(response)

@app.route('/createC2', methods=['POST'])
def createCut2Witness():
    data = request.get_json()
    wit1 = data.get('witness1')
    wit2 = data.get('witness2')
    f = data.get("languageSubset")
    name = data.get('name')

    witness_map[name] = Cut2(witness_map[wit1],witness_map[wit2],f).check

    res = "test"

    # Do something with the received data
    # ...

    response = {'message': res}
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)