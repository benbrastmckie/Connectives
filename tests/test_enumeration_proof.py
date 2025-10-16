"""
Tests for enumeration-based proof system.

This module tests the pattern enumeration proof approach for
verifying maximum nice connective set sizes.
"""

import pytest
from src.proofs.enumeration_proof import (
    build_connective_pool,
    verify_size_16_exists,
    prove_size_17_impossible
)


class TestBuildConnectivePool:
    """Test connective pool building for enumeration proof."""

    def test_max_arity_3(self):
        """Test building pool with arity 0-3."""
        pool = build_connective_pool(max_arity=3)
        assert len(pool) == 278  # 2 + 4 + 16 + 256
        arities = {c.arity for c in pool}
        assert arities == {0, 1, 2, 3}

    def test_pool_contains_all_arities(self):
        """Test that pool contains all expected arities."""
        pool = build_connective_pool(max_arity=3)
        # Count connectives by arity
        arity_counts = {}
        for c in pool:
            arity_counts[c.arity] = arity_counts.get(c.arity, 0) + 1

        assert arity_counts[0] == 2     # Constants
        assert arity_counts[1] == 4     # Unary
        assert arity_counts[2] == 16    # Binary
        assert arity_counts[3] == 256   # Ternary


class TestVerifySize16Exists:
    """Test verification of size-16 nice set existence."""

    @pytest.mark.slow
    def test_verify_returns_tuple(self, sample_connective_pool):
        """Test that verify_size_16_exists returns a tuple."""
        # Use a small pool for speed - test structure, not actual verification
        result = verify_size_16_exists(sample_connective_pool, max_depth=2)
        assert isinstance(result, tuple)
        assert len(result) == 2

    @pytest.mark.slow
    def test_verify_tuple_structure(self, sample_connective_pool):
        """Test the structure of returned tuple."""
        exists, example_set = verify_size_16_exists(sample_connective_pool, max_depth=2)
        assert isinstance(exists, bool)
        # example_set is either a list or None
        assert example_set is None or isinstance(example_set, list)


class TestProveSize17Impossible:
    """Test proof that size-17 nice sets don't exist."""

    @pytest.mark.slow
    def test_returns_tuple(self, sample_connective_pool):
        """Test that prove_size_17_impossible returns a tuple."""
        # Use very small sample size for speed
        result = prove_size_17_impossible(
            sample_connective_pool,
            max_depth=2,
            sample_size=10  # Tiny sample for test speed
        )
        assert isinstance(result, tuple)
        assert len(result) == 3

    @pytest.mark.slow
    def test_tuple_structure(self, sample_connective_pool):
        """Test the structure of returned tuple."""
        proven, checked, elapsed = prove_size_17_impossible(
            sample_connective_pool,
            max_depth=2,
            sample_size=10
        )
        assert isinstance(proven, bool)
        assert isinstance(checked, int)
        assert isinstance(elapsed, float)
        assert checked >= 0
        assert elapsed >= 0


class TestEnumerationProofStructure:
    """Test the structure and organization of enumeration proof."""

    def test_module_imports(self):
        """Test that key components can be imported."""
        # These imports should not raise errors
        from src.proofs.enumeration_proof import build_connective_pool
        from src.proofs.enumeration_proof import verify_size_16_exists
        from src.proofs.enumeration_proof import prove_size_17_impossible

        assert build_connective_pool is not None
        assert verify_size_16_exists is not None
        assert prove_size_17_impossible is not None
