from flask import Flask

#Create Flask Application
app = Flask (__name__)

#Define a route
@app.route('/')
def home ():
    return "Hello Flask is Working"

#Run The App
if __name__ == "__main__":
    app.run(debug=True)