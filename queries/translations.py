"""SPARQL -> Cypher Translation Task.

Each function returns a Cypher **string** whose executed result is
equivalent to the corresponding W9A SPARQL query. Equivalence is asserted
by the autograder as set-of-tuples equality on the named result columns,
ignoring row order.

Run against the books mini-graph in `data/books_kg.cypher`.
"""


def q1() -> str:
    """Q1 — Return all (book, title) pairs.

    SPARQL equivalent:
        SELECT ?book ?title WHERE { ?book a :Book ; :title ?title . }

    Cypher returns two columns: `book` (the Book's id string, e.g. 'book:1')
    and `title`. Result set on the fixture: 5 rows.
    """
    return "MATCH (b:Book) RETURN b.id AS book, b.title AS title"


def q2() -> str:
    """Q2 — Return (book, year) pairs for books published strictly after 2010.

    SPARQL equivalent:
        SELECT ?book ?year WHERE { ?book a :Book ; :year ?year .
                                   FILTER (?year > 2010) }

    Columns: `book` (id string), `year` (int). On the fixture: 1 row.
    """
    return (
        "MATCH (b:Book) "
        "WHERE b.year > 2010 "
        "RETURN b.id AS book, b.year AS year"
    )


def q3() -> str:
    """Q3 — Return all (book, author_name) pairs.

    SPARQL equivalent:
        SELECT ?book ?author_name WHERE {
            ?book a :Book ; :authored_by ?a .
            ?a :name ?author_name .
        }

    Books with multiple authors produce multiple rows. Columns: `book`
    (id string), `author_name` (the Author's name property).
    On the fixture: 7 rows.
    """
    return (
        "MATCH (b:Book)-[:AUTHORED_BY]->(a:Author) "
        "RETURN b.id AS book, a.name AS author_name"
    )


def q4() -> str:
    """Q4 — Return (book, topic) pairs with topic OPTIONAL.

    SPARQL equivalent:
        SELECT ?book ?topic WHERE {
            ?book a :Book .
            OPTIONAL { ?book :topic ?topic }
        }

    Every book appears; books with no topic edge get NULL for topic.
    Columns: `book` (id string), `topic` (string or NULL).
    On the fixture: 5 rows; book:2 has topic = NULL.

    Canonical source: the `topic` property on the :Book node is used
    (rather than the :ON_TOPIC relationship) because it maps directly to
    the SPARQL :topic literal triple and avoids a join that could produce
    duplicates if both sources coexist.
    """
    return (
        "MATCH (b:Book) "
        "RETURN b.id AS book, b.topic AS topic"
    )


def q5() -> str:
    """Q5 — Return TRUE iff any book has more than one distinct author.

    SPARQL equivalent:
        ASK { ?b :authored_by ?a1 ; :authored_by ?a2 . FILTER (?a1 != ?a2) }

    Cypher must return a single row with a single column named `result`
    (boolean). On the fixture: TRUE (book:1 and book:5 each have 2 authors).

    Strategy: use EXISTS { ... } with two distinct author nodes on the same
    book to match the SPARQL ASK pattern exactly.
    """
    return (
        "RETURN EXISTS { "
        "MATCH (b:Book)-[:AUTHORED_BY]->(a1:Author), "
        "(b)-[:AUTHORED_BY]->(a2:Author) "
        "WHERE a1 <> a2 "
        "} AS result"
    )