"""Branch Coverage Test Suite for food_delivery.py.

This suite is systematically designed to evaluate every decision branch,
conditional statement, and boundary condition to achieve 100% branch coverage:
- Distance range boundaries: <= 0, > 15, and valid lower/upper extremes
- Order value discount boundary: >= 500 vs < 500
- Distance tier boundaries: <= 3, <= 8, and > 8
- Weather condition branches: is_raining True vs False across all tiers
- Coupon code presence: code is None vs not None
- Coupon validity membership: code in COUPONS vs not in COUPONS
- First-order compound logic: code == 'WELCOME' and not is_first_order
- Order value coupon eligibility threshold: order_value < 200 vs >= 200
- Delivery time combinations: full 2x2 truth table for is_peak_hour and restaurant_busy
"""

import pytest
from food_delivery import delivery_charge, apply_coupon, estimated_time


class TestDeliveryChargeBranchCoverage:
    """Test decision branches and boundary conditions in delivery_charge()."""

    def test_distance_exact_zero_boundary(self):
        """Branch: distance_km <= 0 is True (boundary value 0)."""
        with pytest.raises(ValueError, match="out of delivery range"):
            delivery_charge(0, 300, False)

    def test_distance_negative_branch(self):
        """Branch: distance_km <= 0 is True (negative value -1)."""
        with pytest.raises(ValueError, match="out of delivery range"):
            delivery_charge(-1, 300, False)

    def test_distance_above_maximum_boundary(self):
        """Branch: distance_km > 15 is True (boundary value 15.01)."""
        with pytest.raises(ValueError, match="out of delivery range"):
            delivery_charge(15.01, 300, False)

    def test_distance_far_above_maximum(self):
        """Branch: distance_km > 15 is True (value 25)."""
        with pytest.raises(ValueError, match="out of delivery range"):
            delivery_charge(25, 300, False)

    def test_distance_valid_minimum_boundary(self):
        """Branch: distance_km <= 0 is False, distance_km > 15 is False (0.1 km)."""
        assert delivery_charge(0.1, 200, False) == 20

    def test_distance_valid_maximum_boundary(self):
        """Branch: distance_km == 15.0 is False for > 15, evaluates to > 8 tier."""
        assert delivery_charge(15.0, 200, False) == 60

    def test_order_value_exact_free_delivery_boundary(self):
        """Branch: order_value >= 500 is True (exact boundary 500)."""
        assert delivery_charge(5, 500, False) == 0

    def test_order_value_above_free_delivery(self):
        """Branch: order_value >= 500 is True (value 750)."""
        assert delivery_charge(10, 750, False) == 0

    def test_order_value_free_delivery_with_rain_surcharge(self):
        """Branch: order_value >= 500 is True, is_raining is True (0 + 30 = 30)."""
        assert delivery_charge(5, 500, True) == 30

    def test_order_value_just_below_free_delivery_boundary(self):
        """Branch: order_value >= 500 is False (boundary 499.99)."""
        assert delivery_charge(2, 499.99, False) == 20

    def test_tier_nearby_exact_boundary(self):
        """Branch: distance_km <= 3 is True (exact boundary 3.0)."""
        assert delivery_charge(3.0, 200, False) == 20

    def test_tier_nearby_with_rain(self):
        """Branch: distance_km <= 3 is True, is_raining is True (20 + 30 = 50)."""
        assert delivery_charge(2.0, 200, True) == 50

    def test_tier_nearby_just_above_boundary(self):
        """Branch: distance_km <= 3 is False, falls to <= 8 (boundary 3.01)."""
        assert delivery_charge(3.01, 200, False) == 40

    def test_tier_mid_exact_boundary(self):
        """Branch: distance_km <= 8 is True (exact boundary 8.0)."""
        assert delivery_charge(8.0, 200, False) == 40

    def test_tier_mid_with_rain(self):
        """Branch: distance_km <= 8 is True, is_raining is True (40 + 30 = 70)."""
        assert delivery_charge(6.0, 200, True) == 70

    def test_tier_mid_just_above_boundary(self):
        """Branch: distance_km <= 8 is False, falls to else (boundary 8.01)."""
        assert delivery_charge(8.01, 200, False) == 60

    def test_tier_far_without_rain(self):
        """Branch: else (distance_km > 8), is_raining is False."""
        assert delivery_charge(12.0, 200, False) == 60

    def test_tier_far_with_rain(self):
        """Branch: else (distance_km > 8), is_raining is True (60 + 30 = 90)."""
        assert delivery_charge(12.0, 200, True) == 90


