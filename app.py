from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index ():
    return render_template('chat.html')

@app.route('/process', methods=['POST'])
def process_data():
    data = request.get_json()
    input_text = data.get('input_text')
    selected_options = data.get('selected_options')

    print(input_text)
    # Do something with the received data
    # ...

    response = {'message': 'Data processed successfully'}
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)