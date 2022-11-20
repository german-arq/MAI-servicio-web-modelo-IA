from flask import Flask, render_template

app = Flask(__name__)

messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]

@app.route('/')
def index():
    #return "Hello World"
    return render_template('input_form.html', messages=messages)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7200, debug=True)