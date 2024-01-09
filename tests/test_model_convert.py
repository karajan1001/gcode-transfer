import numpy as np
from gcode_transfer.model_convert import sampling_line


def test_sampling_line():
    start = np.asarray([0.0,0.0,3.0])
    end = np.asarray([3.0,0.0,3.0])
    assert len(sampling_line(start, end, 0.9)) == 5 * 4
    assert len(sampling_line(start, end, 4)) == 2 * 4
