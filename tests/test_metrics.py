import pandas as pd
from src.metrics import (
    attrition_rate,
    attrition_by_department,
    attrition_by_overtime,
    average_income_by_attrition,
    satisfaction_summary,
)


def test_attrition_rate_returns_expected_percent():
    df = pd.DataFrame(
        {
            "employee_id": [1, 2, 3, 4],
            "department": ["Sales", "Sales", "HR", "HR"],
            "attrition": ["Yes", "No", "No", "Yes"],
        }
    )
    assert attrition_rate(df) == 50.0


def test_attrition_by_department_returns_expected_columns():
    df = pd.DataFrame(
        {
            "employee_id": [1, 2, 3, 4],
            "department": ["Sales", "Sales", "HR", "HR"],
            "attrition": ["Yes", "No", "No", "Yes"],
        }
    )
    result = attrition_by_department(df)
    assert list(result.columns) == ["department", "employees", "leavers", "attrition_rate"]


def test_attrition_by_department_computes_correct_rates():
    df = pd.DataFrame(
        {
            "employee_id": [1, 2, 3, 4, 5],
            "department": ["Sales", "Sales", "HR", "HR", "HR"],
            "attrition": ["Yes", "No", "Yes", "No", "No"],
        }
    )
    result = attrition_by_department(df)
    sales_row = result[result["department"] == "Sales"].iloc[0]
    hr_row = result[result["department"] == "HR"].iloc[0]

    assert sales_row["employees"] == 2
    assert sales_row["leavers"] == 1
    assert sales_row["attrition_rate"] == 50.0

    assert hr_row["employees"] == 3
    assert hr_row["leavers"] == 1
    assert round(hr_row["attrition_rate"], 2) == 33.33

    # Higher attrition department should appear first
    assert result.iloc[0]["department"] == "Sales"


def test_attrition_by_overtime_computes_correct_rates():
    df = pd.DataFrame(
        {
            "employee_id": [1, 2, 3, 4],
            "overtime": ["Yes", "Yes", "No", "No"],
            "attrition": ["Yes", "Yes", "No", "No"],
        }
    )
    result = attrition_by_overtime(df)
    yes_row = result[result["overtime"] == "Yes"].iloc[0]
    no_row = result[result["overtime"] == "No"].iloc[0]

    assert yes_row["employees"] == 2
    assert yes_row["leavers"] == 2
    assert yes_row["attrition_rate"] == 100.0

    assert no_row["employees"] == 2
    assert no_row["leavers"] == 0
    assert no_row["attrition_rate"] == 0.0


def test_average_income_by_attrition_returns_correct_means():
    df = pd.DataFrame(
        {
            "attrition": ["Yes", "Yes", "No", "No"],
            "monthly_income": [3000.0, 5000.0, 7000.0, 9000.0],
        }
    )
    result = average_income_by_attrition(df)
    assert list(result.columns) == ["attrition", "avg_monthly_income"]

    yes_row = result[result["attrition"] == "Yes"].iloc[0]
    no_row = result[result["attrition"] == "No"].iloc[0]

    assert yes_row["avg_monthly_income"] == 4000.0
    assert no_row["avg_monthly_income"] == 8000.0


def test_satisfaction_summary_computes_per_group_attrition_rate():
    # Satisfaction 1: 1 leaver out of 2 employees = 50%
    # Satisfaction 2: 1 leaver out of 3 employees = 33.33%
    # Total leavers = 2. The old buggy formula would give 50% for both groups.
    df = pd.DataFrame(
        {
            "employee_id": [1, 2, 3, 4, 5],
            "job_satisfaction": [1, 1, 2, 2, 2],
            "attrition": ["Yes", "No", "Yes", "No", "No"],
        }
    )
    result = satisfaction_summary(df)
    assert list(result.columns) == ["job_satisfaction", "total_employees", "leavers", "attrition_rate"]

    row1 = result[result["job_satisfaction"] == 1].iloc[0]
    row2 = result[result["job_satisfaction"] == 2].iloc[0]

    assert row1["total_employees"] == 2
    assert row1["leavers"] == 1
    assert row1["attrition_rate"] == 50.0

    assert row2["total_employees"] == 3
    assert row2["leavers"] == 1
    assert round(row2["attrition_rate"], 2) == 33.33


def test_satisfaction_summary_sorted_by_satisfaction():
    df = pd.DataFrame(
        {
            "employee_id": [1, 2, 3],
            "job_satisfaction": [3, 1, 2],
            "attrition": ["No", "Yes", "No"],
        }
    )
    result = satisfaction_summary(df)
    assert list(result["job_satisfaction"]) == [1, 2, 3]
