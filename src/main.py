# import pygame
import random
from flask import Flask, render_template, request, session, jsonify
from board_module import Board
from entity_module import *

app = Flask(__name__)

board = Board(1, 1, 0)


@app.route('/board', methods=['POST'])
def new_board():
    global board

    try:
        n, m = 5, 5

        board = Board(n, m, 3)

        for i in range(3):
            board.board[random.randint(0, n - 1)][random.randint(0, m - 1)].append(
                GrassFeeding(random.randint(0, 20), str(i + 4)))
        for i in range(3):
            board.board[random.randint(0, n - 1)][random.randint(0, m - 1)].append(
                SmallPredator(random.randint(50, 200), str(i + 1)))
        for i in range(2):
            board.board[random.randint(0, n - 1)][random.randint(0, m - 1)].append(
                BigPredator(random.randint(200, 300), str(i + 7)))
        for i in range(5):
            board.board[random.randint(0, n - 1)][random.randint(0, m - 1)].append(Plant(random.randint(0, 40), 'kust'))
        board.board[random.randint(0, n - 1)][random.randint(0, m - 1)].append(Watcher('Man'))

        return 'OK.'
    except:
        return 'Error!'


@app.route('/board/', methods=['GET'])
def get_board_now():
    return jsonify(board.to_json_model())


if __name__ == '__main__':
    app.run(port=80, host='127.0.0.1')
