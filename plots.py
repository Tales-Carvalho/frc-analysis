import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
import os

matplotlib.use('pgf')
matplotlib.rcParams.update({
  'pgf.texsystem': 'pdflatex',
  'font.family': 'serif',
  'text.usetex': True,
  'pgf.rcfonts': False,
})


def scores_depths_plot(file_names: list[str], legend_names: list[str]) -> None:

  scores = []
  depths = []

  for name in file_names:

    csv_file = pd.read_csv(os.path.join('output', f'{name}_history.csv'))

    best_move = csv_file[csv_file['multipv'] == 1]

    group_by_depth = best_move.groupby(['depth'])
    
    if not os.path.exists('plots'):
      os.mkdir('plots')
    
    # Score by depth
    score = group_by_depth['score'].max() # Max because white analysis - use min for black
    scores.append(score.rename(name))

    # plt.figure(figsize=(4,3))
    # plt.plot(score)
    # plt.xlabel('Depth')
    # plt.ylabel('Evaluation Score')
    # plt.tight_layout()
    # plt.grid()
    # plt.savefig(os.path.join('plots', f'{name}_score.eps'))

    # Depth by time
    time = group_by_depth['time'].min()
    depth = pd.Series(time.index.values, index=time)
    depths.append(depth.rename(name))

    # plt.figure(figsize=(4,3))
    # plt.plot(depth)
    # plt.xlabel('Time')
    # plt.ylabel('Reached Depth')
    # plt.tight_layout()
    # plt.grid()
    # plt.savefig(os.path.join('plots', f'{name}_depth.eps'))

  plt.figure(figsize=(4,3))
  for s in scores:
    plt.plot(s)
  plt.xlabel('Depth')
  plt.ylabel('Evaluation Score')
  plt.legend(legend_names)
  plt.tight_layout()
  plt.grid()
  plt.savefig(os.path.join('plots', f'scores.pgf'))

  plt.figure(figsize=(4,3))
  for d in depths:
    plt.plot(d)
  plt.xlabel('Time')
  plt.ylabel('Reached Depth')
  plt.legend(legend_names)
  plt.tight_layout()
  plt.grid()
  plt.savefig(os.path.join('plots', f'depths.pgf'))


if __name__ == '__main__':
  scores_depths_plot(
    ['standard', 'ccrl1', 'ccrl2', 'ccrl3'],
    ['Standard', 'FRC$_1$', 'FRC$_2$', 'FRC$_3$']
  )
