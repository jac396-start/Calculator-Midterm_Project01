import pytest
from decimal import Decimal
from typing import Any, Dict, Type

from app.exceptions import ValidationError
from app.operations import (
    Operation,
    Addition,
    Subtraction,
    Multiplication,
    Division,
    Power,
    Root,
    Modulus,
    IntegerDivision,
    Percentage,
    AbsoluteDifference,
    OperationFactory,
)


class TestOperation:
    def test_str_representation(self):
        class TestOp(Operation):
            def execute(self, a: Decimal, b: Decimal) -> Decimal:
                return a

        assert str(TestOp()) == "TestOp"


class BaseOperationTest:

    operation_class: Type[Operation]
    valid_test_cases: Dict[str, Dict[str, Any]]
    invalid_test_cases: Dict[str, Dict[str, Any]]

    def test_valid_operations(self):
        operation = self.operation_class()
        for name, case in self.valid_test_cases.items():
            a = Decimal(str(case["a"]))
            b = Decimal(str(case["b"]))
            expected = Decimal(str(case["expected"]))
            result = operation.execute(a, b)
            assert result == expected, f"Failed case: {name}"

    def test_invalid_operations(self):
        operation = self.operation_class()
        for name, case in self.invalid_test_cases.items():
            a = Decimal(str(case["a"]))
            b = Decimal(str(case["b"]))
            error = case.get("error", ValidationError)
            error_message = case.get("message", "")

            with pytest.raises(error, match=error_message):
                operation.execute(a, b)


class TestAddition(BaseOperationTest):

    operation_class = Addition
    valid_test_cases = {
        "positive_numbers": {"a": "5", "b": "3", "expected": "8"},
        "negative_numbers": {"a": "-5", "b": "-3", "expected": "-8"},
        "mixed_signs": {"a": "-5", "b": "3", "expected": "-2"},
        "zero_sum": {"a": "5", "b": "-5", "expected": "0"},
        "decimals": {"a": "5.5", "b": "3.3", "expected": "8.8"},
        "large_numbers": {
            "a": "1e10",
            "b": "1e10",
            "expected": "20000000000"
        },
    }
    invalid_test_cases = {}  # Addition has no invalid cases


class TestSubtraction(BaseOperationTest):

    operation_class = Subtraction
    valid_test_cases = {
        "positive_numbers": {"a": "5", "b": "3", "expected": "2"},
        "negative_numbers": {"a": "-5", "b": "-3", "expected": "-2"},
        "mixed_signs": {"a": "-5", "b": "3", "expected": "-8"},
        "zero_result": {"a": "5", "b": "5", "expected": "0"},
        "decimals": {"a": "5.5", "b": "3.3", "expected": "2.2"},
        "large_numbers": {
            "a": "1e10",
            "b": "1e9",
            "expected": "9000000000"
        },
    }
    invalid_test_cases = {}  # Subtraction has no invalid cases


class TestMultiplication(BaseOperationTest):

    operation_class = Multiplication
    valid_test_cases = {
        "positive_numbers": {"a": "5", "b": "3", "expected": "15"},
        "negative_numbers": {"a": "-5", "b": "-3", "expected": "15"},
        "mixed_signs": {"a": "-5", "b": "3", "expected": "-15"},
        "multiply_by_zero": {"a": "5", "b": "0", "expected": "0"},
        "decimals": {"a": "5.5", "b": "3.3", "expected": "18.15"},
        "large_numbers": {
            "a": "1e5",
            "b": "1e5",
            "expected": "10000000000"
        },
    }
    invalid_test_cases = {}  # Multiplication has no invalid cases


class TestDivision(BaseOperationTest):

    operation_class = Division
    valid_test_cases = {
        "positive_numbers": {"a": "6", "b": "2", "expected": "3"},
        "negative_numbers": {"a": "-6", "b": "-2", "expected": "3"},
        "mixed_signs": {"a": "-6", "b": "2", "expected": "-3"},
        "decimals": {"a": "5.5", "b": "2", "expected": "2.75"},
        "divide_zero": {"a": "0", "b": "5", "expected": "0"},
    }
    invalid_test_cases = {
        "divide_by_zero": {
            "a": "5",
            "b": "0",
            "error": ValidationError,
            "message": "Division by zero is not allowed"
        },
    }


class TestPower(BaseOperationTest):

    operation_class = Power
    valid_test_cases = {
        "positive_base_and_exponent": {"a": "2", "b": "3", "expected": "8"},
        "zero_exponent": {"a": "5", "b": "0", "expected": "1"},
        "one_exponent": {"a": "5", "b": "1", "expected": "5"},
        "decimal_base": {"a": "2.5", "b": "2", "expected": "6.25"},
        "zero_base": {"a": "0", "b": "5", "expected": "0"},
    }
    invalid_test_cases = {
        "negative_exponent": {
            "a": "2",
            "b": "-3",
            "error": ValidationError,
            "message": "Negative exponents not supported"
        },
    }


class TestRoot(BaseOperationTest):

    operation_class = Root
    valid_test_cases = {
        "square_root": {"a": "9", "b": "2", "expected": "3"},
        "cube_root": {"a": "27", "b": "3", "expected": "3"},
        "fourth_root": {"a": "16", "b": "4", "expected": "2"},
        "decimal_root": {"a": "2.25", "b": "2", "expected": "1.5"},
    }
    invalid_test_cases = {
        "negative_base": {
            "a": "-9",
            "b": "2",
            "error": ValidationError,
            "message": "Cannot calculate root of negative number"
        },
        "zero_root": {
            "a": "9",
            "b": "0",
            "error": ValidationError,
            "message": "Zero root is undefined"
        },
    }


