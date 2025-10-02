"""
Predefined standard logical connectives.

This module defines commonly used logical connectives for quick reference.
Each connective is defined by its arity and truth table value.
"""

from src.connectives import Connective


# ========== Arity 0 (Constants) ==========

CONST_FALSE = Connective(0, 0b0, "FALSE")
CONST_TRUE = Connective(0, 0b1, "TRUE")


# ========== Arity 1 (Unary) ==========

IDENTITY = Connective(1, 0b10, "ID")      # f(x) = x
NEGATION = Connective(1, 0b01, "NOT")     # f(x) = ¬x
CONST_0_UNARY = Connective(1, 0b00, "0")  # f(x) = 0
CONST_1_UNARY = Connective(1, 0b11, "1")  # f(x) = 1

NOT = NEGATION  # Alias


# ========== Arity 2 (Binary) ==========
# Truth table encoding: bit positions for inputs (x, y):
# Position: (0,0)=0, (0,1)=1, (1,0)=2, (1,1)=3
# Value: 0b[bit3][bit2][bit1][bit0]

# Basic operations
AND = Connective(2, 0b1000, "AND")        # x ∧ y
OR = Connective(2, 0b1110, "OR")          # x ∨ y
XOR = Connective(2, 0b0110, "XOR")        # x ⊕ y
IMPLIES = Connective(2, 0b1011, "IMP")    # x → y
IFF = Connective(2, 0b1001, "IFF")        # x ↔ y (equivalence)

# Negated operations
NAND = Connective(2, 0b0111, "NAND")      # ¬(x ∧ y)
NOR = Connective(2, 0b0001, "NOR")        # ¬(x ∨ y)
XNOR = Connective(2, 0b1001, "XNOR")      # ¬(x ⊕ y) = IFF

# Projections and variants
PROJECT_X = Connective(2, 0b1100, "PROJ_X")       # f(x,y) = x
PROJECT_Y = Connective(2, 0b1010, "PROJ_Y")       # f(x,y) = y
NOT_X = Connective(2, 0b0011, "NOT_X")            # f(x,y) = ¬x
NOT_Y = Connective(2, 0b0101, "NOT_Y")            # f(x,y) = ¬y

# Constants (binary arity)
CONST_FALSE_BIN = Connective(2, 0b0000, "FALSE_2")  # f(x,y) = 0
CONST_TRUE_BIN = Connective(2, 0b1111, "TRUE_2")    # f(x,y) = 1

# Other named binary functions
INHIBIT = Connective(2, 0b0010, "INHIBIT")        # x ∧ ¬y
CONVERSE_INHIBIT = Connective(2, 0b0100, "CONV_INHIBIT")  # ¬x ∧ y
CONVERSE_IMP = Connective(2, 0b1101, "CONV_IMP")  # y → x


# ========== Collections ==========

# All 16 binary connectives
ALL_BINARY = [
    CONST_FALSE_BIN,     # 0b0000 = 0
    NOR,                 # 0b0001 = 1
    INHIBIT,             # 0b0010 = 2
    NOT_X,               # 0b0011 = 3
    CONVERSE_INHIBIT,    # 0b0100 = 4
    NOT_Y,               # 0b0101 = 5
    XOR,                 # 0b0110 = 6
    NAND,                # 0b0111 = 7
    AND,                 # 0b1000 = 8
    IFF,                 # 0b1001 = 9
    PROJECT_Y,           # 0b1010 = 10
    IMPLIES,             # 0b1011 = 11
    PROJECT_X,           # 0b1100 = 12
    CONVERSE_IMP,        # 0b1101 = 13
    OR,                  # 0b1110 = 14
    CONST_TRUE_BIN,      # 0b1111 = 15
]

# Commonly used complete sets (for reference)
COMPLETE_SET_NAND = [NAND]                    # {NAND} is complete
COMPLETE_SET_NOR = [NOR]                      # {NOR} is complete
COMPLETE_SET_STANDARD = [NOT, AND, OR]        # Standard complete set
COMPLETE_SET_MINIMAL = [NOT, AND]             # Minimal complete set


# ========== Helper Functions ==========

def get_binary_by_value(value: int) -> Connective:
    """
    Get a binary connective by its truth table value.

    Args:
        value: Truth table value (0-15)

    Returns:
        Corresponding binary connective

    Raises:
        ValueError: If value is not in range 0-15
    """
    if not 0 <= value <= 15:
        raise ValueError(f"Binary connective value must be 0-15, got {value}")
    return ALL_BINARY[value]


def get_connective_by_name(name: str) -> Connective:
    """
    Get a connective by its standard name.

    Args:
        name: Name of the connective (case-insensitive)

    Returns:
        Corresponding connective

    Raises:
        ValueError: If name is not recognized
    """
    name_upper = name.upper()

    # Build name mapping
    name_map = {
        # Arity 0
        'FALSE': CONST_FALSE,
        'TRUE': CONST_TRUE,
        # Arity 1
        'ID': IDENTITY,
        'IDENTITY': IDENTITY,
        'NOT': NOT,
        'NEGATION': NEGATION,
        # Arity 2
        'AND': AND,
        'OR': OR,
        'XOR': XOR,
        'NAND': NAND,
        'NOR': NOR,
        'IMPLIES': IMPLIES,
        'IMP': IMPLIES,
        'IFF': IFF,
        'XNOR': XNOR,
        'PROJ_X': PROJECT_X,
        'PROJ_Y': PROJECT_Y,
        'NOT_X': NOT_X,
        'NOT_Y': NOT_Y,
        'INHIBIT': INHIBIT,
        'CONV_INHIBIT': CONVERSE_INHIBIT,
        'CONV_IMP': CONVERSE_IMP,
    }

    if name_upper not in name_map:
        raise ValueError(f"Unknown connective name: {name}")

    return name_map[name_upper]