class TestApplyCouponBranchCoverage:
    """Test decision branches and boolean predicates in apply_coupon()."""

    def test_coupon_is_none_branch(self):
        """Branch: code is None is True."""
        assert apply_coupon(350, None, False) == 350
        assert apply_coupon(350, None, True) == 350

    def test_coupon_not_none_invalid_code_branch(self):
        """Branch: code is None is False, code not in COUPONS is True."""
        with pytest.raises(ValueError, match="invalid coupon"):
            apply_coupon(300, "FLAT50", False)

    def test_coupon_case_sensitive_invalid_branch(self):
        """Branch: code not in COUPONS is True (lowercase 'save50')."""
        with pytest.raises(ValueError, match="invalid coupon"):
            apply_coupon(300, "save50", False)

    def test_welcome_coupon_returning_user_branch(self):
        """Branch: code == 'WELCOME' is True, not is_first_order is True."""
        with pytest.raises(ValueError, match="coupon only for first order"):
            apply_coupon(300, "WELCOME", False)

    def test_welcome_coupon_first_order_eligible_branch(self):
        """Branch: code == 'WELCOME' is True, not is_first_order is False."""
        # 300 - 100 = 200
        assert apply_coupon(300, "WELCOME", True) == 200

    def test_save50_coupon_non_first_order_branch(self):
        """Branch: code == 'WELCOME' is False (SAVE50), not is_first_order is True."""
        # SAVE50 does not require first order: 300 - 50 = 250
        assert apply_coupon(300, "SAVE50", False) == 250

    def test_save50_coupon_first_order_branch(self):
        """Branch: code == 'WELCOME' is False (SAVE50), not is_first_order is False."""
        assert apply_coupon(300, "SAVE50", True) == 250

    def test_order_value_below_200_boundary(self):
        """Branch: order_value < 200 is True (boundary 199.99)."""
        assert apply_coupon(199.99, "SAVE50", False) == 199.99

    def test_order_value_exact_200_boundary(self):
        """Branch: order_value < 200 is False (exact boundary 200)."""
        # 200 - 50 = 150
        assert apply_coupon(200, "SAVE50", False) == 150

    def test_order_value_above_200_welcome_discount(self):
        """Branch: order_value < 200 is False (value 250 with WELCOME)."""
        # 250 - 100 = 150
        assert apply_coupon(250, "WELCOME", True) == 150


class TestEstimatedTimeBranchCoverage:
    """Test full decision matrix for estimated_time()."""

    def test_condition_neither_peak_nor_busy(self):
        """Branch: is_peak_hour is False, restaurant_busy is False."""
        # 15 + (4 * 5) = 35 minutes
        assert estimated_time(5, False, False) == 35

    def test_condition_peak_hour_only(self):
        """Branch: is_peak_hour is True, restaurant_busy is False."""
        # 15 + (4 * 5) + 10 = 45 minutes
        assert estimated_time(5, True, False) == 45

    def test_condition_restaurant_busy_only(self):
        """Branch: is_peak_hour is False, restaurant_busy is True."""
        # 15 + (4 * 5) + 15 = 50 minutes (nested is_peak_hour is False)
        assert estimated_time(5, False, True) == 50

    def test_condition_both_peak_and_busy(self):
        """Branch: is_peak_hour is True, restaurant_busy is True (nested is_peak_hour is True)."""
        # 15 + (4 * 5) + 10 + 15 + 5 = 65 minutes
        assert estimated_time(5, True, True) == 65
