import pytest

from rc.geometry import sheet_coords_to_angles, angles_to_coords

test_profile = {
    'upper_arm_length': 124,
    'upper_arm_angle_offset': -10,
    'forearm_length': 160,
    'forearm_arm_angle_offset': 10,
    'sheet_distance': 100,
}

TOLERANCE = 0.1

@pytest.mark.parametrize('x', ([50, 100, 150]), )
@pytest.mark.parametrize('y', ([0, 75, 150]), )
def test_reversed_transform(x, y):
    a, b = sheet_coords_to_angles(x, y, test_profile, safe=False)
    x0, y0 = angles_to_coords(a, b, test_profile)
    assert abs(x - x0) < TOLERANCE
    assert abs(y - y0) < TOLERANCE
