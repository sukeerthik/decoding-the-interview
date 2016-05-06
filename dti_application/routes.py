from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
	return 'Yo this hopefully works tho.'

if __name__ == '__main__':
	app.run()

