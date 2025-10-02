"""
Tests for Post's lattice implementation.
"""

import pytest
from src.connectives import Connective
from src.constants import (
    AND, OR, NOT, NAND, NOR, XOR, IFF,
    PROJECT_X, PROJECT_Y, CONST_FALSE_BIN, CONST_TRUE_BIN
)
from src.post_classes import (
    is_t0_preserving, is_t1_preserving, is_monotone,
    is_self_dual, is_affine, get_post_class_membership,
    is_complete, get_missing_classes, filter_by_post_classes
)


class TestT0Preserving:
    """Test T0 (0-preserving) membership checking."""

    def test_and_is_t0(self):
        """Test that AND is 0-preserving."""
        assert is_t0_preserving(AND)
        # AND(0,0) = 0

    def test_or_is_t0(self):
        """Test that OR is 0-preserving."""
        assert is_t0_preserving(OR)
        # OR(0,0) = 0

    def test_nor_is_not_t0(self):
        """Test that NOR is not 0-preserving."""
        assert not is_t0_preserving(NOR)
        # NOR(0,0) = 1

    def test_const_true_is_not_t0(self):
        """Test that constant TRUE is not 0-preserving."""
        assert not is_t0_preserving(CONST_TRUE_BIN)

    def test_const_false_is_t0(self):
        """Test that constant FALSE is 0-preserving."""
        assert is_t0_preserving(CONST_FALSE_BIN)

    def test_not_is_not_t0(self):
        """Test that NOT is not 0-preserving."""
        # NOT(0) = 1, so NOT is NOT 0-preserving
        assert not is_t0_preserving(NOT)


class TestT1Preserving:
    """Test T1 (1-preserving) membership checking."""

    def test_and_is_t1(self):
        """Test that AND is 1-preserving."""
        assert is_t1_preserving(AND)
        # AND(1,1) = 1

    def test_or_is_t1(self):
        """Test that OR is 1-preserving."""
        assert is_t1_preserving(OR)
        # OR(1,1) = 1

    def test_nand_is_not_t1(self):
        """Test that NAND is not 1-preserving."""
        assert not is_t1_preserving(NAND)
        # NAND(1,1) = 0

    def test_const_true_is_t1(self):
        """Test that constant TRUE is 1-preserving."""
        assert is_t1_preserving(CONST_TRUE_BIN)

    def test_const_false_is_not_t1(self):
        """Test that constant FALSE is not 1-preserving."""
        assert not is_t1_preserving(CONST_FALSE_BIN)

    def test_not_is_not_t1(self):
        """Test that NOT is not 1-preserving."""
        assert not is_t1_preserving(NOT)
        # NOT(1) = 0


class TestMonotone:
    """Test monotone membership checking."""

    def test_and_is_monotone(self):
        """Test that AND is monotone."""
        assert is_monotone(AND)

    def test_or_is_monotone(self):
        """Test that OR is monotone."""
        assert is_monotone(OR)

    def test_not_is_not_monotone(self):
        """Test that NOT is not monotone."""
        assert not is_monotone(NOT)
        # NOT(0) = 1, NOT(1) = 0, so 0 ≤ 1 but NOT(0) > NOT(1)

    def test_xor_is_not_monotone(self):
        """Test that XOR is not monotone."""
        assert not is_monotone(XOR)
        # XOR(0,1) = 1, XOR(1,1) = 0, so (0,1) ≤ (1,1) but XOR(0,1) > XOR(1,1)

    def test_project_x_is_monotone(self):
        """Test that projection is monotone."""
        assert is_monotone(PROJECT_X)

    def test_const_true_is_monotone(self):
        """Test that constant TRUE is monotone."""
        assert is_monotone(CONST_TRUE_BIN)

    def test_const_false_is_monotone(self):
        """Test that constant FALSE is monotone."""
        assert is_monotone(CONST_FALSE_BIN)


