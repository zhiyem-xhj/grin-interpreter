import grin


class GrinInterpreter:
    def __init__(self, parsed_lines):
        self._lines = parsed_lines
        self._pc = 0
        self._vars = {}

    def get_value(self, token):
        if token.kind() == grin.GrinTokenKind.IDENTIFIER:
            return self._vars.get(token.value(), 0)
        return token.value()

    def run(self):
        while self._pc < len(self._lines):
            tokens = self._lines[self._pc]

            if not tokens:
                self._pc += 1
                continue

            keyword_token = tokens[0]
            kind = keyword_token.kind()

            if kind == grin.GrinTokenKind.LET:
                target_var = tokens[1].value()
                val_token = tokens[2]
                self._vars[target_var] = self.get_value(val_token)
                self._pc += 1

            elif kind == grin.GrinTokenKind.PRINT:
                val_token = tokens[1]
                print(self.get_value(val_token))
                self._pc += 1

            elif kind == grin.GrinTokenKind.ADD:
                target_var = tokens[1].value()
                current_val = self._vars.get(target_var, 0)
                operand_val = self.get_value(tokens[2])
                self._vars[target_var] = current_val + operand_val
                self._pc += 1

            elif kind == grin.GrinTokenKind.SUB:
                target_var = tokens[1].value()
                current_val = self._vars.get(target_var, 0)
                operand_val = self.get_value(tokens[2])
                self._vars[target_var] = current_val - operand_val
                self._pc += 1

            elif kind == grin.GrinTokenKind.MULT:
                target_var = tokens[1].value()
                current_val = self._vars.get(target_var, 0)
                operand_val = self.get_value(tokens[2])
                self._vars[target_var] = current_val * operand_val
                self._pc += 1

            elif kind == grin.GrinTokenKind.DIV:
                target_var = tokens[1].value()
                current_val = self._vars.get(target_var, 0)
                operand_val = self.get_value(tokens[2])

                if operand_val == 0:
                    print("Runtime Error: Division by zero")
                    break

                if isinstance(current_val, int) and isinstance(operand_val, int):
                    self._vars[target_var] = current_val // operand_val
                else:
                    self._vars[target_var] = current_val / operand_val
                self._pc += 1

            else:
                self._pc += 1