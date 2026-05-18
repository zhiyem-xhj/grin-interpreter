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

            else:
                self._pc += 1