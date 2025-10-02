"""
Tests for core connective representation.
"""

import pytest
from src.connectives import Connective, generate_all_connectives, get_connective_count
from src.constants import (
    AND, OR, NOT, NAND, NOR, XOR, IFF, IMPLIES,
    PROJECT_X, PROJECT_Y, CONST_FALSE_BIN, CONST_TRUE_BIN,
    ALL_BINARY, get_binary_by_value
)


class TestConnectiveBasics:
    """Test basic Connective class functionality."""

    def test_arity_validation(self):
        """Test that invalid arities raise ValueError."""
        with pytest.raises(ValueError, match="Arity must be in range 0-5"):
            Connective(-1, 0)

        with pytest.raises(ValueError, match="Arity must be in range 0-5"):
            Connective(6, 0)

    def test_truth_table_validation(self):
        """Test that invalid truth table values raise ValueError."""
        # Arity 2 allows values 0-15 (4 bits)
        with pytest.raises(ValueError, match="Truth table value .* invalid"):
            Connective(2, 16)

        with pytest.raises(ValueError, match="Truth table value .* invalid"):
            Connective(2, -1)

    def test_valid_construction(self):
        """Test that valid connectives can be constructed."""
        c = Connective(2, 8, "AND")
        assert c.arity == 2
        assert c.truth_table_int == 8
        assert c.name == "AND"

    def test_default_name(self):
        """Test that default names are generated."""
        c = Connective(2, 8)
        assert c.name == "f2_8"


class TestEvaluation:
    """Test truth table evaluation."""

    def test_and_evaluation(self):
        """Test AND connective evaluates correctly."""
        # AND: 0b1000 = 8
        # (0,0)→0, (0,1)→0, (1,0)→0, (1,1)→1
        assert AND.evaluate((0, 0)) == 0
        assert AND.evaluate((0, 1)) == 0
        assert AND.evaluate((1, 0)) == 0
        assert AND.evaluate((1, 1)) == 1

    def test_or_evaluation(self):
        """Test OR connective evaluates correctly."""
        # OR: 0b1110 = 14
        # (0,0)→0, (0,1)→1, (1,0)→1, (1,1)→1
        assert OR.evaluate((0, 0)) == 0
        assert OR.evaluate((0, 1)) == 1
        assert OR.evaluate((1, 0)) == 1
        assert OR.evaluate((1, 1)) == 1

    def test_not_evaluation(self):
        """Test NOT connective evaluates correctly."""
        # NOT: 0b01 = 1 (arity 1)
        # (0)→1, (1)→0
        assert NOT.evaluate((0,)) == 1
        assert NOT.evaluate((1,)) == 0

    def test_xor_evaluation(self):
        """Test XOR connective evaluates correctly."""
        # XOR: 0b0110 = 6
        # (0,0)→0, (0,1)→1, (1,0)→1, (1,1)→0
        assert XOR.evaluate((0, 0)) == 0
        assert XOR.evaluate((0, 1)) == 1
        assert XOR.evaluate((1, 0)) == 1
        assert XOR.evaluate((1, 1)) == 0

    def test_wrong_number_of_inputs(self):
        """Test that wrong number of inputs raises ValueError."""
        with pytest.raises(ValueError, match="Expected 2 inputs"):
            AND.evaluate((0,))

        with pytest.raises(ValueError, match="Expected 1 inputs"):
            NOT.evaluate((0, 0))

    def test_invalid_input_values(self):
        """Test that non-binary inputs raise ValueError."""
        with pytest.raises(ValueError, match="Input values must be 0 or 1"):
            AND.evaluate((0, 2))


class TestEvaluateAll:
    """Test complete truth table generation."""

    def test_and_full_table(self):
        """Test AND generates complete truth table."""
        table = AND.evaluate_all()
        expected = [
            ((0, 0), 0),
            ((0, 1), 0),
            ((1, 0), 0),
            ((1, 1), 1),
        ]
        assert table == expected

    def test_not_full_table(self):
        """Test NOT generates complete truth table."""
        table = NOT.evaluate_all()
        expected = [
            ((0,), 1),
            ((1,), 0),
        ]
        assert table == expected

    def test_constant_table(self):
        """Test constant (arity 0) generates correct table."""
        from src.constants import CONST_TRUE
        table = CONST_TRUE.evaluate_all()
        expected = [
            ((), 1),
        ]
        assert table == expected


class TestEquality:
    """Test connective equality and hashing."""

    def test_equal_connectives(self):
        """Test that identical connectives are equal."""
        c1 = Connective(2, 8, "AND_1")
        c2 = Connective(2, 8, "AND_2")
        assert c1 == c2

    def test_unequal_connectives(self):
        """Test that different connectives are not equal."""
        assert AND != OR
        assert AND != NOT  # Different arity

    def test_hash_consistency(self):
        """Test that equal connectives have same hash."""
        c1 = Connective(2, 8, "AND_1")
        c2 = Connective(2, 8, "AND_2")
        assert hash(c1) == hash(c2)

    def test_set_membership(self):
        """Test that connectives work in sets."""
        c1 = Connective(2, 8, "AND_1")
        c2 = Connective(2, 8, "AND_2")
        c3 = Connective(2, 14, "OR")

        s = {c1, c2, c3}
        assert len(s) == 2  # c1 and c2 are the same


