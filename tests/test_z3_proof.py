"""
Tests for Z3 proof system.

This module tests the Z3-based proof approach for finding maximum
nice connective set sizes, including checkpoint management and
constraint generation.
"""

import pytest
import json
import time
from pathlib import Path

from src.proofs.z3_proof import (
    build_connective_pool,
    save_checkpoint,
    load_checkpoint
)
from src.constants import ALL_BINARY


class TestBuildConnectivePool:
    """Test connective pool building for Z3 proofs."""

    def test_max_arity_0(self):
        """Test pool with max_arity=0 (includes constants, unary, binary)."""
        # Note: build_connective_pool always includes binary (ALL_BINARY)
        pool = build_connective_pool(max_arity=0)
        assert len(pool) == 22  # 2 + 4 + 16
        arities = {c.arity for c in pool}
        assert arities == {0, 1, 2}

    def test_max_arity_1(self):
        """Test pool with max_arity=1 (includes constants, unary, binary)."""
        # Note: build_connective_pool always includes binary (ALL_BINARY)
        pool = build_connective_pool(max_arity=1)
        assert len(pool) == 22  # 2 + 4 + 16
        arities = {c.arity for c in pool}
        assert arities == {0, 1, 2}

    def test_max_arity_2(self):
        """Test pool with constants, unary, and binary."""
        pool = build_connective_pool(max_arity=2)
        assert len(pool) == 22  # 2 + 4 + 16
        arities = {c.arity for c in pool}
        assert arities == {0, 1, 2}

    def test_max_arity_3(self):
        """Test pool with all arities including ternary."""
        pool = build_connective_pool(max_arity=3)
        assert len(pool) == 278  # 2 + 4 + 16 + 256
        arities = {c.arity for c in pool}
        assert arities == {0, 1, 2, 3}

    def test_binary_connectives_included(self):
        """Test that all standard binary connectives are in pool."""
        pool = build_connective_pool(max_arity=2)
        # Extract binary connectives from pool
        binary_in_pool = [c for c in pool if c.arity == 2]
        assert len(binary_in_pool) == 16
        # Verify they match ALL_BINARY
        pool_values = {c.truth_table_int for c in binary_in_pool}
        expected_values = {c.truth_table_int for c in ALL_BINARY}
        assert pool_values == expected_values


class TestCheckpointSaveLoad:
    """Test checkpoint save and load functionality."""

    def test_save_checkpoint_creates_file(self, temp_checkpoint_file):
        """Test that save_checkpoint creates a valid JSON file."""
        candidates_checked = 100
        blocked_sets = [[0, 1, 2], [3, 4, 5]]
        nice_sets_found = [[6, 7, 8]]
        start_time = time.time()

        save_checkpoint(
            temp_checkpoint_file,
            candidates_checked,
            blocked_sets,
            nice_sets_found,
            start_time
        )

        assert temp_checkpoint_file.exists()
        assert temp_checkpoint_file.suffix == '.json'

    def test_save_checkpoint_valid_json(self, temp_checkpoint_file):
        """Test that saved checkpoint contains valid JSON."""
        save_checkpoint(
            temp_checkpoint_file,
            50,
            [[1, 2]],
            [[3, 4]],
            time.time()
        )

        # Should be readable as JSON
        with open(temp_checkpoint_file, 'r') as f:
            data = json.load(f)

        assert isinstance(data, dict)

    def test_save_checkpoint_required_fields(self, temp_checkpoint_file):
        """Test that checkpoint contains all required fields."""
        candidates_checked = 42
        blocked_sets = [[0, 1]]
        nice_sets_found = []
        start_time = time.time()

        save_checkpoint(
            temp_checkpoint_file,
            candidates_checked,
            blocked_sets,
            nice_sets_found,
            start_time
        )

        with open(temp_checkpoint_file, 'r') as f:
            data = json.load(f)

        # Check required fields
        assert 'candidates_checked' in data
        assert 'blocked_sets' in data
        assert 'nice_sets_found' in data
        assert 'elapsed_time' in data
        assert 'timestamp' in data

        # Check values
        assert data['candidates_checked'] == 42
        assert data['blocked_sets'] == [[0, 1]]
        assert data['nice_sets_found'] == []

    def test_load_checkpoint_missing_file(self):
        """Test that load_checkpoint returns None for missing file."""
        result = load_checkpoint('nonexistent_file.json')
        assert result is None

    def test_load_checkpoint_reads_data(self, temp_checkpoint_file):
        """Test that load_checkpoint correctly reads saved data."""
        # Save checkpoint
        candidates_checked = 123
        blocked_sets = [[1, 2, 3]]
        nice_sets_found = [[4, 5]]
        start_time = time.time()

        save_checkpoint(
            temp_checkpoint_file,
            candidates_checked,
            blocked_sets,
            nice_sets_found,
            start_time
        )

        # Load checkpoint
        loaded_data = load_checkpoint(temp_checkpoint_file)

        assert loaded_data is not None
        assert loaded_data['candidates_checked'] == 123
        assert loaded_data['blocked_sets'] == [[1, 2, 3]]
        assert loaded_data['nice_sets_found'] == [[4, 5]]

    def test_checkpoint_elapsed_time(self, temp_checkpoint_file):
        """Test that checkpoint records elapsed time correctly."""
        start_time = time.time()
        time.sleep(0.01)  # Small delay

        save_checkpoint(
            temp_checkpoint_file,
            10,
            [],
            [],
            start_time
        )

        loaded_data = load_checkpoint(temp_checkpoint_file)
        assert loaded_data['elapsed_time'] > 0

    def test_checkpoint_timestamp(self, temp_checkpoint_file):
        """Test that checkpoint includes timestamp."""
        save_checkpoint(
            temp_checkpoint_file,
            5,
            [],
            [],
            time.time()
        )

        loaded_data = load_checkpoint(temp_checkpoint_file)
        assert 'timestamp' in loaded_data
        assert loaded_data['timestamp'] > 0


