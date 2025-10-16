"""
Test suite for prove command implementations.

Tests both Z3-based and enumeration-based proof commands.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.commands.prove import prove_z3, prove_enumeration
from src.independence import DefinabilityMode


class TestProveZ3:
    """Test Z3-based proof command."""

    @patch('src.commands.prove.z3_proof_approach_1_symmetry_breaking')
    @patch('src.commands.prove.build_connective_pool')
    def test_prove_z3_success_no_target_size(self, mock_pool, mock_z3_proof):
        """Test Z3 proof when no size-17 sets exist (success case)."""
        # Mock pool building
        mock_pool.return_value = [Mock(arity=2) for _ in range(10)]

        # Mock Z3 proof returning True (no size-17 sets exist)
        mock_z3_proof.return_value = True

        # Run command
        exit_code = prove_z3(
            checkpoint=None,
            interval=100,
            target_size=17,
            max_depth=3,
            max_arity=3,
            max_candidates=1000
        )

        # Verify exit code (0 = success)
        assert exit_code == 0

        # Verify pool was built correctly
        mock_pool.assert_called_once_with(max_arity=3)

        # Verify Z3 proof was called with correct arguments
        mock_z3_proof.assert_called_once()
        args = mock_z3_proof.call_args
        assert args[1]['target_size'] == 17
        assert args[1]['max_depth'] == 3
        assert args[1]['checkpoint_interval'] == 100
        assert args[1]['max_candidates'] == 1000

    @patch('src.commands.prove.z3_proof_approach_1_symmetry_breaking')
    @patch('src.commands.prove.build_connective_pool')
    def test_prove_z3_failure_target_size_exists(self, mock_pool, mock_z3_proof):
        """Test Z3 proof when size-17 sets exist (failure case)."""
        # Mock pool building
        mock_pool.return_value = [Mock(arity=2) for _ in range(10)]

        # Mock Z3 proof returning False (size-17 sets exist)
        mock_z3_proof.return_value = False

        # Run command
        exit_code = prove_z3(target_size=17)

        # Verify exit code (1 = failure, sets exist)
        assert exit_code == 1

    @patch('src.commands.prove.z3_proof_approach_1_symmetry_breaking')
    @patch('src.commands.prove.build_connective_pool')
    def test_prove_z3_with_checkpoint(self, mock_pool, mock_z3_proof):
        """Test Z3 proof with checkpoint file specified."""
        mock_pool.return_value = [Mock(arity=2) for _ in range(10)]
        mock_z3_proof.return_value = True

        # Run with checkpoint
        exit_code = prove_z3(checkpoint='/tmp/checkpoint.json', interval=50)

        # Verify checkpoint path was passed through
        args = mock_z3_proof.call_args
        assert args[1]['checkpoint_path'] == '/tmp/checkpoint.json'
        assert args[1]['checkpoint_interval'] == 50

    @patch('src.commands.prove.z3_proof_approach_1_symmetry_breaking')
    @patch('src.commands.prove.build_connective_pool')
    def test_prove_z3_custom_parameters(self, mock_pool, mock_z3_proof):
        """Test Z3 proof with custom depth and arity parameters."""
        mock_pool.return_value = [Mock(arity=2) for _ in range(10)]
        mock_z3_proof.return_value = True

        # Run with custom parameters
        exit_code = prove_z3(
            max_depth=5,
            max_arity=4,
            target_size=18,
            max_candidates=5000
        )

        # Verify custom parameters were passed
        mock_pool.assert_called_once_with(max_arity=4)
        args = mock_z3_proof.call_args
        assert args[1]['target_size'] == 18
        assert args[1]['max_depth'] == 5
        assert args[1]['max_candidates'] == 5000

    @patch('src.commands.prove.z3_proof_approach_1_symmetry_breaking')
    @patch('src.commands.prove.build_connective_pool')
    def test_prove_z3_syntactic_mode(self, mock_pool, mock_z3_proof):
        """Test Z3 proof with syntactic definability mode."""
        mock_pool.return_value = [Mock(arity=2) for _ in range(10)]
        mock_z3_proof.return_value = True

        exit_code = prove_z3(definability_mode=DefinabilityMode.SYNTACTIC)

        args = mock_z3_proof.call_args
        assert args[1]['definability_mode'] == DefinabilityMode.SYNTACTIC

    @patch('src.commands.prove.z3_proof_approach_1_symmetry_breaking')
    @patch('src.commands.prove.build_connective_pool')
    def test_prove_z3_truth_functional_mode(self, mock_pool, mock_z3_proof):
        """Test Z3 proof with truth-functional definability mode."""
        mock_pool.return_value = [Mock(arity=2) for _ in range(10)]
        mock_z3_proof.return_value = True

        exit_code = prove_z3(definability_mode=DefinabilityMode.TRUTH_FUNCTIONAL)

        args = mock_z3_proof.call_args
        assert args[1]['definability_mode'] == DefinabilityMode.TRUTH_FUNCTIONAL


class TestProveEnumeration:
    """Test enumeration-based proof command."""

    @patch('src.commands.prove.enumeration_proof')
    def test_prove_enumeration_success(self, mock_enum_proof):
        """Test enumeration proof returns exit code from main()."""
        # Mock enumeration_proof.main() returning 0
        mock_enum_proof.main.return_value = 0

        exit_code = prove_enumeration()

        assert exit_code == 0
        mock_enum_proof.main.assert_called_once()

    @patch('src.commands.prove.enumeration_proof')
    def test_prove_enumeration_failure(self, mock_enum_proof):
        """Test enumeration proof propagates failure exit code."""
        # Mock enumeration_proof.main() returning 1
        mock_enum_proof.main.return_value = 1

        exit_code = prove_enumeration()

        assert exit_code == 1

    @patch('src.commands.prove.enumeration_proof')
    def test_prove_enumeration_syntactic_mode(self, mock_enum_proof):
        """Test enumeration proof with syntactic mode."""
        mock_enum_proof.main.return_value = 0

        exit_code = prove_enumeration(definability_mode=DefinabilityMode.SYNTACTIC)

        mock_enum_proof.main.assert_called_once_with(
            definability_mode=DefinabilityMode.SYNTACTIC
        )

    @patch('src.commands.prove.enumeration_proof')
    def test_prove_enumeration_truth_functional_mode(self, mock_enum_proof):
        """Test enumeration proof with truth-functional mode."""
        mock_enum_proof.main.return_value = 0

        exit_code = prove_enumeration(definability_mode=DefinabilityMode.TRUTH_FUNCTIONAL)

        mock_enum_proof.main.assert_called_once_with(
            definability_mode=DefinabilityMode.TRUTH_FUNCTIONAL
        )


class TestProveIntegration:
    """Integration tests for prove commands."""

    @patch('src.commands.prove.z3_proof_approach_1_symmetry_breaking')
    @patch('src.commands.prove.build_connective_pool')
    def test_prove_z3_prints_output(self, mock_pool, mock_z3_proof, capsys):
        """Test that prove_z3 prints expected output."""
        mock_pool.return_value = [Mock(arity=2) for _ in range(10)]
        mock_z3_proof.return_value = True

        prove_z3(target_size=17, max_arity=3, max_depth=3)

        captured = capsys.readouterr()

        # Verify output contains key information
        assert "Z3-BASED PROOF" in captured.out
        assert "MAXIMUM NICE SET SIZE = 16" in captured.out
        assert "Arity range: 0-3" in captured.out
        assert "Depth: 3" in captured.out
        assert "Connective pool size: 10" in captured.out
        assert "CONCLUSION" in captured.out
        assert "PROVEN" in captured.out

    @patch('src.commands.prove.z3_proof_approach_1_symmetry_breaking')
    @patch('src.commands.prove.build_connective_pool')
    def test_prove_z3_pool_building(self, mock_pool, mock_z3_proof):
        """Test that connective pool is built with correct max_arity."""
        mock_pool.return_value = [
            Mock(arity=0),  # Constants
            Mock(arity=1),  # Unary
            Mock(arity=2),  # Binary
            Mock(arity=3),  # Ternary
        ]
        mock_z3_proof.return_value = True

        prove_z3(max_arity=3)

        # Verify pool building was called correctly
        mock_pool.assert_called_once_with(max_arity=3)

        # Verify pool was passed to Z3 proof
        pool_arg = mock_z3_proof.call_args[0][0]
        assert len(pool_arg) == 4
