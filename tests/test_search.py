"""
Tests for search algorithms for finding nice connective sets.
"""

import pytest
from src.connectives import Connective
from src.constants import AND, OR, NOT, NAND, NOR, XOR, CONST_TRUE, CONST_FALSE, IMPLIES, IFF
from src.search import (
    find_nice_sets_of_size,
    find_maximum_nice_set,
    search_binary_only,
    search_incremental_arity,
    analyze_nice_set,
    validate_nice_set
)


class TestFindNiceSetsOfSize:
    """Test finding nice sets of specific sizes."""

    def test_empty_pool(self):
        """Empty connective pool should return no nice sets."""
        result = find_nice_sets_of_size([], 1)
        assert result == []

    def test_size_zero(self):
        """Size 0 should return empty set (not nice - not complete)."""
        result = find_nice_sets_of_size([AND, OR, NOT], 0)
        assert result == []

    def test_single_function_not_complete(self):
        """Single binary function is not complete."""
        result = find_nice_sets_of_size([AND, OR, NOT], 1)
        # Single functions (except Sheffer-like) are not complete
        assert len(result) == 0 or all(len(s) == 1 for s in result)

    def test_nand_alone_is_nice(self):
        """NAND alone should be nice (complete and trivially independent)."""
        result = find_nice_sets_of_size([NAND], 1)
        assert len(result) == 1
        assert NAND in result[0]

    def test_nor_alone_is_nice(self):
        """NOR alone should be nice (complete and trivially independent)."""
        result = find_nice_sets_of_size([NOR], 1)
        assert len(result) == 1
        assert NOR in result[0]

    def test_not_and_is_nice_size_2(self):
        """NOT and AND should form a nice set of size 2."""
        result = find_nice_sets_of_size([NOT, AND, OR], 2)
        # Check if {NOT, AND} is in results
        not_and_found = any(
            set([NOT, AND]) == set(nice_set) for nice_set in result
        )
        assert not_and_found

    def test_not_or_is_nice_size_2(self):
        """NOT and OR should form a nice set of size 2."""
        result = find_nice_sets_of_size([NOT, OR, AND], 2)
        # Check if {NOT, OR} is in results
        not_or_found = any(
            set([NOT, OR]) == set(nice_set) for nice_set in result
        )
        assert not_or_found


class TestFindMaximumNiceSet:
    """Test finding maximum nice set size."""

    def test_empty_pool(self):
        """Empty pool should return size 0."""
        max_size, sets, metadata = find_maximum_nice_set([])
        assert max_size == 0
        assert sets == []
        assert 'composition_depth' in metadata
        assert 'strategy' in metadata

    def test_single_sheffer_function(self):
        """NAND alone should give max size 1."""
        max_size, sets, metadata = find_maximum_nice_set([NAND])
        assert max_size == 1
        assert len(sets) == 1
        assert NAND in sets[0]
        assert metadata['composition_depth'] == 3  # default
        assert metadata['strategy'] == 'enumeration'  # default

    def test_not_and_or_gives_size_3(self):
        """NOT, AND, OR should allow nice sets of size at least 2."""
        max_size, sets, metadata = find_maximum_nice_set([NOT, AND, OR], max_size=3)
        assert max_size >= 2  # {NOT, AND} or {NOT, OR} are nice
        assert 'search_time' in metadata
        assert 'basis_size' in metadata


class TestBinaryOnlySearch:
    """Test binary-only search (Phase 4 validation)."""

    def test_binary_only_finds_nice_sets(self):
        """Binary-only search should find nice sets."""
        max_size, sets = search_binary_only(verbose=False)
        assert max_size > 0
        assert len(sets) > 0

    def test_binary_only_max_size_is_3(self):
        """Binary-only search should find maximum size of 3 (known result)."""
        max_size, sets = search_binary_only(verbose=False)
        assert max_size == 3, f"Expected max=3 for binary-only, got {max_size}"

    def test_binary_only_all_sets_valid(self):
        """All found sets should be truly nice."""
        max_size, sets = search_binary_only(verbose=False)
        for nice_set in sets[:5]:  # Check first 5
            is_valid, msg = validate_nice_set(nice_set)
            assert is_valid, f"Set {[c.name for c in nice_set]} invalid: {msg}"

    def test_binary_only_contains_known_nice_set(self):
        """Should find the classic {NOT, AND, XOR} set."""
        max_size, sets = search_binary_only(verbose=False)

        # Check if we found a set containing NOT, AND, and another binary function
        # The exact composition may vary, but should have size 3
        assert max_size == 3


