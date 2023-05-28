# -*- coding: utf-8 -*-
"""
Created on Sun May  7 12:38:34 2023

@author: YL
"""

from flask import Flask, flash, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
# for flash message
app.secret_key = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] ="postgresql://postgres:!QAZ2wsx#EDC4rfv@localhost/postgres"
db = SQLAlchemy(app)

class bg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique =True , nullable = False)
    min_player_count = db.Column(db.Integer, nullable=False)
    max_player_count = db.Column(db.Integer, nullable=False)
    cost=db.Column(db.Float, nullable=False)
    def __repr__(self):
        return (f"Name: {self.name}, Min: {self.min_player_count} Max: {self.max_player_count}, Cost: {self.cost}")


@app.route('/', methods=['GET','POST'])
def index():
    if request.method == "POST":
        game_name = request.form["game_name"]
        player_count = request.form["player_count"]
        if game_name:
            return redirect(url_for("game", game_name=game_name))
        else:
            # to render list of games that fits player count
            return f'<h> Nothing to see here yet</h>'

    else:
        return render_template('index.html')


@app.route('/new',methods=['GET','POST'])
def new():
    error= None
    if request.method == "POST":
        game_name=request.form["game_name"]
        min_player_count=request.form["min_player_count"]
        max_player_count = request.form["max_player_count"]
        cost = request.form["cost"]
        if min_player_count > max_player_count:
            error = "Player Counts are swapped"
            return render_template('new.html', error=error)
        else:
            #pass data to backend
            boardgame = bg(name=game_name,min_player_count=min_player_count,cost=cost)
            db.session.add(boardgame)
            db.session.commit()
            flash("Submission successful")
            return redirect(url_for('index'))
    else:
        return render_template('new.html')

@app.route('/<game_name>')
def game(game_name):
    boardgame=bg.query.filter_by(name=game_name).first()
    name=boardgame.name
    cost=boardgame.cost
# to design a proper template for each game later
    return render_template("game.html",name=name,cost=cost)

if __name__ == "__main__":
    app.run()