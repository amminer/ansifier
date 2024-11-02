import pstats
import sys
from os import listdir
from os.path import join
from pstats import SortKey

if len(sys.argv) > 1 and sys.argv[1] == 'prev':
    directory = './prev_perf/'
else:
    directory = './perf/'

for f in listdir(directory):
    p = pstats.Stats(join(directory, f))
    p.sort_stats(SortKey.CUMULATIVE)
    p.print_stats()
