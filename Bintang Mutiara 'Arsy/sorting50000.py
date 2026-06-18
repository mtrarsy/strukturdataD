import numpy as np
rng = np.random.default_rng()
dummy_ints = rng.integers(0, 127000, size=(1, 50000))

print(dummy_ints)
