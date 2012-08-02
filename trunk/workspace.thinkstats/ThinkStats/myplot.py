"""This file contains code for use with "Think Stats",
by Allen B. Downey, available from greenteapress.com

Copyright 2010 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

import math
import matplotlib
import matplotlib.pyplot as pyplot
import numpy as np

# customize some matplotlib attributes
#matplotlib.rc('figure', figsize=(4, 3))

matplotlib.rc('font', size=14.0)
#matplotlib.rc('axes', labelsize=22.0, titlesize=22.0)
#matplotlib.rc('legend', fontsize=20.0)

#matplotlib.rc('xtick.major', size=6.0)
#matplotlib.rc('xtick.minor', size=3.0)

#matplotlib.rc('ytick.major', size=6.0)
#matplotlib.rc('ytick.minor', size=3.0)


class InfiniteList(list):
    def __init__(self, val):
        self.val = val

    def __getitem__(self, index):
        return self.val


def Underride(d, **options):
    """Add key-value pairs to d only if key is not in d.

    If d is None, create a new dictionary.
    """
    if d is None:
        d = {}

    for key, val in options.iteritems():
        d.setdefault(key, val)

    return d


def Clf():
    """Clears the figure."""
    pyplot.clf()


def Plot(xs, ys, style='', **options):
    """Plots a line.

    Args:
      xs: sequence of x values
      ys: sequence of y values
      style: style string passed along to pyplot.plot
    """
    options = Underride(options, linewidth=3, alpha=0.5)
    pyplot.plot(xs, ys, style, **options)


def Pmf(pmf, **options):
    """Plots a Pmf or Hist as a line.

    Args:
      pmf: Hist or Pmf object
    """
    xs, ps = pmf.Render()
    options = Underride(options, label=pmf.name)
    Plot(xs, ps, **options)


def Pmfs(pmfs, **options):
    """Plots a sequence of PMFs.
    
    Args:
      pmfs: sequence of PMF objects
    """
    for i, pmf in enumerate(pmfs):
        Pmf(pmf, **options)


def Hist(hist, **options):
    """Plots a Pmf or Hist with a bar plot.

    Args:
      hist: Hist or Pmf object
    """
    # find the minimum distance between adjacent values
    xs, fs = hist.Render()
    width = min(Diff(xs))

    options = Underride(options, 
                        label=hist.name,
                        align='center',
                        edgecolor='blue',
                        width=width)

    pyplot.bar(xs, fs, **bar_options)


def Hists(hists, **options):
    """Plots two histograms as interleaved bar plots.

    Args:
      hists: list of two Hist or Pmf objects
    """
    width = 0.4
    shifts = [-width, 0.0]

    for i, hist in enumerate(hists):
        xs, fs = hist.Render()
        xs = Shift(xs, shifts[i])
        pyplot.bar(xs, fs, label=hist.name, width=width, **options)


def Shift(xs, shift):
    """Adds a constant to a sequence of values.

    Args:
      xs: sequence of values

      shift: value to add

    Returns:
      sequence of numbers
    """
    return [x+shift for x in xs]


def Diff(t):
    """Compute the differences between adjacent elements in a sequence.

    Args:
        t: sequence of number

    Returns:
        sequence of differences (length one less than t)
    """
    diffs = [t[i+1] - t[i] for i in range(len(t)-1)]
    return diffs


def Cdf(cdf, complement=False, transform=None, **options):
    """Plots a CDF as a line.

    Args:
      cdf: Cdf object
      complement: boolean, whether to plot the complementary CDF
      transform: string, one of 'exponential', 'pareto', 'weibull', 'gumbel'
    """
    xs, ps = cdf.Render()

    if transform == 'exponential':
        complement = True
        options['yscale'] = 'log'

    if transform == 'pareto':
        complement = True
        options['yscale'] = 'log'
        options['xscale'] = 'log'

    if complement:
        ps = [1.0-p for p in ps]

    if transform == 'weibull':
        xs.pop()
        ps.pop()
        ps = [-math.log(1.0-p) for p in ps]
        options['xscale'] = 'log'
        options['yscale'] = 'log'

    if transform == 'gumbel':
        xs.pop(0)
        ps.pop(0)
        ps = [-math.log(p) for p in ps]
        options['yscale'] = 'log'

    line = pyplot.plot(xs, ps, label=cdf.name, **options)


def Cdfs(cdfs, complement=False, transform=None, **options):
    """Plots a sequence of CDFs.
    
    Args:
      cdfs: sequence of CDF objects
      complement: boolean, whether to plot the complementary CDF
      transform: string, one of 'exponential', 'pareto', 'weibull', 'gumbel'
    """
    for i, cdf in enumerate(cdfs):
        Cdf(cdf, complement, transform, **options)


def Contour(d, pcolor=False, contour=True, **options):
    """Makes a contour plot.
    
    d: map from (x, y) to z
    """
    xs, ys = zip(*d.iterkeys())
    xs = sorted(list(xs))
    ys = sorted(list(ys))

    X, Y = np.meshgrid(xs, ys)
    func = lambda x, y: d.get((x, y))
    func = np.vectorize(func)
    Z = func(X, Y)

    if pcolor:
        pyplot.pcolor(X, Y, Z, **options)
    if contour:
        cs = pyplot.contour(X, Y, Z, **options)
        pyplot.clabel(cs, inline=1, fontsize=10)

def Config(**options):
    """Configures the plot.

    Pulls options out of the option dictionary and passes them to
    title, xlabel, ylabel, xscale, yscale, xticks, yticks, axis, legend,
    and loc.
    """
    title = options.get('title', '')
    pyplot.title(title)

    xlabel = options.get('xlabel', '')
    pyplot.xlabel(xlabel)

    ylabel = options.get('ylabel', '')
    pyplot.ylabel(ylabel)

    if 'xscale' in options:
        pyplot.xscale(options['xscale'])

    if 'xticks' in options:
        pyplot.xticks(*options['xticks'])

    if 'yscale' in options:
        pyplot.yscale(options['yscale'])

    if 'yticks' in options:
        pyplot.yticks(*options['yticks'])

    if 'axis' in options:
        pyplot.axis(options['axis'])

    loc = options.get('loc', 0)
    legend = options.get('legend', True)
    if legend:
        pyplot.legend(loc=loc)


def Show(**options):
    """Shows the plot."""
    # TODO: figure out how to show more than one plot
    Config(**options)
    pyplot.show()


def Save(root=None, formats=None, **options):
    """Saves the plot in the given formats.

    Args:
      root: string filename root
      formats: list of string formats
      options: dictionary of options
    """
    Config(**options)

    if formats is None:
        formats = ['pdf', 'png']

    if root:
        for format in formats:
            SaveFormat(root, format)


def SaveFormat(root, format='eps'):
    """Writes the current figure to a file in the given format.

    Args:
      root: string filename root

      format: string format
    """
    filename = '%s.%s' % (root, format)
    print 'Writing', filename
    pyplot.savefig(filename, format=format, dpi=300)


