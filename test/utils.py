import numpy.testing as nt
import numpy as np

def assert_array_equal_ignorenan(a1, a2, *args, **kwargs):
    assert a1.shape == a2.shape, "Shapes %s and %s do not match." % (a1.shape, a2.shape)

    nan = np.isnan(a2)
    if np.count_nonzero(nan) > 0:
        a1 = a1.astype(a2.dtype)
        a1[nan] = float("nan")
    nt.assert_array_equal(a1, a2, *args, **kwargs)
