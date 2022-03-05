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


def analysis(
    fen_position: str, analysis_name: str, time_limit: int, multipv: int,
    engine_path: str, threads: int
  ) -> None:

  engine = chess.engine.SimpleEngine.popen_uci(engine_path)

  engine.configure({'Threads': threads})

  board = chess.Board(fen=fen_position, chess960=True)

  analysis_keys = ['multipv', 'pv', 'depth', 'time', 'score']
  analysis_list = []

  print(f'Starting analysis for {analysis_name}. Time limit: {time_limit} seconds.')

  if not os.path.exists('logs'):
    os.mkdir('logs')

  with open(os.path.join('logs', f'{analysis_name}.log'), 'w') as f:
    with engine.analysis(board, chess.engine.Limit(time=time_limit), multipv=multipv) as analysis:
      for info in analysis:
        f.write(str(info) + '\n')
        if info.get('pv'): # Checking if engine output is a PV line
          print(f' - Current depth: {info.get("depth")} (Time taken: {info.get("time")})')
          analysis_list.append([info.get(k) for k in analysis_keys])

  print(f'Analysis ended. Saving output to {analysis_name}.csv')

  if not os.path.exists('output'):
    os.mkdir('output')

  with open(os.path.join('output', f'{analysis_name}_history.csv'), 'w') as f:
    f.write(','.join(analysis_keys) + '\n')
    for line in analysis_list:
      f.write(','.join([str_conversion(i) for i in line]) + '\n')

  with open(os.path.join('output', f'{analysis_name}_final_evaluation.txt'), 'w') as f:
    for i in range(1, multipv + 1):
      f.write(str(analysis_list[-i]) + '\n')

  engine.quit()