class TestStringRepresentation:
    """Test string output."""

    def test_repr(self):
        """Test repr shows arity and name."""
        rep = repr(AND)
        assert "arity=2" in rep
        assert "AND" in rep

    def test_str_includes_truth_table(self):
        """Test str shows formatted truth table."""
        s = str(NOT)
        assert "NOT" in s
        assert "arity 1" in s
        # Should show inputs and outputs
        assert "0" in s
        assert "1" in s


class TestBinaryConnectives:
    """Test all 16 binary connectives."""

    def test_all_binary_count(self):
        """Test that all 16 binary connectives are defined."""
        assert len(ALL_BINARY) == 16

    def test_all_binary_unique(self):
        """Test that all binary connectives are unique."""
        truth_tables = [c.truth_table_int for c in ALL_BINARY]
        assert len(truth_tables) == len(set(truth_tables))

    def test_all_binary_ordered(self):
        """Test that binary connectives are ordered by truth table value."""
        for i, c in enumerate(ALL_BINARY):
            assert c.truth_table_int == i

    def test_get_binary_by_value(self):
        """Test retrieval of binary connectives by value."""
        for i in range(16):
            c = get_binary_by_value(i)
            assert c.truth_table_int == i
            assert c.arity == 2

    def test_get_binary_invalid_value(self):
        """Test that invalid values raise ValueError."""
        with pytest.raises(ValueError):
            get_binary_by_value(16)
        with pytest.raises(ValueError):
            get_binary_by_value(-1)


class TestStandardConnectives:
    """Test specific standard connectives have correct truth tables."""

    def test_and_truth_table(self):
        """Test AND has correct truth table value."""
        assert AND.truth_table_int == 0b1000

    def test_or_truth_table(self):
        """Test OR has correct truth table value."""
        assert OR.truth_table_int == 0b1110

    def test_nand_truth_table(self):
        """Test NAND has correct truth table value."""
        assert NAND.truth_table_int == 0b0111

    def test_nor_truth_table(self):
        """Test NOR has correct truth table value."""
        assert NOR.truth_table_int == 0b0001

    def test_xor_truth_table(self):
        """Test XOR has correct truth table value."""
        assert XOR.truth_table_int == 0b0110

    def test_implies_truth_table(self):
        """Test IMPLIES has correct truth table value."""
        # x → y: F only when x=1, y=0
        # (0,0)→1, (0,1)→1, (1,0)→0, (1,1)→1
        assert IMPLIES.truth_table_int == 0b1011
        assert IMPLIES.evaluate((1, 0)) == 0
        assert IMPLIES.evaluate((0, 0)) == 1
        assert IMPLIES.evaluate((0, 1)) == 1
        assert IMPLIES.evaluate((1, 1)) == 1

    def test_iff_truth_table(self):
        """Test IFF (equivalence) has correct truth table value."""
        # x ↔ y: T when x=y
        # (0,0)→1, (0,1)→0, (1,0)→0, (1,1)→1
        assert IFF.truth_table_int == 0b1001


class TestGeneration:
    """Test connective generation functions."""

    def test_generate_all_binary(self):
        """Test generating all binary connectives."""
        connectives = generate_all_connectives(2)
        assert len(connectives) == 16

        # Check all values present
        values = {c.truth_table_int for c in connectives}
        assert values == set(range(16))

    def test_generate_all_unary(self):
        """Test generating all unary connectives."""
        connectives = generate_all_connectives(1)
        assert len(connectives) == 4

    def test_generate_invalid_arity(self):
        """Test that invalid arity raises ValueError."""
        with pytest.raises(ValueError):
            generate_all_connectives(6)

    def test_get_connective_count(self):
        """Test connective count calculation."""
        assert get_connective_count(0) == 2    # 2^(2^0) = 2
        assert get_connective_count(1) == 4    # 2^(2^1) = 4
        assert get_connective_count(2) == 16   # 2^(2^2) = 16
        assert get_connective_count(3) == 256  # 2^(2^3) = 256


class TestProjections:
    """Test projection connectives."""

    def test_project_x(self):
        """Test x projection returns first input."""
        assert PROJECT_X.evaluate((0, 0)) == 0
        assert PROJECT_X.evaluate((0, 1)) == 0
        assert PROJECT_X.evaluate((1, 0)) == 1
        assert PROJECT_X.evaluate((1, 1)) == 1

    def test_project_y(self):
        """Test y projection returns second input."""
        assert PROJECT_Y.evaluate((0, 0)) == 0
        assert PROJECT_Y.evaluate((0, 1)) == 1
        assert PROJECT_Y.evaluate((1, 0)) == 0
        assert PROJECT_Y.evaluate((1, 1)) == 1


class TestConstants:
    """Test constant connectives."""

    def test_binary_constants(self):
        """Test binary constant functions."""
        # FALSE always returns 0
        for inputs in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            assert CONST_FALSE_BIN.evaluate(inputs) == 0

        # TRUE always returns 1
        for inputs in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            assert CONST_TRUE_BIN.evaluate(inputs) == 1
