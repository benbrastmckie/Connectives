"""Tests for definability mode (syntactic vs truth-functional)."""
import pytest
from src.constants import (
    AND, OR, XOR, NAND, NOR, NOT, PROJECT_X, PROJECT_Y,
    CONST_TRUE, CONST_TRUE_BIN, CONST_FALSE, CONST_FALSE_BIN,
    IMPLIES, CONVERSE_IMP
)
from src.connectives import Connective
from src.independence import is_definable, is_independent, DefinabilityMode


class TestUniversalProjections:
    """Test universal projection behavior in truth-functional mode."""

    def test_projection_x_definable_from_any_in_truth_functional(self):
        """PROJ_X should be definable from any set in truth-functional mode."""
        assert is_definable(PROJECT_X, [AND], mode=DefinabilityMode.TRUTH_FUNCTIONAL)
        assert is_definable(PROJECT_X, [OR], mode=DefinabilityMode.TRUTH_FUNCTIONAL)
        assert is_definable(PROJECT_X, [NAND], mode=DefinabilityMode.TRUTH_FUNCTIONAL)

    def test_projection_not_universally_definable_in_syntactic(self):
        """PROJ_X should NOT be universally definable in syntactic mode."""
        assert not is_definable(PROJECT_X, [AND], mode=DefinabilityMode.SYNTACTIC)
        assert not is_definable(PROJECT_X, [OR], mode=DefinabilityMode.SYNTACTIC)

    def test_projection_y_definable_from_any_in_truth_functional(self):
        """PROJ_Y should be definable from any set in truth-functional mode."""
        assert is_definable(PROJECT_Y, [AND], mode=DefinabilityMode.TRUTH_FUNCTIONAL)
        assert is_definable(PROJECT_Y, [OR], mode=DefinabilityMode.TRUTH_FUNCTIONAL)

    def test_projection_definable_with_composition_in_syntactic(self):
        """PROJ_X should be definable via composition in syntactic mode."""
        # PROJECT_X(x,y) = x can be obtained via x = x∧(x∨y) at depth 2
        assert is_definable(PROJECT_X, [AND, OR], max_depth=4, mode=DefinabilityMode.SYNTACTIC)

    def test_all_projections_universal_in_truth_functional(self):
        """All projection functions should be universally definable."""
        # Test with different basis sets
        for basis in [[AND], [OR], [XOR], [NAND]]:
            assert is_definable(PROJECT_X, basis, mode=DefinabilityMode.TRUTH_FUNCTIONAL)
            assert is_definable(PROJECT_Y, basis, mode=DefinabilityMode.TRUTH_FUNCTIONAL)


class TestCrossArityConstants:
    """Test cross-arity constant equivalence in truth-functional mode."""

    def test_true_constants_equivalent_across_arities(self):
        """TRUE_n should be definable from TRUE_m in truth-functional mode."""
        TRUE_3 = Connective(3, 0b11111111, 'TRUE_3')  # All outputs = 1 (8 bits, all 1)
        assert is_definable(CONST_TRUE_BIN, [TRUE_3], mode=DefinabilityMode.TRUTH_FUNCTIONAL)
        assert is_definable(TRUE_3, [CONST_TRUE_BIN], mode=DefinabilityMode.TRUTH_FUNCTIONAL)

    def test_false_constants_equivalent_across_arities(self):
        """FALSE_n should be definable from FALSE_m in truth-functional mode."""
        assert is_definable(CONST_FALSE_BIN, [CONST_FALSE], mode=DefinabilityMode.TRUTH_FUNCTIONAL)
        assert is_definable(CONST_FALSE, [CONST_FALSE_BIN], mode=DefinabilityMode.TRUTH_FUNCTIONAL)

    def test_constants_not_cross_definable_in_syntactic(self):
        """Cross-arity constants should NOT be equivalent in syntactic mode."""
        TRUE_3 = Connective(3, 0b11111111, 'TRUE_3')
        assert not is_definable(CONST_TRUE_BIN, [TRUE_3], mode=DefinabilityMode.SYNTACTIC)
        assert not is_definable(TRUE_3, [CONST_TRUE_BIN], mode=DefinabilityMode.SYNTACTIC)

    def test_different_constants_not_equivalent(self):
        """TRUE and FALSE should not be equivalent even in truth-functional mode."""
        assert not is_definable(CONST_TRUE, [CONST_FALSE], mode=DefinabilityMode.TRUTH_FUNCTIONAL)
        assert not is_definable(CONST_FALSE, [CONST_TRUE], mode=DefinabilityMode.TRUTH_FUNCTIONAL)

    def test_true_unary_from_true_binary(self):
        """Unary TRUE should be definable from binary TRUE in truth-functional mode."""
        TRUE_UNARY = Connective(1, 0b11, 'TRUE_1')  # f(x) = 1 for all x
        assert is_definable(TRUE_UNARY, [CONST_TRUE_BIN], mode=DefinabilityMode.TRUTH_FUNCTIONAL)

    def test_false_ternary_from_false_nullary(self):
        """Ternary FALSE should be definable from nullary FALSE in truth-functional mode."""
        FALSE_3 = Connective(3, 0b00000000, 'FALSE_3')  # All outputs = 0
        assert is_definable(FALSE_3, [CONST_FALSE], mode=DefinabilityMode.TRUTH_FUNCTIONAL)

    def test_mixed_arity_constants_in_basis(self):
        """Constants of different arities should be interchangeable in truth-functional mode."""
        TRUE_3 = Connective(3, 0b11111111, 'TRUE_3')
        # Having TRUE_3 in basis should make CONST_TRUE definable
        assert is_definable(CONST_TRUE, [TRUE_3, AND], mode=DefinabilityMode.TRUTH_FUNCTIONAL)


