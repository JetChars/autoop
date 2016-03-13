''' module docstring
'''
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    '''this is a test
    '''
    return file("template/starter-template.html").read()

@app.route('/usr/<uname>')
def usr():
    '''this is a test
    '''
    return "hello %s" % uname

@app.route('/test')
def test():
    '''this is a test
    '''
    return render_template("starter-template.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0')
