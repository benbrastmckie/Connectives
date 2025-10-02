"""
Z3 SAT-based independence checker using composition tree encoding.

This module implements Approach 4 from the Z3 SMT application analysis:
SAT-based enumeration with pure Boolean constraints for efficient
composition search.

Key features:
- Binary choice variables for function selection at each node
- Boolean output variables for each node and input assignment
- Cardinality constraints for "exactly one function per node"
- Iterative deepening to find minimal depth compositions
- Witness extraction for debugging and verification
"""

from typing import List, Tuple, Optional, Dict, Any
from z3 import Solver, Bool, And, Or, PbEq, sat, unsat
from src.connectives import Connective


class CompositionTree:
    """
    Represents a composition tree witness.

    A composition tree shows how a target connective can be expressed
    as a composition of basis functions.
    """

    def __init__(self, function: Connective,
                 left_child: Optional['CompositionTree'] = None,
                 right_child: Optional['CompositionTree'] = None,
                 middle_child: Optional['CompositionTree'] = None,
                 var_index: Optional[int] = None):
        """
        Initialize a composition tree node.

        Args:
            function: The connective at this node
            left_child: Left child tree (for binary/ternary functions)
            right_child: Right child tree (for binary/ternary functions)
            middle_child: Middle child tree (for ternary functions)
            var_index: Variable index for leaf nodes (0=x, 1=y, 2=z, etc.)
        """
        self.function = function
        self.left_child = left_child
        self.right_child = right_child
        self.middle_child = middle_child
        self.var_index = var_index

    def to_formula(self) -> str:
        """
        Convert the composition tree to a formula string.

        Returns:
            String representation like "NOT(AND(x, y))"
        """
        # Check if this is a leaf variable node
        if self.var_index is not None:
            var_names = ['x', 'y', 'z', 'w', 'v']
            return var_names[self.var_index]

        if self.function.arity == 0:
            # Constant (nullary)
            return self.function.name

        elif self.function.arity == 1:
            # Unary function
            if self.left_child is None:
                # Leaf node - shouldn't happen if var_index is set properly
                return "x"
            else:
                child_formula = self.left_child.to_formula()
                return f"{self.function.name}({child_formula})"

        elif self.function.arity == 2:
            # Binary function
            if self.left_child is None and self.right_child is None:
                # Leaf node - shouldn't happen for binary
                return f"{self.function.name}(x, y)"
            elif self.left_child is None:
                # Left is variable
                right_formula = self.right_child.to_formula()
                return f"{self.function.name}(x, {right_formula})"
            elif self.right_child is None:
                # Right is variable
                left_formula = self.left_child.to_formula()
                return f"{self.function.name}({left_formula}, y)"
            else:
                # Both children
                left_formula = self.left_child.to_formula()
                right_formula = self.right_child.to_formula()
                return f"{self.function.name}({left_formula}, {right_formula})"

        elif self.function.arity == 3:
            # Ternary function
            left_formula = self.left_child.to_formula() if self.left_child else "x"
            middle_formula = self.middle_child.to_formula() if self.middle_child else "y"
            right_formula = self.right_child.to_formula() if self.right_child else "z"
            return f"{self.function.name}({left_formula}, {middle_formula}, {right_formula})"

        else:
            return f"{self.function.name}(...)"

    def evaluate(self, inputs: Tuple[int, ...]) -> int:
        """
        Evaluate the composition tree on given inputs.

        This is used to verify that the witness is correct.

        Args:
            inputs: Input values (0 or 1 for each variable)

        Returns:
            Output value (0 or 1)
        """
        # Check if this is a leaf variable node
        if self.var_index is not None:
            return inputs[self.var_index]

        if self.function.arity == 0:
            # Constant
            return self.function.evaluate(())

        elif self.function.arity == 1:
            if self.left_child is None:
                # Leaf - shouldn't happen if var_index is set properly
                return inputs[0]
            else:
                child_result = self.left_child.evaluate(inputs)
                return self.function.evaluate((child_result,))

        elif self.function.arity == 2:
            # Evaluate children
            if self.left_child is None:
                left_result = inputs[0]
            else:
                left_result = self.left_child.evaluate(inputs)

            if self.right_child is None:
                right_result = inputs[1] if len(inputs) > 1 else inputs[0]
            else:
                right_result = self.right_child.evaluate(inputs)

            return self.function.evaluate((left_result, right_result))

        elif self.function.arity == 3:
            # Ternary
            left_result = self.left_child.evaluate(inputs) if self.left_child else inputs[0]
            middle_result = self.middle_child.evaluate(inputs) if self.middle_child else inputs[1]
            right_result = self.right_child.evaluate(inputs) if self.right_child else inputs[2]
            return self.function.evaluate((left_result, middle_result, right_result))

        else:
            raise ValueError(f"Unsupported arity: {self.function.arity}")

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"CompositionTree({self.to_formula()})"


