"""
Utility functions for Jupyter notebooks in the Nice Connectives project.

This module provides visualization and display helpers for working with
logical connectives interactively in Jupyter notebooks.
"""

import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from src.connectives import Connective


def display_truth_table(connective):
    """
    Display a connective's truth table as a pandas DataFrame.

    Args:
        connective: A Connective instance

    Returns:
        pandas.DataFrame: Truth table with inputs and output column

    Example:
        >>> from src.constants import AND
        >>> df = display_truth_table(AND)
        >>> print(df)
    """
    arity = connective.arity
    num_rows = 2 ** arity

    # Generate all input combinations
    rows = []
    for i in range(num_rows):
        # Convert row number to binary inputs
        inputs = tuple((i >> j) & 1 for j in range(arity))
        output = connective.evaluate(*inputs)
        rows.append(inputs + (output,))

    # Create column names
    input_cols = [f'x{i}' for i in range(arity)]
    columns = input_cols + ['output']

    return pd.DataFrame(rows, columns=columns)


def visualize_truth_table(connective, title=None, figsize=(6, 4)):
    """
    Visualize a connective's truth table as a colored heatmap.

    Args:
        connective: A Connective instance
        title: Optional title for the plot (defaults to connective name)
        figsize: Figure size as (width, height) tuple

    Returns:
        matplotlib.figure.Figure: The created figure

    Example:
        >>> from src.constants import XOR
        >>> fig = visualize_truth_table(XOR)
        >>> plt.show()
    """
    df = display_truth_table(connective)

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Convert DataFrame to array for heatmap
    data = df.values

    # Create heatmap
    cmap = plt.cm.RdYlGn
    im = ax.imshow(data, cmap=cmap, aspect='auto', vmin=0, vmax=1)

    # Set ticks and labels
    ax.set_xticks(range(len(df.columns)))
    ax.set_xticklabels(df.columns)
    ax.set_yticks(range(len(df)))
    ax.set_yticklabels(range(len(df)))

    # Add text annotations
    for i in range(len(df)):
        for j in range(len(df.columns)):
            text = ax.text(j, i, int(data[i, j]),
                          ha="center", va="center", color="black", fontweight='bold')

    # Set title
    if title is None:
        title = f"Truth Table: {connective.name}"
    ax.set_title(title, fontsize=14, fontweight='bold')

    # Add colorbar
    cbar = plt.colorbar(im, ax=ax, ticks=[0, 1])
    cbar.set_label('Truth Value', rotation=270, labelpad=15)

    plt.tight_layout()
    return fig


def compare_connectives(connective_list, titles=None, figsize=(15, 4)):
    """
    Display multiple connectives side-by-side for comparison.

    Args:
        connective_list: List of Connective instances
        titles: Optional list of titles (defaults to connective names)
        figsize: Figure size as (width, height) tuple

    Returns:
        matplotlib.figure.Figure: The created figure with subplots

    Example:
        >>> from src.constants import AND, OR, XOR
        >>> fig = compare_connectives([AND, OR, XOR])
        >>> plt.show()
    """
    num_connectives = len(connective_list)
    fig, axes = plt.subplots(1, num_connectives, figsize=figsize)

    # Handle single connective case
    if num_connectives == 1:
        axes = [axes]

    for idx, (connective, ax) in enumerate(zip(connective_list, axes)):
        df = display_truth_table(connective)
        data = df.values

        # Create heatmap
        cmap = plt.cm.RdYlGn
        im = ax.imshow(data, cmap=cmap, aspect='auto', vmin=0, vmax=1)

        # Set ticks and labels
        ax.set_xticks(range(len(df.columns)))
        ax.set_xticklabels(df.columns, fontsize=9)
        ax.set_yticks(range(len(df)))
        ax.set_yticklabels(range(len(df)), fontsize=9)

        # Add text annotations
        for i in range(len(df)):
            for j in range(len(df.columns)):
                ax.text(j, i, int(data[i, j]),
                       ha="center", va="center", color="black", fontweight='bold')

        # Set title
        if titles and idx < len(titles):
            title = titles[idx]
        else:
            title = connective.name
        ax.set_title(title, fontsize=12, fontweight='bold')

    plt.tight_layout()
    return fig


def plot_arity_distribution(connective_list, title="Arity Distribution", figsize=(8, 5)):
    """
    Plot the distribution of arities in a list of connectives.

    Args:
        connective_list: List of Connective instances
        title: Plot title
        figsize: Figure size as (width, height) tuple

    Returns:
        matplotlib.figure.Figure: The created figure

    Example:
        >>> from src.constants import ALL_BINARY
        >>> fig = plot_arity_distribution(ALL_BINARY)
        >>> plt.show()
    """
    # Count arities
    arity_counts = {}
    for conn in connective_list:
        arity = conn.arity
        arity_counts[arity] = arity_counts.get(arity, 0) + 1

    # Sort by arity
    arities = sorted(arity_counts.keys())
    counts = [arity_counts[a] for a in arities]

    # Create bar plot
    fig, ax = plt.subplots(figsize=figsize)
    colors = plt.cm.viridis([i / len(arities) for i in range(len(arities))])
    bars = ax.bar(arities, counts, color=colors, edgecolor='black', linewidth=1.5)

    # Add value labels on bars
    for bar, count in zip(bars, counts):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height,
               f'{int(count)}',
               ha='center', va='bottom', fontweight='bold')

    # Labels and title
    ax.set_xlabel('Arity', fontsize=12, fontweight='bold')
    ax.set_ylabel('Count', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xticks(arities)
    ax.grid(axis='y', alpha=0.3, linestyle='--')

    plt.tight_layout()
    return fig


def print_nice_set_summary(connective_list, name="Nice Set"):
    """
    Print a summary of a nice set of connectives.

    Args:
        connective_list: List of Connective instances
        name: Name for the nice set

    Example:
        >>> from src.constants import AND, OR, XOR
        >>> print_nice_set_summary([AND, OR, XOR], "Example Set")
    """
    print(f"=== {name} ===")
    print(f"Size: {len(connective_list)}")

    # Arity distribution
    arity_counts = {}
    for conn in connective_list:
        arity = conn.arity
        arity_counts[arity] = arity_counts.get(arity, 0) + 1

    print("\nArity Distribution:")
    for arity in sorted(arity_counts.keys()):
        count = arity_counts[arity]
        percentage = (count / len(connective_list)) * 100
        print(f"  Arity {arity}: {count} connectives ({percentage:.1f}%)")

    print("\nConnectives:")
    for conn in connective_list:
        print(f"  - {conn.name} (arity {conn.arity})")


# Convenience re-exports for common constants
def get_common_connectives():
    """
    Get a dictionary of commonly used connectives.

    Returns:
        dict: Dictionary mapping names to Connective instances
    """
    from src.constants import (
        FALSE, TRUE, NOT,
        AND, OR, XOR, NAND, NOR, IMP, EQUIV
    )

    return {
        'FALSE': FALSE,
        'TRUE': TRUE,
        'NOT': NOT,
        'AND': AND,
        'OR': OR,
        'XOR': XOR,
        'NAND': NAND,
        'NOR': NOR,
        'IMP': IMP,
        'EQUIV': EQUIV,
    }
