from flask import Flask, request, jsonify
from flask_cors import CORS
from othello_ai import init_board, get_valid_moves, apply_move, ai_move

app = Flask(__name__)
CORS(app)  # CORSエラーを防ぐために有効化

@app.route("/init", methods=["GET"])
def init():
    board = init_board()
    return jsonify(board=board)

@app.route("/valid_moves", methods=["POST"])
def valid_moves():
    data = request.get_json()
    board = data["board"]
    player = data["player"]
    moves = get_valid_moves(board, player)
    return jsonify(valid_moves=moves)

@app.route("/apply_move", methods=["POST"])
def apply():
    data = request.get_json()
    board = data["board"]
    player = data["player"]
    move = data["move"]
    new_board = apply_move(board, move[0], move[1], player)
    return jsonify(board=new_board)

@app.route("/ai_move", methods=["POST"])
def ai():
    data = request.get_json()
    board = data["board"]
    player = data["player"]
    move = ai_move(board, player)
    return jsonify(move=move)

if __name__ == "__main__":
    app.run(debug=True)
