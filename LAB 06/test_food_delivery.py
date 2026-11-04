"""Main test module for food delivery system.

Achieves 100% Code Coverage and 100% Branch Coverage.
"""

import pytest
from food_delivery import delivery_charge, apply_coupon, estimated_time

# Import all tests from both suites so running pytest on test_food_delivery.py
# achieves comprehensive 100% line & branch coverage
from CodeCoverageTest_food_delivery import *  # noqa: F401, F403
from BranchCoverageTest_food_delivery import *  # noqa: F401, F403


# Retain starter example test cases:
def test_nearby_small_order():
    assert delivery_charge(2, 200, False) == 20


def test_no_coupon():
    assert apply_coupon(300, None, False) == 300