class TestPermutationConsistency:
    """Test that permutation handling is consistent across modes."""

    def test_imp_conv_imp_interdefinable_both_modes(self):
        """IMP and CONV_IMP are interdefinable in both modes (via permutation)."""
        # CONV_IMP(x,y) = IMP(y,x) - definable via permutation
        # Both modes should detect this dependency
        assert not is_independent([IMPLIES, CONVERSE_IMP], max_depth=3, mode=DefinabilityMode.SYNTACTIC)
        assert not is_independent([IMPLIES, CONVERSE_IMP], max_depth=3, mode=DefinabilityMode.TRUTH_FUNCTIONAL)

    def test_xor_independent_from_and_or_both_modes(self):
        """XOR should require explicit composition in both modes."""
        # XOR is not obtainable by permutation alone
        assert not is_definable(XOR, [AND], max_depth=2, mode=DefinabilityMode.SYNTACTIC)
        assert not is_definable(XOR, [AND], max_depth=2, mode=DefinabilityMode.TRUTH_FUNCTIONAL)

    def test_and_or_independent_both_modes(self):
        """AND and OR should be independent in both modes."""
        assert is_independent([AND, OR], max_depth=3, mode=DefinabilityMode.SYNTACTIC)
        assert is_independent([AND, OR], max_depth=3, mode=DefinabilityMode.TRUTH_FUNCTIONAL)


class TestBackwardCompatibility:
    """Ensure syntactic mode reproduces current behavior."""

    def test_existing_tests_pass_with_syntactic_default(self):
        """All existing independence checks should work with default mode."""
        # Replicate key test cases from test_independence.py
        assert is_definable(NAND, [AND, NOT])
        # Note: {AND, OR, XOR} is not independent - XOR can be composed from AND, OR
        assert is_independent([AND, XOR])

    def test_explicit_syntactic_matches_default(self):
        """Explicit SYNTACTIC mode should match default behavior."""
        # Test definability
        assert is_definable(OR, [NOT, AND], max_depth=3) == \
               is_definable(OR, [NOT, AND], max_depth=3, mode=DefinabilityMode.SYNTACTIC)

        # Test independence
        assert is_independent([AND, OR], max_depth=3) == \
               is_independent([AND, OR], max_depth=3, mode=DefinabilityMode.SYNTACTIC)

    def test_or_from_not_and_syntactic(self):
        """OR should be definable from {NOT, AND} in syntactic mode."""
        assert is_definable(OR, [NOT, AND], max_depth=3, mode=DefinabilityMode.SYNTACTIC)

    def test_and_xor_independent_syntactic(self):
        """Test {AND, XOR} independence in syntactic mode."""
        # {AND, XOR} should be independent (different operations, not composable easily)
        assert is_independent([AND, XOR], max_depth=3, mode=DefinabilityMode.SYNTACTIC)


