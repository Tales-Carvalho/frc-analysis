import analysis

ENGINE_PATH = '/usr/bin/stockfish'  # Stockfish 14.1 path
TIME_LIMIT = 1800                   # in seconds
MULTI_PV = 5                        # number of variants in analysis
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


if __name__ == '__main__':
  for key in fen_positions:
    analysis.analysis(fen_positions[key], key, TIME_LIMIT, MULTI_PV, ENGINE_PATH, THREADS)
