from flask import Flask, render_template, url_for, request

app = Flask(__name__)

storage= ['chocolate','strawberry','melon']
basket={}
for items in storage:
	basket[items]=0

@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html', title="Home",basket=basket)

@app.route('/items', methods=["GET","POST"])
def items():
	form = str(request.form).split("'")[1]
	if form in(basket):
		basket[form]+=1
		form = None
	return render_template('items.html', title="Items", storage=storage, basket=basket)

if __name__ == '__main__':
	app.run(debug=True)