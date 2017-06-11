from flask import Flask, render_template, redirect, request
import time

# global variables
global players
players = {}

# Home page
@app.route('/')
def main():
    return render_template('index.html',

# Join a game
@app.route('/join', methods=['POST'])
def join():
    name = request.form["username"]
    players[name] = None
    return redirect('/lobby/' + name)
