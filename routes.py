from flask import Flask, render_template

app = Flask(__name__)

# Make login the default landing page
@app.route('/', methods=['GET', 'POST']) # GET for displaying login form, POST for handling user inputs.
def login():
    return render_template('login.html') 

# Defining route to registration page
@app.route('/register', methods=['GET', 'POST']) # GET for displaying registration form, POST for handling registration data.
def registration():
    return render_template('registration.html')

# Defining route to introduction page
@app.route('/intro')
def intro():
    return render_template('intro.html')

# Defining route to marketplace
@app.route('/marketplace')
def marketplace():
    return render_template('marketplace.html')

# Defining route to for users to play game
@app.route('/game')
def game():
    return render_template('game.html')

# Defining route for gameplay instructions
@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')

if __name__ == '__main__':
    app.run(debug=True)