def _build_tree_structure(depth: int, max_arity: int = 2) -> Dict[str, Any]:
    """
    Build the structure of a composition tree for a given depth.

    For a binary tree of depth d, we have 2^d - 1 nodes.
    Nodes are indexed from 0 (root) to 2^d - 2.

    Args:
        depth: Maximum depth of the tree
        max_arity: Maximum arity of functions (2 for binary, 3 for ternary)

    Returns:
        Dictionary with tree structure information:
        - num_nodes: Total number of nodes
        - nodes: List of node indices
        - parents: Dict mapping node -> parent node
        - children: Dict mapping node -> list of child nodes
        - depth_of: Dict mapping node -> depth (0 = root)
        - leaves: List of leaf node indices
    """
    if depth < 1:
        raise ValueError("Depth must be >= 1")

    # For simplicity, we build a complete binary tree structure
    # even though not all nodes may be used
    num_nodes = 2 ** depth - 1
    nodes = list(range(num_nodes))

    # Build parent-child relationships
    # For node i: left_child = 2*i+1, right_child = 2*i+2
    parents = {}
    children = {}
    depth_of = {0: 0}

    for i in range(num_nodes):
        left = 2 * i + 1
        right = 2 * i + 2

        node_children = []
        if left < num_nodes:
            node_children.append(left)
            parents[left] = i
            depth_of[left] = depth_of[i] + 1

        if right < num_nodes:
            node_children.append(right)
            parents[right] = i
            depth_of[right] = depth_of[i] + 1

        children[i] = node_children

    # Identify leaves (nodes with no children)
    leaves = [i for i in nodes if not children[i]]

    return {
        'num_nodes': num_nodes,
        'nodes': nodes,
        'parents': parents,
        'children': children,
        'depth_of': depth_of,
        'leaves': leaves
    }


def _encode_tree_choices(solver: Solver, tree_struct: Dict[str, Any],
                         basis: List[Connective]) -> Dict[Tuple[int, int], Any]:
    """
    Encode choice variables: which function is selected at each node.

    For each node and each basis function, create a Boolean variable
    representing whether that function is selected at that node.

    Uses cardinality constraint to ensure exactly one function per node.

    Args:
        solver: Z3 solver instance
        tree_struct: Tree structure from _build_tree_structure
        basis: List of basis connectives

    Returns:
        Dictionary mapping (node_idx, func_idx) -> Bool variable
    """
    choices = {}

    for node in tree_struct['nodes']:
        # Create choice variables for this node
        node_choices = []
        for func_idx, func in enumerate(basis):
            choice_var = Bool(f'choice_{node}_{func_idx}')
            choices[(node, func_idx)] = choice_var
            node_choices.append(choice_var)

        # Add cardinality constraint: exactly one function selected
        # PbEq means "pseudo-Boolean equals"
        # This is efficient for SAT solvers
        solver.add(PbEq([(c, 1) for c in node_choices], 1))

    return choices


