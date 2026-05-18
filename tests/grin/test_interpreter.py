import unittest
import grin

class TestGrinInterpreterArithmetic(unittest.TestCase):
    def test_math_operations(self):
        program_text = [
            "LET A 10",
            "ADD A 5",
            "SUB A 2",
            "MULT A 3",
            "DIV A 2"
        ]
        parsed = list(grin.parse(program_text))
        interpreter = grin.GrinInterpreter(parsed)
        interpreter.run()
        self.assertEqual(interpreter._vars["A"], 19)

    def test_labels_are_skipped(self):
        program_text = [
            "START: LET A 5",
            "NEXT: ADD A 3"
        ]
        parsed = list(grin.parse(program_text))
        interpreter = grin.GrinInterpreter(parsed)
        interpreter.run()
        self.assertEqual(interpreter._vars["A"], 8)
        self.assertEqual(interpreter._labels["START"], 0)
        self.assertEqual(interpreter._labels["NEXT"], 1)

if __name__ == "__main__":
    unittest.main()