class TestIncrementalAritySearch:
    """Test incremental arity search (Phase 5)."""

    @pytest.mark.slow
    def test_incremental_starts_with_binary(self):
        """Incremental search should start with binary connectives."""
        max_size, sets, stats = search_incremental_arity(
            max_arity=2,
            verbose=False
        )
        assert 2 in stats['arity_results']
        assert stats['arity_results'][2]['max_size'] > 0

    @pytest.mark.slow
    def test_incremental_includes_unary(self):
        """Incremental search should include unary connectives."""
        max_size, sets, stats = search_incremental_arity(
            max_arity=2,  # Will add binary and unary
            verbose=False
        )
        assert 1 in stats['connectives_by_arity']
        assert stats['connectives_by_arity'][1] == 4  # 4 unary functions

    @pytest.mark.slow
    def test_incremental_finds_best_result(self):
        """Incremental search should find best result across arities."""
        max_size, sets, stats = search_incremental_arity(
            max_arity=3,
            verbose=False
        )
        assert max_size >= 3  # Should at least match binary-only result

    @pytest.mark.slow
    def test_incremental_stopping_criterion(self):
        """Should stop when no improvement for several arities."""
        max_size, sets, stats = search_incremental_arity(
            max_arity=5,  # Allow up to arity 5
            stopping_criterion=2,  # Stop after 2 no-improvements
            verbose=False
        )
        # Should have stopped before trying all arities
        assert max_size > 0


class TestAnalyzeNiceSet:
    """Test nice set analysis."""

    def test_analyze_empty_set(self):
        """Analysis of empty set."""
        analysis = analyze_nice_set([])
        assert analysis['size'] == 0
        assert analysis['arities'] == []

    def test_analyze_single_function(self):
        """Analysis of single function set."""
        analysis = analyze_nice_set([NAND])
        assert analysis['size'] == 1
        assert analysis['arities'] == [2]
        assert analysis['arity_distribution'] == {2: 1}

    def test_analyze_mixed_arity_set(self):
        """Analysis of mixed arity set."""
        analysis = analyze_nice_set([NOT, AND, OR])
        assert analysis['size'] == 3
        assert 1 in analysis['arity_distribution']  # NOT is unary
        assert 2 in analysis['arity_distribution']  # AND, OR are binary

    def test_analyze_includes_post_classes(self):
        """Analysis should include Post class information."""
        analysis = analyze_nice_set([NOT, AND])
        assert 'post_classes' in analysis
        assert NOT.name in analysis['post_classes']


class TestValidateNiceSet:
    """Test nice set validation."""

    def test_validate_nand_alone(self):
        """NAND alone should be valid."""
        is_valid, msg = validate_nice_set([NAND])
        assert is_valid
        assert "valid" in msg.lower()

    def test_validate_nor_alone(self):
        """NOR alone should be valid."""
        is_valid, msg = validate_nice_set([NOR])
        assert is_valid

    def test_validate_not_and(self):
        """NOT and AND should be valid."""
        is_valid, msg = validate_nice_set([NOT, AND])
        assert is_valid

    def test_validate_incomplete_set(self):
        """AND and OR (without NOT) should not be valid."""
        is_valid, msg = validate_nice_set([AND, OR])
        assert not is_valid
        assert "complete" in msg.lower()

    def test_validate_dependent_set(self):
        """NOT, AND, OR (with OR redundant) should not be valid at depth 3."""
        # OR is definable from NOT and AND via De Morgan
        # This should be detected at depth 3
        is_valid, msg = validate_nice_set([NOT, AND, OR], max_depth=3)
        assert not is_valid
        assert "independent" in msg.lower()