class TestSelfDual:
    """Test self-dual membership checking."""

    def test_not_is_self_dual(self):
        """Test that NOT is self-dual."""
        # NOT(x) = ¬x, and ¬NOT(x) = ¬¬x = x = NOT(¬x)
        assert is_self_dual(NOT)

    def test_and_is_not_self_dual(self):
        """Test that AND is not self-dual."""
        assert not is_self_dual(AND)

    def test_or_is_not_self_dual(self):
        """Test that OR is not self-dual."""
        assert not is_self_dual(OR)

    def test_xor_is_not_self_dual(self):
        """Test that XOR is not self-dual."""
        # XOR(0,0) = 0, so ¬XOR(0,0) = 1
        # XOR(¬0, ¬0) = XOR(1,1) = 0
        # So NOT self-dual
        assert not is_self_dual(XOR)

    def test_iff_is_not_self_dual(self):
        """Test that IFF is not self-dual."""
        # IFF(0,0) = 1, ¬IFF(0,0) = 0
        # IFF(1,1) = 1
        assert not is_self_dual(IFF)


class TestAffine:
    """Test affine membership checking."""

    def test_xor_is_affine(self):
        """Test that XOR is affine."""
        # XOR is the canonical affine function
        assert is_affine(XOR)

    def test_not_is_affine(self):
        """Test that NOT is affine."""
        # NOT(x) = 1 ⊕ x
        assert is_affine(NOT)

    def test_const_true_is_affine(self):
        """Test that constant TRUE is affine."""
        # f(x,y) = 1 (constant)
        assert is_affine(CONST_TRUE_BIN)

    def test_const_false_is_affine(self):
        """Test that constant FALSE is affine."""
        # f(x,y) = 0 (constant)
        assert is_affine(CONST_FALSE_BIN)

    def test_project_x_is_affine(self):
        """Test that projection is affine."""
        # f(x,y) = x
        assert is_affine(PROJECT_X)

    def test_project_y_is_affine(self):
        """Test that projection is affine."""
        # f(x,y) = y
        assert is_affine(PROJECT_Y)

    def test_and_is_not_affine(self):
        """Test that AND is not affine."""
        # AND is nonlinear
        assert not is_affine(AND)

    def test_or_is_not_affine(self):
        """Test that OR is not affine."""
        # OR is nonlinear
        assert not is_affine(OR)

    def test_iff_is_affine(self):
        """Test that IFF (XNOR) is affine."""
        # IFF(x,y) = 1 ⊕ x ⊕ y
        assert is_affine(IFF)


class TestPostClassMembership:
    """Test get_post_class_membership function."""

    def test_and_classes(self):
        """Test AND's Post class membership."""
        classes = get_post_class_membership(AND)
        # AND is in T0, T1, M (not D, not A)
        assert 'T0' in classes
        assert 'T1' in classes
        assert 'M' in classes
        assert 'D' not in classes
        assert 'A' not in classes

    def test_or_classes(self):
        """Test OR's Post class membership."""
        classes = get_post_class_membership(OR)
        # OR is in T0, T1, M (not D, not A)
        assert 'T0' in classes
        assert 'T1' in classes
        assert 'M' in classes

    def test_xor_classes(self):
        """Test XOR's Post class membership."""
        classes = get_post_class_membership(XOR)
        # XOR is in T0, A (not T1, not M, not D)
        assert 'T0' in classes
        assert 'A' in classes
        assert 'T1' not in classes
        assert 'M' not in classes
        assert 'D' not in classes

    def test_not_classes(self):
        """Test NOT's Post class membership."""
        classes = get_post_class_membership(NOT)
        # NOT is in D, A (not T0, not T1, not M)
        assert 'D' in classes
        assert 'A' in classes
        assert 'T0' not in classes
        assert 'T1' not in classes
        assert 'M' not in classes


