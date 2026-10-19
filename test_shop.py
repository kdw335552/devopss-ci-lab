from shop import order_total


def test_no_coupon():
    assert order_total([1000, 2000]) == 3000


def test_save10():
    assert order_total([10000]) * 0.9 == order_total([10000], "SAVE10")


def test_flat_never_negative():
    assert order_total([1000], "FLAT3000") == 0
