from flask import Flask 
from flask import render_template
from flask import redirect
from flask import request
from flask_pymongo import PyMongo
import scrape_mars
from pymongo import MongoClient
import pymongo

# Create an instance of Flask

# app = Flask(__name__, template_folder='../templates')
app = Flask(__name__)


# Use PyMongo to establish Mongo Connection
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")

# Elie said to try using this, might solve "jinja error" 
# app.config["MONGO_URI"] = "mongodb://localhost:27017/mission_to_mars"
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)

# conn = "mongodb://localhost:27017/mission_to_mars"

# client = pymongo.MongoClient(conn)

# Route to render index.html template using data from Mongo
@app.route("/")
def index():
    # FLASK TEST, CHECKING FOR CONNECTION 
    # return "<h1>Mission To Mars - THE APP IS RUNNING!</h>"

    # Find one record  of data from the Mongo Database
    # mars = mongo.db.collections.find_one()
    
    # mars = client.db.mars.find_one()
    mars = mongo.db.mars.find_one()
    
    # Return template and data
    return render_template("index.html", mars = mars)

# Route that will trigger the scrape function    
@app.route("/scrape")
def scrape():

    # Run the scrape function
    # mars = client.db.mars
    mars = mongo.db.mars
    mars_web = scrape_mars.scrape_news()
    mars_web = scrape_mars.scrape_marsImage()
    mars_web = scrape_mars.scrape_marsTwitter()
    mars_web = scrape_mars.scrape_marsFacts()
    mars_web = scrape_mars.scrape_marsH1Cerberus()
    mars_web = scrape_mars.scrape_marsH2Schiaparelli()
    mars_web = scrape_mars.scrape_marsH3SyrtisMajor()
    mars_web = scrape_mars.scrape_marsH4VallesMarineris()
    
    # Update the Mongo Database using update and upsert=True
    mars.update({}, mars_web, upsert=True)
    
    # Redirect back to home page
    return redirect("/", code=302)

# # Given Already
if __name__ == "__main__":
    app.run(debug=True)