import os, json
import analysis

ENGINE_PATH = '/usr/bin/stockfish'  # Stockfish 14.1 path
TIME_LIMIT = 300                    # in seconds
DEPTH_LIMIT = 35                    # for finding best moves
MULTI_PV = 4                        # number of variants in analysis
THREADS = 4                         # number of threads for Stockfish

fen_positions = {
  'standard':   'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', # Standard Chess
  # 'chesscom':   'bbnnrkrq/pppppppp/8/8/8/8/PPPPPPPP/BBNNRKRQ w KQkq - 0 1', # Chesscom forums: https://www.chess.com/clubs/forum/view/960-balance-analysis-the-search-for-really-unfair-positions
  # 'chessbase1': 'rnbknbqr/pppppppp/8/8/8/8/PPPPPPPP/RNBKNBQR w KQkq - 0 1', # Chessbase post: https://en.chessbase.com/post/the-problem-with-chess960
  # 'chessbase2': 'nbqnbrkr/pppppppp/8/8/8/8/PPPPPPPP/NBQNBRKR w KQkq - 0 1',
  # 'chessbase3': 'rbqkbrnn/pppppppp/8/8/8/8/PPPPPPPP/RBQKBRNN w KQkq - 0 1',
  # 'chessbase4': 'rnkbbrnq/pppppppp/8/8/8/8/PPPPPPPP/RNKBBRNQ w KQkq - 0 1',
  'ccrl1':      'qbbrkrnn/pppppppp/8/8/8/8/PPPPPPPP/QBBRKRNN w KQkq - 0 1', # CCRL FRC results: http://computerchess.org.uk/ccrl/404FRC/opening_report_by_white_score.html#table_start
  'ccrl2':      'nbrkbqnr/pppppppp/8/8/8/8/PPPPPPPP/NBRKBQNR w KQkq - 0 1',
  'ccrl3':      'rbqnkrbn/pppppppp/8/8/8/8/PPPPPPPP/RBQNKRBN w KQkq - 0 1'
}

def find_white_moves():
  # Find best moves for white
  best_white_moves = dict()
  for key in fen_positions:
    best_white_moves[key] = analysis.analysis(
      fen_positions[key], key, DEPTH_LIMIT,
      MULTI_PV, ENGINE_PATH, THREADS
    )
  
  with open(os.path.join('data', 'best_white_moves.json'), 'w') as f:
    json.dump(best_white_moves, f)


def find_black_moves():
  # Find best moves for black, given white move
  f = open(os.path.join('data', 'best_white_moves.json'), 'r')
  best_white_moves = json.load(f)
  f.close()

  best_black_moves = dict()
  for key in fen_positions:
    best_black_moves[key] = dict()
    for move in best_white_moves[key]:
      best_black_moves[key][move] = analysis.analysis(
        fen_positions[key], key, DEPTH_LIMIT,
        MULTI_PV, ENGINE_PATH, THREADS, [move]
      )
  
  with open(os.path.join('data', 'best_black_moves.json'), 'w') as f:
    json.dump(best_black_moves, f)


def analyze_white_moves():
  # Analysis of white moves
  f = open(os.path.join('data', 'best_white_moves.json'), 'r')
  best_white_moves = json.load(f)
  f.close()

  for key in fen_positions:
    analysis.analysis_move(fen_positions[key], key, TIME_LIMIT, ENGINE_PATH, THREADS, best_white_moves[key])


def analyze_black_moves():
  # Analysis of black moves
  f = open(os.path.join('data', 'best_black_moves.json'), 'r')
  best_black_moves = json.load(f)
  f.close()

  for key in fen_positions:
    for move in best_black_moves[key]:
      analysis.analysis_move(fen_positions[key], key, TIME_LIMIT, ENGINE_PATH, THREADS, best_black_moves[key][move], [move])

if __name__ == '__main__':
  find_white_moves()
  find_black_moves()
  analyze_white_moves()
  analyze_black_moves()
