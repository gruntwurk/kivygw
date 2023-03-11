from kivygw import (
    float_tuple, int_tuple, is_float_tuple,
    color_outline
    )
import pytest


def test_float_tuples():
    assert is_float_tuple((0.5, 0.0, 1.0))
    assert is_float_tuple((0.5, 0.0, 1.0, 1.0))
    assert is_float_tuple((0, 0, 0, 0))
    assert is_float_tuple((0, 0, 0, 1))
    assert is_float_tuple((0, 0, 1, 1))
    assert is_float_tuple((0, 1, 1, 1))
    assert is_float_tuple((1, 1, 1, 1))
    assert is_float_tuple((0, 0, 0))
    assert is_float_tuple((1, 1, 1))
    assert not is_float_tuple((2, 1, 1, 1))
    assert not is_float_tuple((0.5, 0.5, 0.5, 1.1))
    assert not is_float_tuple((0.5, 0.5, 1.1))
    assert not is_float_tuple((-0.1, 1, 1, 1))
    assert len(float_tuple((224, 238, 238))) == 3
    assert len(float_tuple((224, 238, 238, 99))) == 4
    with pytest.raises(ValueError) as e_info:
        _ = float_tuple((224, 238))
        assert e_info == "float_tuple() requires a 3-tuple or a 4-tuple, but a 2-tuple was given."
    with pytest.raises(ValueError) as e_info:
        _ = float_tuple((224, 238, 30, 40, 50))
        assert e_info == "float_tuple() requires a 3-tuple or a 4-tuple, but a 5-tuple was given."

    ft = float_tuple((224, 238, 238))
    assert is_float_tuple(ft)
    assert ft[0] < 1.0
    assert ft[1] < 1.0
    assert ft[2] < 1.0
    it = int_tuple(ft)
    assert it == (224, 238, 238)

    assert int_tuple((0, 0, 0)) == (0, 0, 0)
    assert int_tuple((0, 0, 0, 0)) == (0, 0, 0, 0)

    assert int_tuple((1, 1, 1)) == (255, 255, 255)
    assert int_tuple((1, 1, 1, 1)) == (255, 255, 255, 255)

    assert int_tuple((0.25, 0.5, 0.75)) == (63, 127, 191)
    assert int_tuple((0.25, 0.5, 0.75, 1.0)) == (63, 127, 191, 255)
    assert int_tuple((0.25, 0.5, 0.75, 0.999)) == (63, 127, 191, 255)


def test_color_outline():
    assert color_outline((0, 0, 0)) == (1, 1, 1)
    assert color_outline((4, 0, 0)) == (255, 255, 255)
    assert color_outline((0.1, 0, 0)) == (1, 1, 1)
    assert color_outline((230, 0, 0)) == (255, 255, 255)
    assert color_outline((230, 230, 0)) == (0, 0, 0)
    assert is_float_tuple((0.7, 0.8, 0))
    assert color_outline((0.7, 0.8, 0.2)) == (0, 0, 0)

