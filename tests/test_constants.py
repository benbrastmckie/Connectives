"""
Tests for constants module helper functions.

This module tests the helper functions in src/constants.py for
retrieving and looking up predefined connectives.
"""

import pytest
from src.constants import (
    get_binary_by_value,
    get_connective_by_name,
    ALL_BINARY,
    AND, OR, NOT, NAND, NOR, XOR, IFF, IMPLIES,
    PROJECT_X, PROJECT_Y, CONST_FALSE_BIN, CONST_TRUE_BIN,
    CONST_FALSE, CONST_TRUE, IDENTITY, NEGATION
)


class TestGetBinaryByValue:
    """Test get_binary_by_value() function."""

    def test_valid_values(self):
        """Test retrieval of binary connectives by valid values."""
        # Test a few key values
        c0 = get_binary_by_value(0)
        assert c0.arity == 2
        assert c0.truth_table_int == 0

        c8 = get_binary_by_value(8)
        assert c8.arity == 2
        assert c8.truth_table_int == 8
        assert c8.name == "AND"

        c15 = get_binary_by_value(15)
        assert c15.arity == 2
        assert c15.truth_table_int == 15

    def test_all_valid_values(self):
        """Test that all values 0-15 return valid connectives."""
        for i in range(16):
            c = get_binary_by_value(i)
            assert c.arity == 2
            assert c.truth_table_int == i

    def test_invalid_negative_value(self):
        """Test that negative values raise ValueError."""
        with pytest.raises(ValueError, match="Binary connective value must be 0-15"):
            get_binary_by_value(-1)

    def test_invalid_large_value(self):
        """Test that values > 15 raise ValueError."""
        with pytest.raises(ValueError, match="Binary connective value must be 0-15"):
            get_binary_by_value(16)

        with pytest.raises(ValueError, match="Binary connective value must be 0-15"):
            get_binary_by_value(100)

    def test_boundary_values(self):
        """Test boundary values 0 and 15."""
        c_min = get_binary_by_value(0)
        assert c_min.truth_table_int == 0

        c_max = get_binary_by_value(15)
        assert c_max.truth_table_int == 15


class TestGetConnectiveByName:
    """Test get_connective_by_name() function."""

    def test_arity_0_names(self):
        """Test retrieval of arity-0 (constant) connectives."""
        false = get_connective_by_name('FALSE')
        assert false.arity == 0
        assert false == CONST_FALSE

        true = get_connective_by_name('TRUE')
        assert true.arity == 0
        assert true == CONST_TRUE

    def test_arity_1_names(self):
        """Test retrieval of arity-1 (unary) connectives."""
        identity = get_connective_by_name('ID')
        assert identity.arity == 1
        assert identity == IDENTITY

        negation = get_connective_by_name('NOT')
        assert negation.arity == 1
        assert negation == NOT

        # Test alias
        negation2 = get_connective_by_name('NEGATION')
        assert negation2 == NOT

    def test_arity_2_names(self):
        """Test retrieval of arity-2 (binary) connectives."""
        and_conn = get_connective_by_name('AND')
        assert and_conn.arity == 2
        assert and_conn == AND

        or_conn = get_connective_by_name('OR')
        assert or_conn.arity == 2
        assert or_conn == OR

        xor_conn = get_connective_by_name('XOR')
        assert xor_conn.arity == 2
        assert xor_conn == XOR

    def test_negated_operations(self):
        """Test retrieval of negated operations."""
        nand = get_connective_by_name('NAND')
        assert nand == NAND

        nor = get_connective_by_name('NOR')
        assert nor == NOR

        xnor = get_connective_by_name('XNOR')
        assert xnor.arity == 2

    def test_implication_names(self):
        """Test retrieval of implication connectives."""
        implies = get_connective_by_name('IMPLIES')
        assert implies == IMPLIES

        # Test alias
        imp = get_connective_by_name('IMP')
        assert imp == IMPLIES

    def test_equivalence_names(self):
        """Test retrieval of equivalence connectives."""
        iff = get_connective_by_name('IFF')
        assert iff == IFF

    def test_projection_names(self):
        """Test retrieval of projection connectives."""
        proj_x = get_connective_by_name('PROJ_X')
        assert proj_x == PROJECT_X

        proj_y = get_connective_by_name('PROJ_Y')
        assert proj_y == PROJECT_Y

    def test_case_insensitivity(self):
        """Test that name lookup is case-insensitive."""
        and_upper = get_connective_by_name('AND')
        and_lower = get_connective_by_name('and')
        and_mixed = get_connective_by_name('AnD')

        assert and_upper == and_lower == and_mixed == AND

    def test_invalid_name(self):
        """Test that unknown names raise ValueError."""
        with pytest.raises(ValueError, match="Unknown connective name"):
            get_connective_by_name('INVALID')

        with pytest.raises(ValueError, match="Unknown connective name"):
            get_connective_by_name('FOOBAR')

    def test_not_x_not_y(self):
        """Test retrieval of NOT_X and NOT_Y connectives."""
        not_x = get_connective_by_name('NOT_X')
        not_y = get_connective_by_name('NOT_Y')

        assert not_x.arity == 2
        assert not_y.arity == 2

    def test_inhibit_connectives(self):
        """Test retrieval of inhibit connectives."""
        inhibit = get_connective_by_name('INHIBIT')
        conv_inhibit = get_connective_by_name('CONV_INHIBIT')

        assert inhibit.arity == 2
        assert conv_inhibit.arity == 2


class TestALLBINARY:
    """Test ALL_BINARY collection."""

    def test_collection_size(self):
        """Test that ALL_BINARY contains exactly 16 connectives."""
        assert len(ALL_BINARY) == 16

    def test_all_binary_arity(self):
        """Test that all connectives in ALL_BINARY have arity 2."""
        for c in ALL_BINARY:
            assert c.arity == 2

    def test_all_binary_unique(self):
        """Test that all connectives in ALL_BINARY are unique."""
        truth_tables = [c.truth_table_int for c in ALL_BINARY]
        assert len(truth_tables) == len(set(truth_tables))

    def test_all_binary_ordered(self):
        """Test that ALL_BINARY is ordered by truth table value."""
        for i, c in enumerate(ALL_BINARY):
            assert c.truth_table_int == i

    def test_all_binary_completeness(self):
        """Test that ALL_BINARY covers all possible binary functions."""
        truth_table_values = {c.truth_table_int for c in ALL_BINARY}
        expected_values = set(range(16))
        assert truth_table_values == expected_values

    def test_specific_connectives_present(self):
        """Test that specific well-known connectives are in ALL_BINARY."""
        # Extract connectives by value
        by_value = {c.truth_table_int: c for c in ALL_BINARY}

        # Check specific connectives
        assert by_value[0b1000] == AND
        assert by_value[0b1110] == OR
        assert by_value[0b0110] == XOR
        assert by_value[0b0111] == NAND
        assert by_value[0b0001] == NOR
