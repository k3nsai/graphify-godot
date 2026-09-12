"""GDScript extractor (Godot's scripting language).

Wires GDScript into graphify's shared generic tree-sitter engine via a
LanguageConfig. The ``tree_sitter_gdscript`` grammar declares
``function_definition`` and ``class_definition`` containers plus ``call`` /
``attribute_call`` nodes, but does not declare a ``function`` field on call
nodes and uses ``extends`` for inheritance -- so the generic engine's
language-agnostic fallbacks bind callee names (first named child) and dotted
member calls.

Node types observed in ``tree_sitter_gdscript``:
    source, class_name_statement, extends_statement, variable_statement,
    signal_statement, function_definition (+ parameters / body),
    class_definition (+ extends_statement / class_body), call, attribute_call,
    attribute, assignment, identifier, type.
"""
from __future__ import annotations

from pathlib import Path

from graphify.extractors.engine import _extract_generic
from graphify.extractors.models import LanguageConfig

_GDSCRIPT_CONFIG = LanguageConfig(
    ts_module="tree_sitter_gdscript",
    class_types=frozenset({"class_definition"}),
    function_types=frozenset({"function_definition"}),
    import_types=frozenset(),  # GDScript uses `extends` / preload, not imports
    call_types=frozenset({"call", "attribute_call"}),
    call_function_field="",  # no `function` field; generic fallback resolves callee
    call_accessor_node_types=frozenset({"attribute"}),
    function_boundary_types=frozenset({"function_definition", "class_definition"}),
)


def extract_gdscript(path: Path) -> dict:
    """Extract classes, methods, functions, and calls from a .gd file via tree-sitter AST."""
    return _extract_generic(path, _GDSCRIPT_CONFIG)
