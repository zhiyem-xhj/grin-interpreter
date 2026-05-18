import grin


class GrinInterpreter:
    def __init__(self, parsed_lines):
        self._lines = parsed_lines
        self._pc = 0
        self._vars = {}
        self._labels = {}

        # Pre-process lines to find and map labels
        self._find_labels()

    def _find_labels(self):
        """Scans the program lines to map labels to their instruction indices."""
        for index, tokens in enumerate(self._lines):
            if len(tokens) >= 2:
                # If a line starts with an IDENTIFIER followed by a COLON, it's a label
                if (tokens[0].kind() == grin.GrinTokenKind.IDENTIFIER and
                        tokens[1].kind() == grin.GrinTokenKind.COLON):
                    label_name = tokens[0].value()
                    self._labels[label_name] = index

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

            # Skip the label prefix if it exists to locate the actual statement keyword
            start_idx = 0
            if (len(tokens) >= 2 and
                    tokens[0].kind() == grin.GrinTokenKind.IDENTIFIER and
                    tokens[1].kind() == grin.GrinTokenKind.COLON):
                start_idx = 2

            # If there's no statement after the label, move on
            if start_idx >= len(tokens):
                self._pc += 1
                continue

            keyword_token = tokens[start_idx]
            kind = keyword_token.kind()

            if kind == grin.GrinTokenKind.LET:
                target_var = tokens[start_idx + 1].value()
                val_token = tokens[start_idx + 2]
                self._vars[target_var] = self.get_value(val_token)
                self._pc += 1

            elif kind == grin.GrinTokenKind.PRINT:
                val_token = tokens[start_idx + 1]
                print(self.get_value(val_token))
                self._pc += 1

            elif kind == grin.GrinTokenKind.ADD:
                target_var = tokens[start_idx + 1].value()
                current_val = self._vars.get(target_var, 0)
                operand_val = self.get_value(tokens[start_idx + 2])
                self._vars[target_var] = current_val + operand_val
                self._pc += 1

            elif kind == grin.GrinTokenKind.SUB:
                target_var = tokens[start_idx + 1].value()
                current_val = self._vars.get(target_var, 0)
                operand_val = self.get_value(tokens[start_idx + 2])
                self._vars[target_var] = current_val - operand_val
                self._pc += 1

            elif kind == grin.GrinTokenKind.MULT:
                target_var = tokens[start_idx + 1].value()
                current_val = self._vars.get(target_var, 0)
                operand_val = self.get_value(tokens[start_idx + 2])
                self._vars[target_var] = current_val * operand_val
                self._pc += 1

            elif kind == grin.GrinTokenKind.DIV:
                target_var = tokens[start_idx + 1].value()
                current_val = self._vars.get(target_var, 0)
                operand_val = self.get_value(tokens[start_idx + 2])

                if operand_val == 0:
                    print("Runtime Error: Division by zero")
                    break

                if isinstance(current_val, int) and isinstance(operand_val, int):
                    self._vars[target_var] = current_val // operand_val
                else:
                    self._vars[target_var] = current_val / operand_val
                self._pc += 1

            elif kind == grin.GrinTokenKind.END:
                break

            elif kind == grin.GrinTokenKind.GOTO:
                target_token = tokens[start_idx + 1]
                target_kind = target_token.kind()

                if target_kind == grin.GrinTokenKind.IDENTIFIER:
                    label_name = target_token.value()
                    if label_name in self._labels:
                        self._pc = self._labels[label_name]
                        continue
                    else:
                        print(f"Runtime Error: Label '{label_name}' not found")
                        break

                elif target_kind == grin.GrinTokenKind.LITERAL_INTEGER:
                    offset = target_token.value()
                    new_pc = self._pc + offset

                    if 0 <= new_pc < len(self._lines):
                        self._pc = new_pc
                        continue
                    else:
                        print(f"Runtime Error: Jump target line {new_pc} out of bounds")
                        break

                elif target_kind == grin.GrinTokenKind.LITERAL_STRING:
                    label_name = target_token.value()
                    if label_name in self._labels:
                        self._pc = self._labels[label_name]
                        continue
                    else:
                        print(f"Runtime Error: Label string '{label_name}' not found")
                        break

                self._pc += 1