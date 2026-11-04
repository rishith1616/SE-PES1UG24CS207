"""Code Coverage Test Suite for food_delivery.py.

This test suite is designed to achieve 100% line (statement) coverage
for the food delivery pricing, coupon validation, and delivery time estimation module.
"""

import pytest
from food_delivery import delivery_charge, apply_coupon, estimated_time


class TestDeliveryChargeCodeCoverage:
    """Test suite covering all statements in delivery_charge()."""

    def test_distance_out_of_range_zero(self):
        """Line 5-6: distance_km <= 0 raises ValueError."""
        with pytest.raises(ValueError, match="out of delivery range"):
            delivery_charge(0, 200, False)

    def test_distance_out_of_range_negative(self):
        """Line 5-6: negative distance_km raises ValueError."""
        with pytest.raises(ValueError, match="out of delivery range"):
            delivery_charge(-2.5, 200, False)

    def test_distance_out_of_range_above_maximum(self):
        """Line 5-6: distance_km > 15 raises ValueError."""
        with pytest.raises(ValueError, match="out of delivery range"):
            delivery_charge(15.5, 200, False)

    def test_free_delivery_high_order_value(self):
        """Line 7-8: order_value >= 500 waives base delivery charge."""
        assert delivery_charge(5, 500, False) == 0

    def test_nearby_distance_tier(self):
        """Line 9-10: distance_km <= 3 charges ₹20 base fee."""
        assert delivery_charge(2, 200, False) == 20

    def test_mid_distance_tier(self):
        """Line 11-12: distance_km <= 8 charges ₹40 base fee."""
        assert delivery_charge(6, 200, False) == 40

    def test_far_distance_tier(self):
        """Line 13-14: distance_km > 8 charges ₹60 base fee."""
        assert delivery_charge(12, 200, False) == 60

    def test_rain_surcharge_applied(self):
        """Line 15-16: is_raining adds ₹30 surcharge."""
        assert delivery_charge(5, 200, True) == 70


class TestApplyCouponCodeCoverage:
    """Test suite covering all statements in apply_coupon()."""

    def test_none_coupon_returns_original_value(self):
        """Line 21-22: code is None returns order_value unchanged."""
        assert apply_coupon(300, None, False) == 300

    def test_unrecognized_coupon_raises_error(self):
        """Line 23-24: code not in COUPONS raises ValueError."""
        with pytest.raises(ValueError, match="invalid coupon"):
            apply_coupon(300, "NONEXISTENT", False)

    def test_welcome_coupon_rejected_for_returning_customer(self):
        """Line 25-26: WELCOME coupon on non-first order raises ValueError."""
        with pytest.raises(ValueError, match="coupon only for first order"):
            apply_coupon(300, "WELCOME", False)

    def test_order_value_below_minimum_threshold(self):
        """Line 27-28: order_value < 200 does not apply discount."""
        assert apply_coupon(150, "SAVE50", True) == 150

    def test_save50_coupon_applied(self):
        """Line 29: order_value >= 200 applies ₹50 discount."""
        assert apply_coupon(350, "SAVE50", False) == 300

    def test_welcome_coupon_first_order_applied(self):
        """Line 29: WELCOME coupon applies ₹100 discount for first order."""
        assert apply_coupon(400, "WELCOME", True) == 300


class TestEstimatedTimeCodeCoverage:
    """Test suite covering all statements in estimated_time()."""

    def test_standard_delivery_time(self):
        """Line 33-40: Base time calculation without peak hour or busy restaurant."""
        # 15 + (5 * 4) = 35 minutes
        assert estimated_time(5, False, False) == 35

    def test_peak_hour_only_delivery_time(self):
        """Line 34-35: Peak hour adds 10 minutes."""
        # 15 + (5 * 4) + 10 = 45 minutes
        assert estimated_time(5, True, False) == 45

    def test_restaurant_busy_non_peak_delivery_time(self):
        """Line 36-37: Busy restaurant adds 15 minutes."""
        # 15 + (5 * 4) + 15 = 50 minutes
        assert estimated_time(5, False, True) == 50

    def test_restaurant_busy_and_peak_hour_combined(self):
        """Line 38-39: Busy restaurant during peak hour adds 15 + 5 extra minutes."""
        # 15 + (5 * 4) + 10 (peak) + 15 (busy) + 5 (busy+peak) = 65 minutes
        assert estimated_time(5, True, True) == 65
