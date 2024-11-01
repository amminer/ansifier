import pstats
import sys
from pstats import SortKey

if len(sys.argv) > 1 and sys.argv[1] == 'prev':
    directory = './prev_perf/'
else:
    directory = './perf/'

sizes = ((20*i, 20*i) for i in range(1,640//20))
for size in sizes:
    p = pstats.Stats(f'{directory}ansify_perf_{size[0]}_{size[1]}.profile')
    p.sort_stats(SortKey.CUMULATIVE)
    p.print_stats()