def _encode_tree_outputs(solver: Solver, tree_struct: Dict[str, Any],
                         basis: List[Connective], target: Connective,
                         choices: Dict[Tuple[int, int], Any]) -> Dict[Tuple[int, Tuple[int, ...]], Any]:
    """
    Encode output variables: what each node outputs for each input assignment.

    For each node and each input assignment (e.g., (0,0), (0,1), (1,0), (1,1)),
    create a Boolean variable representing the output of that node.

    Link outputs to chosen functions via implications.

    Args:
        solver: Z3 solver instance
        tree_struct: Tree structure
        basis: List of basis connectives
        target: Target connective (determines input space)
        choices: Choice variables from _encode_tree_choices

    Returns:
        Dictionary mapping (node_idx, input_assignment) -> Bool variable
    """
    outputs = {}
    num_inputs = target.arity

    # Generate all possible input assignments
    input_assignments = []
    for i in range(2 ** num_inputs):
        assignment = tuple((i >> (num_inputs - 1 - k)) & 1 for k in range(num_inputs))
        input_assignments.append(assignment)

    # For each node and input assignment, create output variable
    for node in tree_struct['nodes']:
        for inp in input_assignments:
            output_var = Bool(f'out_{node}_{inp}')
            outputs[(node, inp)] = output_var

    # Link outputs to chosen functions
    # If choice[node, func] is true, then output[node, inp] = func(children_outputs[inp])
    # This is complex and will be handled in _encode_tree_structure

    return outputs


def _encode_tree_structure(solver: Solver, tree_struct: Dict[str, Any],
                            basis: List[Connective], target: Connective,
                            choices: Dict[Tuple[int, int], Any],
                            outputs: Dict[Tuple[int, Tuple[int, ...]], Any]) -> None:
    """
    Encode parent-child constraints linking node outputs.

    For leaf nodes: outputs are input variables (no choice).
    For internal nodes: outputs depend on chosen function and children outputs.

    Args:
        solver: Z3 solver instance
        tree_struct: Tree structure
        basis: List of basis connectives
        target: Target connective
        choices: Choice variables
        outputs: Output variables
    """
    from z3 import Not, Implies

    num_inputs = target.arity
    leaves = tree_struct['leaves']
    children_map = tree_struct['children']

    # Get all input assignments
    input_assignments = []
    for i in range(2 ** num_inputs):
        inp = tuple((i >> (num_inputs - 1 - k)) & 1 for k in range(num_inputs))
        input_assignments.append(inp)

    # For leaf nodes: outputs equal the corresponding input variable
    for leaf in leaves:
        leaf_idx = leaves.index(leaf)
        for inp in input_assignments:
            # Map leaf to input variable
            # For binary: first two leaves map to x and y
            if num_inputs == 0:
                # Nullary (constant) - no variables, this shouldn't happen
                # but handle gracefully
                var_value = 0
            elif num_inputs == 1:
                var_value = inp[0]
            else:
                var_value = inp[leaf_idx % num_inputs]

            # Assert output equals variable value
            if var_value == 1:
                solver.add(outputs[(leaf, inp)])
            else:
                solver.add(Not(outputs[(leaf, inp)]))

    # For internal nodes: link outputs to function and children
    for node in tree_struct['nodes']:
        if node in leaves:
            continue

        node_children = children_map[node]
        if not node_children:
            continue

        for func_idx, func in enumerate(basis):
            choice = choices[(node, func_idx)]

            # For each input assignment
            for inp in input_assignments:
                node_out = outputs[(node, inp)]

                # Handle different arities
                if func.arity == 0:
                    # Constant function
                    func_output = func.evaluate(())
                    # If function is chosen: output == func_output
                    if func_output == 1:
                        solver.add(Implies(choice, node_out))
                    else:
                        solver.add(Implies(choice, Not(node_out)))

                elif func.arity == 1 and len(node_children) >= 1:
                    # Unary function
                    left_child = node_children[0]
                    left_out = outputs[(left_child, inp)]

                    # For each possible child output value
                    for child_val in [0, 1]:
                        func_out = func.evaluate((child_val,))

                        # If choice and child==child_val, then node_out==func_out
                        child_cond = left_out if child_val == 1 else Not(left_out)
                        out_cond = node_out if func_out == 1 else Not(node_out)

                        solver.add(Implies(And(choice, child_cond), out_cond))

                elif func.arity == 2 and len(node_children) >= 2:
                    # Binary function
                    left_child = node_children[0]
                    right_child = node_children[1]
                    left_out = outputs[(left_child, inp)]
                    right_out = outputs[(right_child, inp)]

                    # For each combination of child outputs
                    for left_val in [0, 1]:
                        for right_val in [0, 1]:
                            func_out = func.evaluate((left_val, right_val))

                            # If choice and children match vals, output matches func_out
                            left_cond = left_out if left_val == 1 else Not(left_out)
                            right_cond = right_out if right_val == 1 else Not(right_out)
                            out_cond = node_out if func_out == 1 else Not(node_out)

                            solver.add(Implies(And(choice, left_cond, right_cond), out_cond))


