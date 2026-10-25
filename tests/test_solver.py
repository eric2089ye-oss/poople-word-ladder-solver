"""Solver correctness checks with an independent distance oracle."""
import sys
import unittest
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import solver


class SolverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.words = solver.load_words(ROOT / "data" / "words.json")
        cls.adj = solver.build_adj(cls.words)
        # Independent implementation: plain BFS over every word pair.
        cls.distances = {"poop": 0}
        queue = deque(["poop"])
        while queue:
            current = queue.popleft()
            for candidate in cls.words:
                if candidate not in cls.distances and sum(
                    a != b for a, b in zip(current, candidate)
                ) == 1:
                    cls.distances[candidate] = cls.distances[current] + 1
                    queue.append(candidate)

    def assert_valid_path(self, path, start, end="poop"):
        self.assertEqual(path[0], start)
        self.assertEqual(path[-1], end)
        self.assertTrue(all(word in self.words for word in path))
        self.assertTrue(all(sum(a != b for a, b in zip(left, right)) == 1
                            for left, right in zip(path, path[1:])))

    def test_every_word_has_declared_distance(self):
        self.assertGreaterEqual(len(self.words), 2000)
        self.assertEqual(set(self.distances), self.words)

    def test_shortest_path_matches_oracle(self):
        for start in sorted(self.words)[:200]:
            path = solver.shortest_path(start, adj=self.adj)
            self.assertIsNotNone(path, start)
            self.assert_valid_path(path, start)
            self.assertEqual(len(path) - 1, self.distances[start], start)

    def test_examples(self):
        path = solver.shortest_path("item", "poop", adj=self.adj)
        self.assert_valid_path(path, "item")
        self.assertEqual(len(path) - 1, 6)
        self.assertIsNone(solver.shortest_path("zzzz", adj=self.adj))

    def test_hints(self):
        path = solver.shortest_path("item", adj=self.adj)
        hints = solver.hints_for("item", path)
        self.assertEqual(hints["par"], 6)
        self.assertIn("letter", hints["position_hint"])
        self.assertIn(hints["bridge_word"], path)

    def test_all_shortest_paths(self):
        paths = solver.all_shortest_paths("item", adj=self.adj, cap=4)
        self.assertGreaterEqual(len(paths), 1)
        for path in paths:
            self.assertEqual(len(path) - 1, 6)
            self.assert_valid_path(path, "item")


if __name__ == "__main__":
    unittest.main()
