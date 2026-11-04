# Lab 6: Code and Branch Coverage Analysis — Food Delivery

**Course:** Software Engineering (SE) Lab  
**Student Name:** Rishith  
**SRN:** PES1UG24CS207  
**Assigned Repository:** [SETAPESU26/L6_L7_20_food_delivery](https://github.com/SETAPESU26/L6_L7_20_food_delivery)  
**Submission Repository:** [rishith1616/SE-PES1UG24CS207](https://github.com/rishith1616/SE-PES1UG24CS207)  

---

## Overview

This lab focuses on measuring, analyzing, and improving software test completeness using Python's `coverage` library and `pytest`. Testing is evaluated across two critical testing dimensions:
- **Code (Line) Coverage:** Measuring the proportion of executable statements traversed by the test suite.
- **Branch Coverage:** Measuring whether each conditional decision point (`if`, `elif`, `else`, boolean guards) evaluates to both `True` and `False`.

The system under test is `food_delivery.py`, which provides three core functions:
1. `delivery_charge(distance_km, order_value, is_raining)`: Calculates delivery fee based on distance boundaries (<= 0 km error, > 15 km error, <= 3 km ₹20, <= 8 km ₹40, > 8 km ₹60), free delivery for orders >= ₹500, and a ₹30 rain surcharge.
2. `apply_coupon(order_value, code, is_first_order)`: Validates coupons (`SAVE50`, `WELCOME`), enforces first-order restriction on `WELCOME`, enforces a minimum order threshold of ₹200, and applies discounts.
3. `estimated_time(distance_km, is_peak_hour, restaurant_busy)`: Computes base delivery minutes (15 + 4 × distance), adding 10 mins during peak hours, 15 mins when the restaurant is busy, and an additional 5 mins when busy during peak hours.

---

## Deliverables & Analysis Artifacts

| Deliverable | Description | File Link |
| :--- | :--- | :--- |
| **Application Script** | The module under test | [`food_delivery.py`](food_delivery.py) |
| **Code Coverage Test Suite** | Test cases targeting 100% statement (line) coverage | [`CodeCoverageTest_food_delivery.py`](CodeCoverageTest_food_delivery.py) |
| **Branch Coverage Test Suite** | Test cases targeting 100% branch and boundary coverage | [`BranchCoverageTest_food_delivery.py`](BranchCoverageTest_food_delivery.py) |
| **Master Test Script** | Complete unified test runner (imports both suites + starter tests) | [`test_food_delivery.py`](test_food_delivery.py) |
| **Student Handout** | Official lab instructions & guidelines | [`Lab_6_Code&BranchCoverage_Student_Handout.pdf`](Lab_6_Code&BranchCoverage_Student_Handout.pdf) |
| **Code Coverage Screenshot** | Terminal output screenshot demonstrating 100% line coverage | [`screenshots/code_coverage_analysis.png`](screenshots/code_coverage_analysis.png) |
| **Branch Coverage Screenshot** | Terminal output screenshot demonstrating 100% branch coverage | [`screenshots/branch_coverage_analysis.png`](screenshots/branch_coverage_analysis.png) |
| **Code Coverage Report** | Plaintext terminal report for line coverage | [`reports/code_coverage_report.txt`](reports/code_coverage_report.txt) |
| **Branch Coverage Report** | Plaintext terminal report for branch coverage | [`reports/branch_coverage_report.txt`](reports/branch_coverage_report.txt) |
| **Initial Baseline Report** | Baseline report from starter test (36% line, 30% branch) | [`reports/initial_coverage_report.txt`](reports/initial_coverage_report.txt) |

---

## Directory Structure

```
LAB 06/
├── .gitignore
├── food_delivery.py
├── CodeCoverageTest_food_delivery.py
├── BranchCoverageTest_food_delivery.py
├── test_food_delivery.py
├── Lab_6_Code&BranchCoverage_Student_Handout.pdf
├── README.md
├── screenshots/
│   ├── code_coverage_analysis.png
│   └── branch_coverage_analysis.png
└── reports/
    ├── initial_coverage_report.txt
    ├── code_coverage_report.txt
    └── branch_coverage_report.txt
```

---

## Coverage Analysis & Comparison

```
+------------------------------------+--------------------+--------------------+
| Metric                             | Initial Baseline   | Final Achieved     |
+------------------------------------+--------------------+--------------------+
| Line (Statement) Coverage          | 36% (21 missed)    | 100% (0 missed)    |
| Branch Coverage                    | 30% (5 partial)    | 100% (0 missed)    |
| Passing Unit Tests                 | 2 passed           | 32 passed          |
| Missing Lines / Untested Branches  | 21 lines / 5 part  | 0 lines / 0 br     |
+------------------------------------+--------------------+--------------------+
```

### Initial Coverage (Starter Test Case):
- Total statements: 33
- Executed statements: 12 (36% line coverage)
- Missed statements: 21 (`6, 8, 11-14, 16, 23-29, 33-40`)
- Branch coverage: 30% (5 partial branches)

### Final Coverage (Targeted Test Suites):
- Total statements in module: 33 / 33 executed (**100% Line Coverage**)
- Total branches in module: 24 / 24 evaluated both True and False (**100% Branch Coverage**)
- Missing statements: **None (0)**
- Missing branches: **None (0)**

---

## Line Coverage vs. Branch Coverage: Key Takeaways

1. **Why Line Coverage is Insufficient:**
   - Line coverage checks only whether an instruction was executed at least once.
   - For example, if a conditional `if is_raining:` executes when `is_raining` is `True`, line coverage reports 100% for that block even if the `False` branch (order without rain) has never been tested.
2. **The Power of Branch Coverage:**
   - Branch coverage enforces testing of all decision outcomes.
   - In `food_delivery.py`, branch testing verified critical boundary and compound conditions:
     - `distance_km <= 0` vs `distance_km > 15` vs valid distance boundaries (`0.1`, `3.0`, `8.0`, `15.0`).
     - `order_value >= 500` (free delivery boundary at ₹500 and ₹499.99).
     - Compound first-order restriction: `code == "WELCOME" and not is_first_order`.
     - Coupon minimum order threshold: `order_value < 200` (boundary at ₹199.99 and ₹200).
     - Delivery time nested condition: busy restaurant during peak hour (+5 min extra) vs non-peak.

---

## Reproduction Commands

To reproduce the test executions and generate the coverage reports:

```bash
# Navigate to LAB 06 directory
cd "LAB 06"

# 1. Run Line Coverage
coverage run -m pytest CodeCoverageTest_food_delivery.py
coverage report -m

# 2. Run Branch Coverage
coverage run --branch -m pytest BranchCoverageTest_food_delivery.py
coverage report -m

# 3. Run Master Test Suite (all tests combined)
coverage run --branch -m pytest test_food_delivery.py
coverage report -m
```
