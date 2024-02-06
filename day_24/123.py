import itertools

with open('input.txt') as f:
    hailstorms = [ln.strip().split(' @ ') for ln in f]
    hailstorms = [([int(x) for x in p.split(',')], [int(x) for x in v.split(',')]) for p, v in hailstorms]

# refer to https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
count = 0
minc, maxc = 200000000000000, 400000000000000
for a, b in itertools.combinations(hailstorms, 2):
    def cross(v, w):
        return v[0] * w[1] - v[1] * w[0]

    (p, r), (q, s) = a, b
    rxs = cross(r, s)
    if rxs == 0:  # parallel or collinear
        continue
    q_minus_p = [i - j for i, j in zip(q, p)]
    t = cross(q_minus_p, s) / rxs
    u = cross(q_minus_p, r) / rxs
    if t < 0 or u < 0:  # past
        continue
    intersection = [pi + t * ri for pi, ri in zip(p, r)]
    if minc <= intersection[0] <= maxc and minc <= intersection[1] <= maxc:
        count += 1

print(count)

# part 2
# refer to https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
# you can see that (p - q) x (r - s) = 0, because t == u.
# pick any 3 hailstorms and you get 6 equations for 6 unknowns.

import numpy as np

(p1, v1), (p2, v2), (p3, v3) = hailstorms[:3]

A = np.array([
    [-(v1[1] - v2[1]), v1[0] - v2[0], 0, p1[1] - p2[1], -(p1[0] - p2[0]), 0],
    [-(v1[1] - v3[1]), v1[0] - v3[0], 0, p1[1] - p3[1], -(p1[0] - p3[0]), 0],

    [0, -(v1[2] - v2[2]), v1[1] - v2[1],  0, p1[2] - p2[2], -(p1[1] - p2[1])],
    [0, -(v1[2] - v3[2]), v1[1] - v3[1],  0, p1[2] - p3[2], -(p1[1] - p3[1])],

    [-(v1[2] - v2[2]), 0, v1[0] - v2[0],  p1[2] - p2[2], 0, -(p1[0] - p2[0])],
    [-(v1[2] - v3[2]), 0, v1[0] - v3[0],  p1[2] - p3[2], 0, -(p1[0] - p3[0])]
    ])

b = [
        (p1[1] * v1[0] - p2[1] * v2[0]) - (p1[0] * v1[1] - p2[0] * v2[1]),
        (p1[1] * v1[0] - p3[1] * v3[0]) - (p1[0] * v1[1] - p3[0] * v3[1]),

        (p1[2] * v1[1] - p2[2] * v2[1]) - (p1[1] * v1[2] - p2[1] * v2[2]),
        (p1[2] * v1[1] - p3[2] * v3[1]) - (p1[1] * v1[2] - p3[1] * v3[2]),

        (p1[2] * v1[0] - p2[2] * v2[0]) - (p1[0] * v1[2] - p2[0] * v2[2]),
        (p1[2] * v1[0] - p3[2] * v3[0]) - (p1[0] * v1[2] - p3[0] * v3[2])
     ]

x = np.linalg.solve(A, b)
x = [float(i) for i in x]
print(x)

print(round(sum(x[:3])))