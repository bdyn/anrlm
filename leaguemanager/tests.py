from django import test


class DummyTests(test.TestCase):

    def test_nothing(self):
        # Just here as a demonstration.
        self.assertEqual(1 + 1, 2)
