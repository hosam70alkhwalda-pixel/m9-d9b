"""Learner-written tests for queries/warmups.py.

Tests run against the same Neo4j instance as the autograder, with the
drill fixtures already loaded via conftest.py's `driver` fixture.

Fixture facts sourced from data/recipes_mini.cypher:
  - 5 recipes total
  - 2 Italian recipes:  "Spaghetti Carbonara", "Margherita Pizza"
  - 1 direct-Chinese recipe: "Kung Pao Chicken"
  - 1 Sichuan recipe (Sichuan -[:SUBCLASS_OF]-> Chinese): "Mapo Tofu"
  - 1 Japanese recipe: "Sushi Platter"
"""

import pytest

from queries.warmups import q1_list_recipes, q2_filter_by_cuisine, q3_subclass_traversal


def test_q1_list_recipes_returns_all_five(driver):
    """q1_list_recipes() must return exactly 5 recipe names, one per node."""
    cypher = q1_list_recipes()
    with driver.session() as session:
        rows = [record["name"] for record in session.run(cypher)]

    assert len(rows) == 5, f"Expected 5 recipes, got {len(rows)}: {rows}"
    # Spot-check two known recipes from the fixture
    assert "Spaghetti Carbonara" in rows
    assert "Sushi Platter" in rows


def test_q3_traversal_picks_up_subclasses(driver):
    """q3_subclass_traversal('Chinese') must return both direct-Chinese and
    Sichuan recipes, while q2_filter_by_cuisine('Chinese') must return only
    the direct-Chinese ones — proving *0.. is doing hierarchy traversal.
    """
    cypher_q2, params_q2 = q2_filter_by_cuisine("Chinese")
    cypher_q3, params_q3 = q3_subclass_traversal("Chinese")

    with driver.session() as session:
        direct_names = {r["name"] for r in session.run(cypher_q2, params_q2)}
        traversal_names = {r["name"] for r in session.run(cypher_q3, params_q3)}

    # Sichuan is a sub-cuisine of Chinese; traversal must include it
    assert "Mapo Tofu" in traversal_names, (
        "q3 should include Sichuan recipe 'Mapo Tofu' via :SUBCLASS_OF"
    )
    # Direct filter must NOT include the Sichuan recipe
    assert "Mapo Tofu" not in direct_names, (
        "q2 should NOT include Sichuan recipe 'Mapo Tofu' — no hierarchy"
    )
    # Traversal is a strict superset of (or equal to) the direct filter
    assert direct_names.issubset(traversal_names), (
        "Every direct-Chinese recipe should also appear in the traversal result"
    )