def _encode_target_match(solver: Solver, tree_struct: Dict[str, Any],
                         target: Connective,
                         outputs: Dict[Tuple[int, Tuple[int, ...]], Any]) -> None:
    """
    Encode constraint that root node output matches target truth table.

    Args:
        solver: Z3 solver instance
        tree_struct: Tree structure
        target: Target connective
        outputs: Output variables
    """
    from z3 import Not

    root = 0  # Root is always node 0
    num_inputs = target.arity

    # For each input assignment
    for i in range(2 ** num_inputs):
        inp = tuple((i >> (num_inputs - 1 - k)) & 1 for k in range(num_inputs))

        # Get target's output for this input
        target_out = target.evaluate(inp)

        # Root output must match target output
        root_out_var = outputs[(root, inp)]

        if target_out == 1:
            solver.add(root_out_var)
        else:
            solver.add(Not(root_out_var))


def _extract_witness_from_model(model, tree_struct: Dict[str, Any],
                                  basis: List[Connective],
                                  choices: Dict[Tuple[int, int], Any],
                                  num_inputs: int) -> CompositionTree:
    """
    Extract a composition tree witness from a satisfying Z3 model.

    Args:
        model: Z3 model (from solver.model())
        tree_struct: Tree structure from _build_tree_structure
        basis: List of basis connectives
        choices: Choice variables from _encode_tree_choices
        num_inputs: Number of inputs (arity of target connective)

    Returns:
        CompositionTree representing the witness composition
    """
    from z3 import is_true

    # Map node index to CompositionTree
    node_trees = {}
    leaves = tree_struct['leaves']

    # Process nodes in reverse order (leaves first, then parents)
    # This ensures children are processed before parents
    nodes_by_depth = {}
    for node in tree_struct['nodes']:
        depth = tree_struct['depth_of'][node]
        if depth not in nodes_by_depth:
            nodes_by_depth[depth] = []
        nodes_by_depth[depth].append(node)

    # Process from deepest to shallowest
    max_depth = max(nodes_by_depth.keys())
    for depth in range(max_depth, -1, -1):
        for node in nodes_by_depth[depth]:
            # Find which function is selected at this node
            selected_func = None
            for func_idx, func in enumerate(basis):
                choice_var = choices[(node, func_idx)]
                if is_true(model.eval(choice_var)):
                    selected_func = func
                    break

            if selected_func is None:
                raise ValueError(f"No function selected for node {node}")

            # Get children
            node_children = tree_struct['children'][node]

            if not node_children:
                # Leaf node - compute var_index
                if num_inputs > 0:
                    leaf_idx = leaves.index(node)
                    var_idx = leaf_idx % num_inputs
                    node_trees[node] = CompositionTree(selected_func, var_index=var_idx)
                else:
                    # Nullary target (constant) - no variables
                    node_trees[node] = CompositionTree(selected_func)
            elif selected_func.arity == 1 and len(node_children) >= 1:
                # Unary function - one child
                left_child = node_children[0]
                node_trees[node] = CompositionTree(
                    selected_func,
                    left_child=node_trees[left_child]
                )
            elif selected_func.arity == 2 and len(node_children) >= 2:
                # Binary function - two children
                left_child = node_children[0]
                right_child = node_children[1]
                node_trees[node] = CompositionTree(
                    selected_func,
                    left_child=node_trees[left_child],
                    right_child=node_trees[right_child]
                )
            elif selected_func.arity == 0:
                # Constant - no children needed
                node_trees[node] = CompositionTree(selected_func)
            else:
                raise ValueError(f"Unsupported arity {selected_func.arity} for node {node}")

    # Return root tree
    return node_trees[0]


