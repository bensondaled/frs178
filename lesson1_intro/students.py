import numpy as np

def get_students():
    with open('names.txt') as f:
        names = f.readlines()

    names = [n.strip() for n in names]
    scores = np.random.normal(0.75, 0.1, size=len(names))
    return names,scores
