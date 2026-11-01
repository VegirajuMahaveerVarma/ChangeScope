from demo_pkg.service import get_value


def test_get_value():
    assert get_value() == 42
