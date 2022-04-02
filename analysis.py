import chess
import chess.engine
import os


def str_conversion(item: chess.engine.InfoDict) -> str:

  if isinstance(item, chess.engine.PovScore):
    return str(item.relative.score())
  elif isinstance(item, list):
    return item[0].uci()
  else:
    return str(item)


def analysis_move(
    fen_position: str, analysis_name: str, time_limit: int,
    engine_path: str, threads: int, move_list: list[str], starting_moves: list[str] = []
  ) -> None:

  engine = chess.engine.SimpleEngine.popen_uci(engine_path)

  engine.configure({'Threads': threads})

  analysis_str = '_'.join([analysis_name] + starting_moves)

  board = chess.Board(fen=fen_position, chess960=True)

  for move in starting_moves:
    board.push(chess.Move.from_uci(move))

  analysis_keys = ['multipv', 'pv', 'depth', 'time', 'score']
  
  print(f'Starting analysis for {analysis_str}. Time limit: {time_limit} seconds.')

  if not os.path.exists('logs_move'):
    os.mkdir('logs_move')

  for move in move_list:
    print(f'Analysing move {move}')

    analysis_list = []
    root_moves = [chess.Move.from_uci(move)]

    with open(os.path.join('logs_move', f'{analysis_str}_{move}.log'), 'w') as f:
      with engine.analysis(board, chess.engine.Limit(time=time_limit), root_moves=root_moves) as analysis:
        for info in analysis:
          f.write(str(info) + '\n')
          if info.get('pv'): # Checking if engine output is a PV line
            print(f' - Current depth: {info.get("depth")} (Time taken: {info.get("time")} s)', end='\r')
            analysis_list.append([info.get(k) for k in analysis_keys])
    print(f'\nAnalysis ended. Saving output to {analysis_str}_{move}_history.csv and {analysis_str}_{move}_final_evaluation.txt\n')

    if not os.path.exists('output_move'):
      os.mkdir('output_move')

    with open(os.path.join('output_move', f'{analysis_str}_{move}_history.csv'), 'w') as f:
      f.write(','.join(analysis_keys) + '\n')
      for line in analysis_list:
        f.write(','.join([str_conversion(i) for i in line]) + '\n')

    with open(os.path.join('output_move', f'{analysis_str}_{move}_final_evaluation.txt'), 'w') as f:
      f.write(str(analysis_list[-1]) + '\n')

  engine.quit()


def analysis(
    fen_position: str, analysis_name: str, depth_limit: int, multipv: int,
    engine_path: str, threads: int, starting_moves: list[str] = []
  ) -> list[str]:

  engine = chess.engine.SimpleEngine.popen_uci(engine_path)

  engine.configure({'Threads': threads})

  analysis_str = '_'.join([analysis_name] + starting_moves)

  board = chess.Board(fen=fen_position, chess960=True)

  for move in starting_moves:
    board.push(chess.Move.from_uci(move))

  analysis_keys = ['multipv', 'pv', 'depth', 'time', 'score']
  analysis_list = []

  print(f'Starting analysis for {analysis_str}. Depth limit: {depth_limit}.')

  if not os.path.exists('logs'):
    os.mkdir('logs')

  with open(os.path.join('logs', f'{analysis_str}.log'), 'w') as f:
    with engine.analysis(board, chess.engine.Limit(depth=depth_limit), multipv=multipv) as analysis:
      for info in analysis:
        f.write(str(info) + '\n')
        if info.get('pv'): # Checking if engine output is a PV line
          print(f' - Current depth: {info.get("depth")} (Time taken: {info.get("time")} s)', end='\r')
          analysis_list.append([info.get(k) for k in analysis_keys])

  print(f'\nAnalysis finished. Saving output to {analysis_str}_history.csv and {analysis_str}_final_evaluation.txt\n')

  if not os.path.exists('output'):
    os.mkdir('output')

  with open(os.path.join('output', f'{analysis_str}_history.csv'), 'w') as f:
    f.write(','.join(analysis_keys) + '\n')
    for line in analysis_list:
      f.write(','.join([str_conversion(i) for i in line]) + '\n')

  best_moves = []
  with open(os.path.join('output', f'{analysis_str}_final_evaluation.txt'), 'w') as f:
    for i in range(1, multipv + 1):
      best_moves.append(analysis_list[-i][1][0].uci())
      f.write(str(analysis_list[-i]) + '\n')

  engine.quit()

  return best_moves