def _verify_witness(witness: CompositionTree, target: Connective) -> bool:
    """
    Verify that a witness composition tree produces the target truth table.

    Args:
        witness: CompositionTree to verify
        target: Target connective

    Returns:
        True if witness is correct, False otherwise

    Raises:
        ValueError: If witness is invalid
    """
    num_inputs = target.arity

    # Check all input assignments
    for i in range(2 ** num_inputs):
        inp = tuple((i >> (num_inputs - 1 - k)) & 1 for k in range(num_inputs))

        # Evaluate witness and target
        witness_out = witness.evaluate(inp)
        target_out = target.evaluate(inp)

        if witness_out != target_out:
            raise ValueError(
                f"Witness failed for input {inp}: "
                f"witness={witness_out}, target={target_out}\n"
                f"Witness formula: {witness.to_formula()}"
            )

    return True


def is_definable_z3_sat(target: Connective, basis: List[Connective],
                         max_depth: int = 3, timeout_ms: int = 5000) -> Tuple[bool, Optional[CompositionTree]]:
    """
    Check if target is definable from basis using Z3 SAT encoding.

    Uses iterative deepening: tries depth 1, then 2, then 3, etc.
    Returns as soon as a witness is found.

    Args:
        target: Target connective to define
        basis: List of basis connectives
        max_depth: Maximum composition depth to try (default 3)
        timeout_ms: Timeout in milliseconds for each depth (default 5000)

    Returns:
        (True, witness) if target is definable, (False, None) otherwise
    """
    from z3 import sat, unsat, unknown

    # Iterative deepening
    for depth in range(1, max_depth + 1):
        try:
            # Build solver for this depth
            solver = Solver()
            solver.set("timeout", timeout_ms)

            # Build tree structure
            tree_struct = _build_tree_structure(depth)

            # Encode constraints
            choices = _encode_tree_choices(solver, tree_struct, basis)
            outputs = _encode_tree_outputs(solver, tree_struct, basis, target, choices)
            _encode_tree_structure(solver, tree_struct, basis, target, choices, outputs)
            _encode_target_match(solver, tree_struct, target, outputs)

            # Check satisfiability
            result = solver.check()

            if result == sat:
                # Extract witness
                model = solver.model()
                witness = _extract_witness_from_model(
                    model, tree_struct, basis, choices, target.arity
                )

                # Verify witness
                _verify_witness(witness, target)

                return (True, witness)

            elif result == unsat:
                # No composition at this depth, try deeper
                continue

            elif result == unknown:
                # Timeout or other issue - conservative False
                import logging
                logging.warning(
                    f"Z3 returned 'unknown' at depth {depth} for target {target.name} "
                    f"(timeout={timeout_ms}ms)"
                )
                continue

        except Exception as e:
            # Catch any Z3 errors and return conservative False
            import logging
            logging.error(
                f"Z3 error at depth {depth} for target {target.name}: {e}"
            )
            continue

    # No witness found at any depth
    return (False, None)
