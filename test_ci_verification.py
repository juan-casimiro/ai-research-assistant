import unittest


class CIVerificationTests(unittest.TestCase):
    """Temporary — JUA-97 verification that a failing test fails the
    required `build-and-test` check. Removed in the next commit."""

    def test_deliberately_fails(self):
        self.fail("JUA-97: deliberate failure to verify CI fails (do not merge)")


if __name__ == "__main__":
    unittest.main()
