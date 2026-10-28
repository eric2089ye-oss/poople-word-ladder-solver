# Poople Word Ladder Solver

A small, deterministic four-letter word-ladder solver. Given a starting word (and an optional target), it returns the shortest path in the bundled dictionary, a progressive hint, or several shortest alternatives.

This is an independent, open-source utility. It is not the official Poople game, is not affiliated with poople.io, and does not publish or reproduce any official accepted-word list. Shortest paths are relative to the bundled dictionary version.

Live practice site: https://pooplegame.fun/ - a free daily Poople-style word ladder with a verified daily route, progressive hints, and this solver.

- Today's verified Poople answer (dated, source-checked): https://pooplegame.fun/answer/
- Poople Unlimited practice: https://pooplegame.fun/unlimited/

Live version of the tool: https://pooplegame.fun/word-ladder-solver/

## What it does

- Breadth-first search over a four-letter word graph. Every step changes exactly one letter and keeps a real word.
- Returns a single shortest path to a target word (default target: POOP).
- Computes the par (minimum number of moves) for any start word.
- Produces progressive hints: move count, one changed letter, then the first bridge word.
- Lists up to N alternative shortest paths.

## Quick start

No dependencies, Python 3.10 or newer.

    python3 solver.py ITEM
    python3 solver.py GENE --target POOP
    python3 solver.py CASH --json

Example output:

    ITEM: par=6
    path=ITEM -> STEM -> STEP -> STOP -> SLOP -> PLOP -> POOP
    hint=One shortest route changes letter 1 (the 'I') next.

Use it as a library:

    import solver

    words = solver.load_words()
    adj = solver.build_adj(words)
    path = solver.shortest_path('item', 'poop', adj=adj)
    hints = solver.hints_for('item', path)

## Dictionary and scope

The bundled list contains 2,347 four-letter English words selected from SCOWL 2020.12.07 and filtered by a project exclusion policy. It also includes a 1,576-word familiar bridge subset used by the live tool.

Version: scowl-2020.12.07-practice-84c372d0e87a

Important limits:

- Only four-letter words are supported.
- The dictionary is a maintained practice list, not an official game dictionary.
- A word accepted by another game may be missing here, and vice versa.
- The shortest path here is only the shortest path relative to this dictionary version.

## Repository layout

    solver.py              solver, hints and CLI
    data/words.json        versioned dictionary and familiar-word subset
    data/SCOWL-Copyright.txt  retained SCOWL license and notices
    data/dictionary-source.txt  source, release and provenance notes
    tests/test_solver.py   correctness checks with an independent oracle

Run the tests with:

    python3 -m unittest discover -s tests -p 'test_*.py'

## License

- Code in this repository is released under the MIT License; see LICENSE.
- The word list is derived from the SCOWL project and keeps its original notices; see data/SCOWL-Copyright.txt and data/dictionary-source.txt.

## Why it exists

The live site publishes verified daily routes and offers spoiler-controlled hints. This repository keeps the solver logic and the dictionary provenance reviewable outside the website build.

## Contact

Project email: support@pooplegame.fun (for corrections and partnership questions). No personal contact details are published.