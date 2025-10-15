import pytest
from decimal import Decimal
from datetime import datetime
from app.calculation import Calculation
from app.exceptions import OperationError
import logging


def test_addition():
    calc = Calculation(operation="Addition", operand1=Decimal("2"), operand2=Decimal("3"))
    assert calc.result == Decimal("5")


def test_subtraction():
    calc = Calculation(operation="Subtraction", operand1=Decimal("5"), operand2=Decimal("3"))
    assert calc.result == Decimal("2")


def test_multiplication():
    calc = Calculation(operation="Multiplication", operand1=Decimal("4"), operand2=Decimal("2"))
    assert calc.result == Decimal("8")


def test_division():
    calc = Calculation(operation="Division", operand1=Decimal("8"), operand2=Decimal("2"))
    assert calc.result == Decimal("4")


def test_division_by_zero():
    with pytest.raises(OperationError, match="Division by zero is not allowed"):
        Calculation(operation="Division", operand1=Decimal("8"), operand2=Decimal("0"))


def test_power():
    calc = Calculation(operation="Power", operand1=Decimal("2"), operand2=Decimal("3"))
    assert calc.result == Decimal("8")


def test_negative_power():
    with pytest.raises(OperationError, match="Negative exponents are not supported"):
        Calculation(operation="Power", operand1=Decimal("2"), operand2=Decimal("-3"))


def test_root():
    calc = Calculation(operation="Root", operand1=Decimal("16"), operand2=Decimal("2"))
    assert calc.result == Decimal("4")


def test_invalid_root():
    with pytest.raises(OperationError, match="Cannot calculate root of negative number"):
        Calculation(operation="Root", operand1=Decimal("-16"), operand2=Decimal("2"))


def test_modulus_standard():
    """Test standard positive modulus (10 % 3 = 1)."""
    calc = Calculation(operation="Modulus", operand1=Decimal("10"), operand2=Decimal("3"))
    assert calc.result == Decimal("1")

def test_modulus_with_decimal_result():
    """Test modulus with decimal operands (5.5 % 2 = 1.5)."""
    calc = Calculation(operation="Modulus", operand1=Decimal("5.5"), operand2=Decimal("2"))
    assert calc.result == Decimal("1.5")

def test_modulus_division_by_zero():
    """Test modulus fails on division by zero."""
    with pytest.raises(OperationError, match="Cannot divide by zero"):
        Calculation(operation="Modulus", operand1=Decimal("10"), operand2=Decimal("0"))

# --- Integer Division Tests ---

def test_integer_division_standard():
    """Test standard integer division (10 // 3 = 3)."""
    calc = Calculation(operation="Integer Division", operand1=Decimal("10"), operand2=Decimal("3"))
    assert calc.result == Decimal("3")

def test_integer_division_flooring():
    """Test integer division correctly floors negative results (-10 // 3 = -4)."""
    calc = Calculation(operation="Integer Division", operand1=Decimal("-10"), operand2=Decimal("3"))
    assert calc.result == Decimal("-4")

def test_integer_division_by_zero():
    """Test integer division fails on division by zero."""
    with pytest.raises(OperationError, match="Cannot divide by zero"):
        Calculation(operation="Integer Division", operand1=Decimal("10"), operand2=Decimal("0"))

# --- Percentage Calculation Tests ---

def test_percentage_standard():
    """Test standard percentage calculation (50 is 50% of 100)."""
    calc = Calculation(operation="Percentage", operand1=Decimal("50"), operand2=Decimal("100"))
    assert calc.result == Decimal("50")

def test_percentage_over_hundred():
    """Test calculation where result is over 100% (10 is 200% of 5)."""
    calc = Calculation(operation="Percentage", operand1=Decimal("10"), operand2=Decimal("5"))
    assert calc.result == Decimal("200")

def test_percentage_division_by_zero():
    """Test percentage calculation fails on division by zero."""
    with pytest.raises(OperationError, match="Cannot divide by zero"):
        Calculation(operation="Percentage", operand1=Decimal("10"), operand2=Decimal("0"))

# --- Absolute Difference Tests ---

def test_absolute_difference_standard():
    """Test standard absolute difference (|10 - 5| = 5)."""
    calc = Calculation(operation="Absolute Difference", operand1=Decimal("10"), operand2=Decimal("5"))
    assert calc.result == Decimal("5")

def test_absolute_difference_negative_result():
    """Test absolute difference when the subtraction is negative (|5 - 10| = 5)."""
    calc = Calculation(operation="Absolute Difference", operand1=Decimal("5"), operand2=Decimal("10"))
    assert calc.result == Decimal("5")

def test_absolute_difference_mixed_signs():
    """Test absolute difference with mixed signs (|10 - (-5)| = 15)."""
    calc = Calculation(operation="Absolute Difference", operand1=Decimal("10"), operand2=Decimal("-5"))
    assert calc.result == Decimal("15")

def test_absolute_difference_decimal_precision():
    """Test absolute difference maintaining decimal precision."""
    calc = Calculation(operation="Absolute Difference", operand1=Decimal("4.3"), operand2=Decimal("5.1"))
    assert calc.result == Decimal("0.8")


def test_unknown_operation():
    with pytest.raises(OperationError, match="Unknown operation"):
        Calculation(operation="Unknown", operand1=Decimal("5"), operand2=Decimal("3"))


def test_to_dict():
    calc = Calculation(operation="Addition", operand1=Decimal("2"), operand2=Decimal("3"))
    result_dict = calc.to_dict()
    assert result_dict == {
        "operation": "Addition",
        "operand1": "2",
        "operand2": "3",
        "result": "5",
        "timestamp": calc.timestamp.isoformat()
    }


def test_from_dict():
    data = {
        "operation": "Addition",
        "operand1": "2",
        "operand2": "3",
        "result": "5",
        "timestamp": datetime.now().isoformat()
    }
    calc = Calculation.from_dict(data)
    assert calc.operation == "Addition"
    assert calc.operand1 == Decimal("2")
    assert calc.operand2 == Decimal("3")
    assert calc.result == Decimal("5")


def test_invalid_from_dict():
    data = {
        "operation": "Addition",
        "operand1": "invalid",
        "operand2": "3",
        "result": "5",
        "timestamp": datetime.now().isoformat()
    }
    with pytest.raises(OperationError, match="Invalid calculation data"):
        Calculation.from_dict(data)


def test_format_result():
    calc = Calculation(operation="Division", operand1=Decimal("1"), operand2=Decimal("3"))
    assert calc.format_result(precision=2) == "0.33"
    assert calc.format_result(precision=10) == "0.3333333333"


def test_equality():
    calc1 = Calculation(operation="Addition", operand1=Decimal("2"), operand2=Decimal("3"))
    calc2 = Calculation(operation="Addition", operand1=Decimal("2"), operand2=Decimal("3"))
    calc3 = Calculation(operation="Subtraction", operand1=Decimal("5"), operand2=Decimal("3"))
    assert calc1 == calc2
    assert calc1 != calc3


# New Test to Cover Logging Warning
def test_from_dict_result_mismatch(caplog):
    """
    Test the from_dict method to ensure it logs a warning when the saved result
    does not match the computed result.
    """
    # Arrange
    data = {
        "operation": "Addition",
        "operand1": "2",
        "operand2": "3",
        "result": "10",  # Incorrect result to trigger logging.warning
        "timestamp": datetime.now().isoformat()
    }

    # Act
    with caplog.at_level(logging.WARNING):
        calc = Calculation.from_dict(data)

    # Assert
    assert "Loaded calculation result 10 differs from computed result 5" in caplog.text  
    
