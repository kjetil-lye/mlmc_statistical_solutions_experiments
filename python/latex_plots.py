import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['savefig.dpi'] = 600
# see https://stackoverflow.com/a/46262952 (for norm symbol)
# and https://stackoverflow.com/a/23856968
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.preamble'] = [
    r'\usepackage{amsmath}',
    r'\usepackage{amsfonts}',
    r'\usepackage{amssymb}',
    #See https://tex.stackexchange.com/a/760
    '\def\Xint#1{\mathchoice',
    '{\\XXint\\displaystyle\\textstyle{#1}}%',
    '{\\XXint\\textstyle\\scriptstyle{#1}}%',
    '{\\XXint\\scriptstyle\\scriptscriptstyle{#1}}%',
    '{\\XXint\\scriptscriptstyle\\scriptscriptstyle{#1}}%',
    '\\!\\int}',
    '\\def\\XXint#1#2#3{{\\setbox0=\\hbox{$#1{#2#3}{\\int}$ }',
    '\\vcenter{\\hbox{$#2#3$ }}\\kern-.6\\wd0}}',
    '\\def\\ddashint{\\Xint=}',
    '\\def\\dashint{\\Xint-}'
]
import matplotlib.pyplot as plt
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
