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

    def test_goto_with_label(self):
        program_text = [
            "LET A 1",
            "GOTO TARGET",
            "ADD A 10",
            "TARGET: ADD A 5",
            "END",
            "ADD A 100"
        ]
        parsed = list(grin.parse(program_text))
        interpreter = grin.GrinInterpreter(parsed)
        interpreter.run()
        self.assertEqual(interpreter._vars["A"], 6)

    def test_goto_with_relative_integer(self):
        program_text = [
            "LET A 2",
            "GOTO 2",
            "ADD A 10",
            "ADD A 20",
            "END"
        ]
        parsed = list(grin.parse(program_text))
        interpreter = grin.GrinInterpreter(parsed)
        interpreter.run()
        self.assertEqual(interpreter._vars["A"], 22)

if __name__ == "__main__":
    unittest.main()