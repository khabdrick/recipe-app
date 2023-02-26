from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint #u8sed to make sure user_id and article_id is unique
from dataclasses import dataclass # used to define a clas that encapsulate data
import requests
from producer import publish

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://khabdrick1:secure-password@flask_db/comments'

db = SQLAlchemy(app)

@dataclass
class Recipe(db.Model):
    id: int
    title: str
    time_minutes: int
    price: int
    description: str
    ingredients: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    time_minutes = db.Column(db.Integer)
    price = db.Column(db.String)
    description = db.Column(db.String(1000))
    ingredients = db.Column(db.String(500))


@app.route('/api/recipe')
def index():
    return jsonify(Recipe.query.all())


@app.route('/api/comment', methods=['POST'])
def comment():
    
    data = request.get_json()
    print(data['recipe_id'])
    recipe_id = data['recipe_id']
    comment_text = data['comment_text']
    messages = [recipe_id, comment_text]

    # publish messages
    
    publish('commented', messages)    

    return jsonify({
        'message': 'success'
    })



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5005')
