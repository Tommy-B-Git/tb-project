from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
  return render_template("base.html")

@app.route("/basic")
def basic():
  return "This will be the basic signup page"

@app.route("/premium")
def premium():
  return "This will be the Premium signup page"

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)


