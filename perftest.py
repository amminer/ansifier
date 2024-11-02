import cProfile
from ansifier import ansify


filepath = '/home/meelz/Downloads/FUITC.mp4'
sizes = ((20*i, 20*i) for i in range(1, 640//20))
for size in sizes:
    if size[0] < 500 or size[0] > 520: continue
    cProfile.run(
        f'print({size}); ansify("{filepath}", height={size[0]}, width={size[1]})',
        f'./perf/ansify_perf_{size[0]}_{size[1]}.profile')