class TestCompleteness:
    """Test completeness checking."""

    def test_empty_set_not_complete(self):
        """Test that empty set is not complete."""
        assert not is_complete([])

    def test_single_and_not_complete(self):
        """Test that {AND} is not complete."""
        assert not is_complete([AND])

    def test_and_or_not_complete(self):
        """Test that {AND, OR} is not complete."""
        # Both in T0, T1, M - doesn't escape these classes
        assert not is_complete([AND, OR])

    def test_not_and_complete(self):
        """Test that {NOT, AND} is complete."""
        # This is a known complete set
        assert is_complete([NOT, AND])

    def test_not_and_or_complete(self):
        """Test that {NOT, AND, OR} is complete."""
        assert is_complete([NOT, AND, OR])

    def test_nand_alone_complete(self):
        """Test that {NAND} is complete."""
        # NAND is functionally complete by itself
        assert is_complete([NAND])

    def test_nor_alone_complete(self):
        """Test that {NOR} is complete."""
        # NOR is functionally complete by itself
        assert is_complete([NOR])

    def test_not_xor_not_complete(self):
        """Test that {NOT, XOR} is not complete."""
        # Both are affine, so cannot escape A
        assert not is_complete([NOT, XOR])


class TestMissingClasses:
    """Test get_missing_classes function."""

    def test_empty_set_missing_all(self):
        """Test that empty set is missing all classes."""
        missing = get_missing_classes([])
        assert missing == {'T0', 'T1', 'M', 'D', 'A'}

    def test_and_or_missing_classes(self):
        """Test missing classes for {AND, OR}."""
        missing = get_missing_classes([AND, OR])
        # Both in T0, T1, M
        assert 'T0' in missing
        assert 'T1' in missing
        assert 'M' in missing
        # At least one not in D, A
        assert 'D' not in missing
        assert 'A' not in missing

    def test_complete_set_missing_none(self):
        """Test that complete set has no missing classes."""
        missing = get_missing_classes([NOT, AND])
        assert len(missing) == 0

    def test_affine_set_missing_a(self):
        """Test that affine-only set is missing A."""
        missing = get_missing_classes([NOT, XOR, PROJECT_X])
        assert 'A' in missing


class TestFilterByPostClasses:
    """Test filter_by_post_classes function."""

    def test_filter_escapes_t0(self):
        """Test filtering for connectives that escape T0."""
        from src.connectives import generate_all_connectives

        binaries = generate_all_connectives(2)
        filtered = filter_by_post_classes(binaries, {'T0'})

        # Filtered should only contain functions where f(0,0) = 1
        for c in filtered:
            assert not is_t0_preserving(c)

    def test_filter_escapes_multiple(self):
        """Test filtering for connectives that escape multiple classes."""
        from src.connectives import generate_all_connectives

        binaries = generate_all_connectives(2)
        filtered = filter_by_post_classes(binaries, {'T0', 'T1'})

        # Filtered should escape both T0 and T1
        for c in filtered:
            assert not is_t0_preserving(c)
            assert not is_t1_preserving(c)

    def test_filter_empty_requirements(self):
        """Test filtering with no requirements returns all."""
        from src.connectives import generate_all_connectives

        binaries = generate_all_connectives(2)
        filtered = filter_by_post_classes(binaries, set())

        # No requirements, so all should pass
        assert len(filtered) == len(binaries)


class TestKnownResults:
    """Test against known theoretical results."""

    def test_sheffer_stroke_complete(self):
        """Test that Sheffer stroke (NAND) is complete alone."""
        assert is_complete([NAND])

    def test_peirce_arrow_complete(self):
        """Test that Peirce arrow (NOR) is complete alone."""
        assert is_complete([NOR])

    def test_standard_basis_complete(self):
        """Test that {NOT, AND, OR} is complete."""
        assert is_complete([NOT, AND, OR])

    def test_minimal_basis_complete(self):
        """Test that {NOT, AND} is complete."""
        assert is_complete([NOT, AND])

    def test_affine_not_complete(self):
        """Test that purely affine sets are incomplete."""
        # Any subset of affine functions cannot escape A
        assert not is_complete([XOR, NOT])
        assert not is_complete([PROJECT_X, PROJECT_Y])
        assert not is_complete([CONST_TRUE_BIN, XOR, NOT])