class TestCheckpointDataStructures:
    """Test checkpoint data structure integrity."""

    def test_empty_blocked_sets(self, temp_checkpoint_file):
        """Test checkpoint with no blocked sets."""
        save_checkpoint(temp_checkpoint_file, 0, [], [], time.time())
        data = load_checkpoint(temp_checkpoint_file)
        assert data['blocked_sets'] == []

    def test_empty_nice_sets(self, temp_checkpoint_file):
        """Test checkpoint with no nice sets found."""
        save_checkpoint(temp_checkpoint_file, 10, [[1, 2]], [], time.time())
        data = load_checkpoint(temp_checkpoint_file)
        assert data['nice_sets_found'] == []

    def test_multiple_blocked_sets(self, temp_checkpoint_file):
        """Test checkpoint with multiple blocked sets."""
        blocked = [[0, 1], [2, 3], [4, 5, 6]]
        save_checkpoint(temp_checkpoint_file, 15, blocked, [], time.time())
        data = load_checkpoint(temp_checkpoint_file)
        assert data['blocked_sets'] == blocked

    def test_multiple_nice_sets(self, temp_checkpoint_file):
        """Test checkpoint with multiple nice sets."""
        nice_sets = [[0, 1, 2], [3, 4, 5, 6]]
        save_checkpoint(temp_checkpoint_file, 20, [], nice_sets, time.time())
        data = load_checkpoint(temp_checkpoint_file)
        assert data['nice_sets_found'] == nice_sets


@pytest.mark.integration
class TestZ3Integration:
    """Integration tests for Z3 proof system (using real Z3 with small datasets)."""

    def test_small_pool_search(self, sample_connective_pool):
        """Test Z3 search with a small connective pool."""
        # This is a simplified integration test
        # We import the function but don't run full search due to time
        from src.proofs.z3_proof import z3_proof_approach_1_symmetry_breaking

        # Test that function can be called (will exit early with max_candidates)
        # Using a very small pool and very low max_candidates for speed
        small_pool = sample_connective_pool[:10]  # Only 10 connectives

        # This should complete quickly with max_candidates=1
        result = z3_proof_approach_1_symmetry_breaking(
            pool=small_pool,
            target_size=3,
            max_depth=2,
            checkpoint_path=None,
            max_candidates=1  # Stop after 1 candidate
        )

        # Result should be boolean (True = no nice sets, False = found nice sets)
        assert isinstance(result, bool)
