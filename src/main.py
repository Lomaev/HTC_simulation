# import pygame
import random
from flask import Flask, render_template, request, session, jsonify
from board_module import Board
from entity_module import *
from log_module import print_to_log, get_log, clear_log

app = Flask(__name__, static_folder='data', static_url_path='/data')

board = Board(1, 1, 0)


@app.route('/board', methods=['POST'])
def new_board():
    global board

    try:
        # print(request.form.get(cols))
        m, n = int(request.form.get('cols')), int(request.form.get('rows'))
        animals = int(request.form.get('animals'))

        board = Board(m, n, 3)

        for i in range(animals):
            board.board[random.randint(0, n - 1)][random.randint(0, m - 1)].append(
                GrassFeeding(random.randint(0, 20), str(i + animals + 1)))
        for i in range(animals):
            board.board[random.randint(0, n - 1)][random.randint(0, m - 1)].append(
                SmallPredator(random.randint(50, 200), str(i + 1)))
        for i in range(animals//2+1):
            board.board[random.randint(0, n - 1)][random.randint(0, m - 1)].append(
                BigPredator(random.randint(200, 300), str(i + animals * 2 + 1)))
        for i in range(animals*2):
            board.board[random.randint(0, n - 1)][random.randint(0, m - 1)].append(Plant(random.randint(0, 40), 'kust'))
        board.board[random.randint(0, n - 1)][random.randint(0, m - 1)].append(Watcher('Man'))

        clear_log()

        print(board.to_json_model())
        print(jsonify(board.to_json_model()))
        return jsonify(board.to_json_model())
    except Exception as exep:
        print(exep)
        return 'Error!'


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/board/', methods=['GET'])
def get_board_now():
    return jsonify(board.to_json_model())


@app.route('/board/next', methods=['GET'])
def step():
    clear_log()
    board.move()
    board.interact()
    return jsonify(board.to_json_model())


@app.route('/board/logs', methods=['GET'])
def logs():
    return jsonify(get_log())


if __name__ == '__main__':
    app.run(port=80, host='127.0.0.1')
