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

if __name__ == "__main__":
    unittest.main()