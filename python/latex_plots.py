import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['savefig.dpi'] = 600
# see https://stackoverflow.com/a/46262952 (for norm symbol)
# and https://stackoverflow.com/a/23856968
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.preamble'] = [
    r'\usepackage{amsmath}',
    r'\usepackage{amsfonts}',
    r'\usepackage{amssymb}']
import matplotlib.pyplot as plt
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