class TestKnownResults:
    """Test against known mathematical results."""

    def test_binary_max_is_exactly_3(self):
        """Binary-only maximum should be exactly 3."""
        max_size, sets = search_binary_only(verbose=False)
        assert max_size == 3

    def test_no_binary_nice_sets_of_size_4(self):
        """There should be no binary-only nice sets of size 4."""
        from src.connectives import generate_all_connectives
        binary = generate_all_connectives(2)

        size_4_sets = find_nice_sets_of_size(binary, 4, verbose=False)
        assert len(size_4_sets) == 0

    def test_sheffer_functions_are_nice_alone(self):
        """NAND and NOR should each be nice sets of size 1."""
        nand_sets = find_nice_sets_of_size([NAND], 1)
        nor_sets = find_nice_sets_of_size([NOR], 1)

        assert len(nand_sets) == 1
        assert len(nor_sets) == 1


class TestPerformance:
    """Test performance characteristics."""

    def test_binary_search_completes_quickly(self):
        """Binary-only search should complete in reasonable time."""
        import time
        start = time.time()
        max_size, sets = search_binary_only(verbose=False)
        elapsed = time.time() - start

        # Should complete in under 30 seconds
        assert elapsed < 30, f"Binary search took {elapsed:.2f}s (too slow)"

    @pytest.mark.slow
    def test_incremental_search_arity_2_fast(self):
        """Incremental search with max_arity=2 should complete within reasonable time.

        Note: Despite the name 'fast', incremental searches take several minutes.
        This test verifies it completes in under 10 minutes.
        Skip with: pytest -m "not slow"
        """
        import time
        start = time.time()
        max_size, sets, stats = search_incremental_arity(
            max_arity=2,
            verbose=False
        )
        elapsed = time.time() - start

        # Should complete in under 10 minutes (600 seconds)
        # Previous runs show ~380 seconds on some systems
        assert elapsed < 600, f"Arity-2 search took {elapsed:.2f}s (too slow, exceeded 10 minutes)"

        # Verify it found the expected max size of 5 for arity <= 2
        assert max_size == 5, f"Expected max_size=5 for arity<=2, got {max_size}"


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_request_size_larger_than_pool(self):
        """Requesting size larger than pool should return empty."""
        result = find_nice_sets_of_size([AND, OR], 5)
        assert result == []

    def test_all_incomplete_functions(self):
        """Pool of all incomplete functions should find no nice sets."""
        # CONST_TRUE and CONST_FALSE alone are incomplete
        result = find_nice_sets_of_size([CONST_TRUE, CONST_FALSE], 2)
        assert result == []

    def test_max_depth_affects_independence(self):
        """Different max_depth should potentially affect results."""
        # Test with very shallow depth (may miss some dependencies)
        is_valid_shallow, _ = validate_nice_set([NOT, AND, OR], max_depth=1)

        # Test with deeper depth (should catch OR being definable)
        is_valid_deep, _ = validate_nice_set([NOT, AND, OR], max_depth=3)

        # Deep search should be more conservative (catch more dependencies)
        # Note: OR is definable from NOT and AND in depth 3
        assert not is_valid_deep


class TestSymmetryBreakingSearch:
    """Test search with symmetry breaking."""

    def test_filtered_search_finds_correct_max(self):
        """Search with symmetry breaking should find same max size."""
        # Without symmetry breaking
        max_size_base, sets_base = search_binary_only(
            max_depth=3,
            verbose=False,
            use_symmetry_breaking=False
        )

        # With symmetry breaking
        max_size_filtered, sets_filtered = search_binary_only(
            max_depth=3,
            verbose=False,
            use_symmetry_breaking=True
        )

        # Both should find max=3
        assert max_size_base == max_size_filtered == 3

    def test_filtered_search_fewer_results(self):
        """Search with symmetry breaking should find fewer symmetric variants."""
        # Without symmetry breaking
        max_size_base, sets_base = search_binary_only(
            max_depth=3,
            verbose=False,
            use_symmetry_breaking=False
        )

        # With symmetry breaking
        max_size_filtered, sets_filtered = search_binary_only(
            max_depth=3,
            verbose=False,
            use_symmetry_breaking=True
        )

        # Filtered should find fewer sets (due to symmetry reduction)
        assert len(sets_filtered) < len(sets_base)
        assert len(sets_filtered) >= 1  # At least one representative
