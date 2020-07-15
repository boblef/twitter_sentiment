from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def hello():
    name = hello2()
    return render_template('index.html', name=name)


def hello2():
    return "Hello World"


if __name__ == "__main__":
    app.run(debug=True)
