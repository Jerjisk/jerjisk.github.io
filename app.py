from flask import Flask, render_template, request, jsonify
import chess
import chess.pgn

app = Flask(__name__)

def is_valid_chess_moves(san_moves):
    board = chess.Board()
    pgn = chess.pgn.Game()

    for san_move in san_moves:
        move = chess.Move.from_uci(board.parse_san(san_move))
        if move in board.legal_moves:
            board.push(move)
            pgn.add_move(move)
        else:
            return False, None

    return True, pgn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_moves():
    san_moves = request.form['moves'].split()
    
    try:
        valid, game = is_valid_chess_moves(san_moves)

        if valid:
            return jsonify({'success': 'PGN file generated successfully!'})
        else:
            return jsonify({'error': 'Invalid chess moves.'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
