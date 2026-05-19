import grin
import sys


class GrinInterpreter:
    def __init__(self, parsed_lines):
        self._lines = parsed_lines
        self._pc = 0
        self._vars = {}
        self._labels = {}
        self._call_stack = []

        self._find_labels()

    def _find_labels(self):
        for index, tokens in enumerate(self._lines):
            if len(tokens) >= 2:
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

            start_idx = 0
            if (len(tokens) >= 2 and
                    tokens[0].kind() == grin.GrinTokenKind.IDENTIFIER and
                    tokens[1].kind() == grin.GrinTokenKind.COLON):
                start_idx = 2

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

                has_condition = False
                if len(tokens) > start_idx + 2:
                    if tokens[start_idx + 2].kind() == grin.GrinTokenKind.IF:
                        has_condition = True

                condition_met = True
                if has_condition:
                    left_val = self.get_value(tokens[start_idx + 3])
                    op_kind = tokens[start_idx + 4].kind()
                    right_val = self.get_value(tokens[start_idx + 5])

                    if op_kind == grin.GrinTokenKind.EQUAL:
                        condition_met = (left_val == right_val)
                    elif op_kind == grin.GrinTokenKind.NOT_EQUAL:
                        condition_met = (left_val != right_val)
                    elif op_kind == grin.GrinTokenKind.LESS_THAN:
                        condition_met = (left_val < right_val)
                    elif op_kind == grin.GrinTokenKind.LESS_THAN_OR_EQUAL:
                        condition_met = (left_val <= right_val)
                    elif op_kind == grin.GrinTokenKind.GREATER_THAN:
                        condition_met = (left_val > right_val)
                    elif op_kind == grin.GrinTokenKind.GREATER_THAN_OR_EQUAL:
                        condition_met = (left_val >= right_val)

                if condition_met:
                    target_kind = target_token.kind()
                    target_raw_val = target_token.value()

                    # First check if the identifier name matches a label directly
                    if isinstance(target_raw_val, str) and target_raw_val in self._labels:
                        self._pc = self._labels[target_raw_val]
                        continue

                    # Otherwise, evaluate dynamic variable lookups/integers
                    target_val = self.get_value(target_token)

                    if isinstance(target_val, str):
                        if target_val in self._labels:
                            self._pc = self._labels[target_val]
                            continue
                        else:
                            print(f"Runtime Error: Label '{target_val}' not found")
                            break
                    elif isinstance(target_val, int):
                        new_pc = self._pc + target_val
                        if 0 <= new_pc < len(self._lines):
                            self._pc = new_pc
                            continue
                        else:
                            print(f"Runtime Error: Jump target line {new_pc} out of bounds")
                            break
                else:
                    self._pc += 1
                    continue

            elif kind == grin.GrinTokenKind.GOSUB:
                target_token = tokens[start_idx + 1]

                has_condition = False
                if len(tokens) > start_idx + 2:
                    if tokens[start_idx + 2].kind() == grin.GrinTokenKind.IF:
                        has_condition = True

                condition_met = True
                if has_condition:
                    left_val = self.get_value(tokens[start_idx + 3])
                    op_kind = tokens[start_idx + 4].kind()
                    right_val = self.get_value(tokens[start_idx + 5])

                    if op_kind == grin.GrinTokenKind.EQUAL:
                        condition_met = (left_val == right_val)
                    elif op_kind == grin.GrinTokenKind.NOT_EQUAL:
                        condition_met = (left_val != right_val)
                    elif op_kind == grin.GrinTokenKind.LESS_THAN:
                        condition_met = (left_val < right_val)
                    elif op_kind == grin.GrinTokenKind.LESS_THAN_OR_EQUAL:
                        condition_met = (left_val <= right_val)
                    elif op_kind == grin.GrinTokenKind.GREATER_THAN:
                        condition_met = (left_val > right_val)
                    elif op_kind == grin.GrinTokenKind.GREATER_THAN_OR_EQUAL:
                        condition_met = (left_val >= right_val)

                if condition_met:
                    target_kind = target_token.kind()
                    target_raw_val = target_token.value()

                    if isinstance(target_raw_val, str) and target_raw_val in self._labels:
                        self._call_stack.append(self._pc + 1)
                        self._pc = self._labels[target_raw_val]
                        continue

                    target_val = self.get_value(target_token)

                    if isinstance(target_val, str):
                        if target_val in self._labels:
                            self._call_stack.append(self._pc + 1)
                            self._pc = self._labels[target_val]
                            continue
                        else:
                            print(f"Runtime Error: Label '{target_val}' not found")
                            break
                    elif isinstance(target_val, int):
                        new_pc = self._pc + target_val
                        if 0 <= new_pc < len(self._lines):
                            self._call_stack.append(self._pc + 1)
                            self._pc = new_pc
                            continue
                        else:
                            print(f"Runtime Error: Jump target line {new_pc} out of bounds")
                            break
                else:
                    self._pc += 1
                    continue

            elif kind == grin.GrinTokenKind.RETURN:
                if not self._call_stack:
                    print("Runtime Error: RETURN executed with an empty call stack")
                    break
                self._pc = self._call_stack.pop()
                continue

            elif kind == grin.GrinTokenKind.INNUM:
                target_var = tokens[start_idx + 1].value()
                try:
                    user_input = sys.stdin.readline().strip()
                    if '.' in user_input:
                        self._vars[target_var] = float(user_input)
                    else:
                        self._vars[target_var] = int(user_input)
                except ValueError:
                    print("Runtime Error: Invalid numeric input")
                    break
                self._pc += 1

            elif kind == grin.GrinTokenKind.INSTR:
                target_var = tokens[start_idx + 1].value()
                user_input = sys.stdin.readline().rstrip('\r\n')
                self._vars[target_var] = user_input
                self._pc += 1