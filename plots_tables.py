import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
import os, json

matplotlib.use('pgf')
matplotlib.rcParams.update({
  'pgf.texsystem': 'pdflatex',
  'font.family': 'serif',
  'text.usetex': True,
  'pgf.rcfonts': False,
})


def mean_stability_plot(moves, legend_names):

  moves_white = {}
  for name in moves:
    arr = []
    for white in moves[name]:
      arr.append(f'{name}_{white}')
    moves_white[name] = arr.copy()
  
  moves_black = {}
  for name in moves:
    arr = []
    for white in moves[name]:
      for black in moves[name][white]:
        arr.append(f'{name}_{white}_{black}')
    moves_black[name] = arr.copy()

  # White mean stabilibty
  white_mean_stabilities = []

  for name in moves:
    stabilities = []
    for move in moves_white[name]:
      csv_file = pd.read_csv(os.path.join('output_move', f'{move}_history.csv'))
      group_by_depth = csv_file.groupby(['depth'])
      stability = group_by_depth['score'].max().diff().abs()
      stabilities.append(stability)
    white_mean_stabilities.append(pd.concat(stabilities, axis=1).mean(axis=1).rename(name))

  plt.figure(figsize=(4,3))
  for s in white_mean_stabilities:
    plt.plot(s)
  plt.xlabel('Depth')
  plt.ylabel('Average Absolute Stability')
  plt.legend(legend_names)
  plt.tight_layout()
  plt.grid()
  plt.savefig(os.path.join('plots', f'mean_stability_white.pgf'))
  plt.savefig(os.path.join('plots', f'mean_stability_white.png'))

  # Black mean stabilibty
  black_mean_stabilities = []

  for name in moves:
    stabilities = []
    for move in moves_black[name]:
      csv_file = pd.read_csv(os.path.join('output_move', f'{move}_history.csv'))
      group_by_depth = csv_file.groupby(['depth'])
      stability = group_by_depth['score'].max().diff().abs()
      stabilities.append(stability)
    black_mean_stabilities.append(pd.concat(stabilities, axis=1).mean(axis=1).rename(name))

  plt.figure(figsize=(4,3))
  for s in black_mean_stabilities:
    plt.plot(s)
  plt.xlabel('Depth')
  plt.ylabel('Average Absolute Stability')
  plt.legend(legend_names)
  plt.tight_layout()
  plt.grid()
  plt.savefig(os.path.join('plots', f'mean_stability_black.pgf'))
  plt.savefig(os.path.join('plots', f'mean_stability_black.png'))


def scores_depths_plot(folder, player, moves, legend_names: list[str]) -> None:

  scores = []
  depths = []

  for move in moves:

    csv_file = pd.read_csv(os.path.join(folder, f'{move}_history.csv'))

    group_by_depth = csv_file.groupby(['depth'])
    
    if not os.path.exists('plots'):
      os.mkdir('plots')
    
    # Score by depth
    score = group_by_depth['score'].max()
    scores.append(score.rename(move))

    # plt.figure(figsize=(4,3))
    # plt.plot(score)
    # plt.xlabel('Depth')
    # plt.ylabel('Evaluation Score')
    # plt.tight_layout()
    # plt.grid()
    # plt.savefig(os.path.join('plots', f'{name}_score.pgf'))

    # Depth by time
    time = group_by_depth['time'].min()
    depth = pd.Series(time.index.values, index=time)
    depths.append(depth.rename(move))

    # plt.figure(figsize=(4,3))
    # plt.plot(depth)
    # plt.xlabel('Time')
    # plt.ylabel('Reached Depth')
    # plt.tight_layout()
    # plt.grid()
    # plt.savefig(os.path.join('plots', f'{name}_depth.pgf'))

  plt.figure(figsize=(4,3))
  for s in scores:
    plt.plot(s)
  plt.xlabel('Depth')
  plt.ylabel('Evaluation Score [centipawns]')
  plt.title(f'First {player} move evaluation')
  plt.legend(legend_names)
  plt.tight_layout()
  plt.grid()
  plt.savefig(os.path.join('plots', f'{player}_scores.pgf'))
  plt.savefig(os.path.join('plots', f'{player}_scores.png'))

  plt.figure(figsize=(4,3))
  for d in depths:
    plt.plot(d)
  plt.xlabel('Time [seconds]')
  plt.ylabel('Reached Depth')
  plt.legend(legend_names)
  plt.tight_layout()
  plt.grid()
  plt.savefig(os.path.join('plots', f'{player}_depths.pgf'))
  plt.savefig(os.path.join('plots', f'{player}_depths.png'))


def tactical_indicators(analysis_name: str, folder: str, file_names: list[str]) -> None:

  if not os.path.exists('tables'):
    os.mkdir('tables')

  with open(os.path.join('tables', f'{analysis_name}_analysis.csv'), 'w') as f:

    f.write('name,reached_depth,stability,final_score\n')

    for name in file_names:

      csv_file = pd.read_csv(os.path.join(folder, f'{name}_history.csv'))

      best_move = csv_file[csv_file['multipv'] == 1]

      group_by_depth = best_move.groupby(['depth'])

      reached_depth = max(group_by_depth.indices)

      final_score = group_by_depth['score'].max().iloc[-1]
      
      stability = group_by_depth['score'].max().diff().abs().mean()

      f.write(f'{name},{reached_depth},{stability},{final_score}\n')


if __name__ == '__main__':
  f = open(os.path.join('data', 'best_black_moves.json'), 'r')
  moves = json.load(f)
  f.close()

  moves_white = []
  for name in moves:
    for white in moves[name]:
      moves_white.append(f'{name}_{white}')
  
  moves_black = []
  for name in moves:
    for white in moves[name]:
      for black in moves[name][white]:
        moves_black.append(f'{name}_{white}_{black}')
  
  tactical_indicators('white', 'output_move', moves_white)
  tactical_indicators('black', 'output_move', moves_black)

  mean_stability_plot(moves, ['Standard', 'FRC$_1$', 'FRC$_2$', 'FRC$_3$'])

  scores_depths_plot('output_move', 'white', [
    'standard_e2e4', 'ccrl1_h1g3', 'ccrl2_f2f4', 'ccrl3_f2f4'
  ], ['Standard', 'FRC$_1$', 'FRC$_2$', 'FRC$_3$'])

  scores_depths_plot('output_move', 'black', [
    'standard_e2e4_e7e6', 'ccrl1_h1g3_h8g6', 'ccrl2_f2f4_f7f5', 'ccrl3_f2f4_c7c5'
  ], ['Standard', 'FRC$_1$', 'FRC$_2$', 'FRC$_3$'])
