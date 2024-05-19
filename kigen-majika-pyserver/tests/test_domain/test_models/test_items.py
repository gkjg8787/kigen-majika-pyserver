from domain.models import JanCode


def test_create_jancode_half_width():
    base = "0123456789012"
    jan_code = JanCode(value=base)
    assert jan_code.value == base


def test_create_jancode_full_width():
    base = "０１２３４５６７８９０１２"
    jan_code = JanCode(value=base)
    comparing_data = "0123456789012"
    assert jan_code.value == comparing_data