class TestModulus(BaseOperationTest):

    operation_class = Modulus

    # Valid test cases for remainder calculation
    valid_test_cases = {
        # 10 divided by 3 is 3 remainder 1
        "standard_positive": {"a": "10", "b": "3", "expected": "1"},
        # 10 divided by -3 is -4 remainder -2 (Python's behavior: sign of divisor)
        "negative_divisor": {"a": "10", "b": "-3", "expected": "-2"},
        # -10 divided by 3 is -4 remainder 2
        "negative_dividend": {"a": "-10", "b": "3", "expected": "2"},
        # 5.5 divided by 2.0 is 2 remainder 1.5
        "decimal_operands": {"a": "5.5", "b": "2", "expected": "1.5"},
        # 10 divided by 10 is 1 remainder 0
        "zero_remainder": {"a": "10", "b": "10", "expected": "0"},
    }

    # Invalid test case for division by zero
    invalid_test_cases = {
        "zero_divisor": {
            "a": "10",
            "b": "0",
            "error": ValidationError,
            "message": "Cannot divide by zero" # Match the expected error message from your core logic
        },
    }


class TestIntegerDivision(BaseOperationTest):
    """Tests for the Integer Division operation."""

    operation_class = IntegerDivision

    # Valid test cases for integer quotient calculation
    valid_test_cases = {
        # 10 // 3 = 3
        "standard_positive": {"a": "10", "b": "3", "expected": "3"},
        # -10 // 3 = -4 (Python floors the result)
        "negative_dividend": {"a": "-10", "b": "3", "expected": "-4"},
        # 10 // -3 = -4
        "negative_divisor": {"a": "10", "b": "-3", "expected": "-4"},
        # 7.8 // 2.5 = 3
        "decimal_operands": {"a": "7.8", "b": "2.5", "expected": "3"},
        # Result should discard the fractional part (4.5 // 2.0 = 2)
        "half_result": {"a": "4.5", "b": "2", "expected": "2"},
    }

    # Invalid test case for division by zero
    invalid_test_cases = {
        "zero_divisor": {
            "a": "10",
            "b": "0",
            "error": ValidationError,
            "message": "Cannot divide by zero"
        },
    }


class TestPercentage(BaseOperationTest):
    """Tests for the Percentage operation (a is what percent of b)."""

    operation_class = Percentage

    # Valid test cases
    valid_test_cases = {
        # 50 is 50% of 100
        "standard_fifty_percent": {"a": "50", "b": "100", "expected": "50"},
        # 25 is 200% of 12.5
        "over_one_hundred_percent": {"a": "25", "b": "12.5", "expected": "200"},
        # 1 is 10% of 10
        "standard_ten_percent": {"a": "1", "b": "10", "expected": "10"},
        # 10 is 1000% of 1
        "large_percentage": {"a": "10", "b": "1", "expected": "1000"},
        # Precision check: 1/3 * 100
        "with_precision": {"a": "1", "b": "3", "expected": "33.33333333333333333333333333"},
    }

    # Invalid test case for division by zero
    invalid_test_cases = {
        "zero_divisor": {
            "a": "10",
            "b": "0",
            "error": ValidationError,
            "message": "Cannot divide by zero"
        },
    }


class TestAbsoluteDifference(BaseOperationTest):
    """Tests for the Absolute Difference operation (|a - b|)."""

    operation_class = AbsoluteDifference

    # Valid test cases
    valid_test_cases = {
        # |10 - 5| = 5
        "standard_positive": {"a": "10", "b": "5", "expected": "5"},
        # |5 - 10| = 5
        "standard_reverse": {"a": "5", "b": "10", "expected": "5"},
        # | -10 - (-5) | = |-5| = 5
        "negative_numbers": {"a": "-10", "b": "-5", "expected": "5"},
        # | 10 - (-5) | = |15| = 15
        "mixed_sign": {"a": "10", "b": "-5", "expected": "15"},
        # | 7.5 - 7.5 | = 0
        "zero_difference": {"a": "7.5", "b": "7.5", "expected": "0"},
        # | 4.3 - 5.1 | = 0.8
        "decimal_result": {"a": "4.3", "b": "5.1", "expected": "0.8"},
    }

    # No invalid cases needed, as absolute difference is always defined
    invalid_test_cases = {}


class TestOperationFactory:
    """Test OperationFactory functionality."""

    def test_create_valid_operations(self):
        """Test creation of all valid operations."""
        operation_map = {
            'add': Addition,
            'subtract': Subtraction,
            'multiply': Multiplication,
            'divide': Division,
            'power': Power,
            'root': Root,
            'modulus': Modulus,
            'interger_division': Interger_Division,
            'percentage': Percentage,
            'absolute_difference': Absolute_Difference
        }

        for op_name, op_class in operation_map.items():
            operation = OperationFactory.create_operation(op_name)
            assert isinstance(operation, op_class)
            # Test case-insensitive
            operation = OperationFactory.create_operation(op_name.upper())
            assert isinstance(operation, op_class)

    def test_create_invalid_operation(self):
        """Test creation of invalid operation raises error."""
        with pytest.raises(ValueError, match="Unknown operation: invalid_op"):
            OperationFactory.create_operation("invalid_op")

    def test_register_valid_operation(self):
        """Test registering a new valid operation."""
        class NewOperation(Operation):
            def execute(self, a: Decimal, b: Decimal) -> Decimal:
                return a

        OperationFactory.register_operation("new_op", NewOperation)
        operation = OperationFactory.create_operation("new_op")
        assert isinstance(operation, NewOperation)

    def test_register_invalid_operation(self):
        """Test registering an invalid operation class raises error."""
        class InvalidOperation:
            pass

        with pytest.raises(TypeError, match="Operation class must inherit"):
            OperationFactory.register_operation("invalid", InvalidOperation)
               