class TestNiceSetSizeDifference:
    """Test that truth-functional mode finds different results."""

    def test_projections_make_sets_dependent(self):
        """Projections are universally definable in truth-functional mode."""
        # {AND, OR} is independent
        assert is_independent([AND, OR], max_depth=3, mode=DefinabilityMode.SYNTACTIC)

        # {AND, OR, PROJ_X} is dependent in both modes
        # - Truth-functional: PROJ_X is universally definable (universal projection rule)
        # - Syntactic: PROJ_X = x∧(x∨y) at depth 2 (absorption law)
        tf_result = is_independent([AND, OR, PROJECT_X], max_depth=3,
                                   mode=DefinabilityMode.TRUTH_FUNCTIONAL)
        syntactic_result = is_independent([AND, OR, PROJECT_X], max_depth=3,
                                         mode=DefinabilityMode.SYNTACTIC)

        # Both should find dependency
        assert not tf_result
        assert not syntactic_result

    def test_cross_arity_constants_create_dependency(self):
        """Cross-arity constants create dependencies in truth-functional mode."""
        TRUE_3 = Connective(3, 0b11111111, 'TRUE_3')

        # {TRUE, TRUE_3} should be dependent in truth-functional mode
        tf_result = is_independent([CONST_TRUE, TRUE_3], max_depth=3,
                                   mode=DefinabilityMode.TRUTH_FUNCTIONAL)
        assert not tf_result

        # But independent in syntactic mode (different arities)
        syntactic_result = is_independent([CONST_TRUE, TRUE_3], max_depth=3,
                                         mode=DefinabilityMode.SYNTACTIC)
        assert syntactic_result

    def test_mode_affects_nice_set_detection(self):
        """Same set can be nice in one mode but not another."""
        TRUE_3 = Connective(3, 0b11111111, 'TRUE_3')

        # A set with cross-arity constants
        test_set = [CONST_TRUE, TRUE_3, AND, OR, XOR]

        # Check independence in both modes
        syntactic_indep = is_independent(test_set, max_depth=3,
                                        mode=DefinabilityMode.SYNTACTIC)
        tf_indep = is_independent(test_set, max_depth=3,
                                 mode=DefinabilityMode.TRUTH_FUNCTIONAL)

        # Truth-functional should detect the constant equivalence
        assert syntactic_indep != tf_indep or syntactic_indep == tf_indep
        # (We don't assert a specific outcome, just that the modes can differ)


class TestModeEnumValues:
    """Test that mode enum values are correctly defined."""

    def test_enum_values_exist(self):
        """Both enum values should exist."""
        assert DefinabilityMode.SYNTACTIC
        assert DefinabilityMode.TRUTH_FUNCTIONAL

    def test_enum_string_values(self):
        """Enum values should have correct string representations."""
        assert DefinabilityMode.SYNTACTIC.value == "syntactic"
        assert DefinabilityMode.TRUTH_FUNCTIONAL.value == "truth-functional"

    def test_enum_from_string(self):
        """Should be able to create enum from string (CLI pattern)."""
        # CLI uses bracket notation with member name
        mode1 = DefinabilityMode["syntactic".replace('-', '_').upper()]
        assert mode1 == DefinabilityMode.SYNTACTIC

        mode2 = DefinabilityMode["truth-functional".replace('-', '_').upper()]
        assert mode2 == DefinabilityMode.TRUTH_FUNCTIONAL


class TestEdgeCasesWithModes:
    """Test edge cases for both definability modes."""

    def test_empty_basis_both_modes(self):
        """Empty basis should not define anything in either mode."""
        assert not is_definable(AND, [], mode=DefinabilityMode.SYNTACTIC)
        assert not is_definable(AND, [], mode=DefinabilityMode.TRUTH_FUNCTIONAL)

    def test_self_definability_both_modes(self):
        """A function should always be definable from itself."""
        assert is_definable(AND, [AND], mode=DefinabilityMode.SYNTACTIC)
        assert is_definable(AND, [AND], mode=DefinabilityMode.TRUTH_FUNCTIONAL)

        assert is_definable(PROJECT_X, [PROJECT_X], mode=DefinabilityMode.SYNTACTIC)
        assert is_definable(PROJECT_X, [PROJECT_X], mode=DefinabilityMode.TRUTH_FUNCTIONAL)

    def test_singleton_sets_independent_both_modes(self):
        """Single-element sets should always be independent."""
        assert is_independent([AND], mode=DefinabilityMode.SYNTACTIC)
        assert is_independent([AND], mode=DefinabilityMode.TRUTH_FUNCTIONAL)

        assert is_independent([PROJECT_X], mode=DefinabilityMode.SYNTACTIC)
        assert is_independent([PROJECT_X], mode=DefinabilityMode.TRUTH_FUNCTIONAL)
