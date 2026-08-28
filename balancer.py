import re
from math import gcd
from functools import reduce
from sympy import Matrix

def parse_formula(formula):
    formula = formula.replace(" ", "").replace("·", ".")

    def parse_group(text):
        stack = [{}]
        i = 0

        while i < len(text):
            if text[i] == "(":
                stack.append({})
                i += 1
                continue

            if text[i] == ")":
                i += 1
                digits = ""

                while i < len(text) and text[i].isdigit():
                    digits += text[i]
                    i += 1

                multiplier = int(digits) if digits else 1

                if len(stack) == 1:
                    raise ValueError("Parentheses do not match.")

                group = stack.pop()

                for element, count in group.items():
                    current = stack[-1]
                    current[element] = current.get(element, 0) + count * multiplier

                continue

            if text[i].isupper():
                element = text[i]
                i += 1

                while i < len(text) and text[i].islower():
                    element += text[i]
                    i += 1

                digits = ""

                while i < len(text) and text[i].isdigit():
                    digits += text[i]
                    i += 1

                count = int(digits) if digits else 1

                current = stack[-1]
                current[element] = current.get(element, 0) + count
                continue

            raise ValueError(f"Cannot parse formula: {formula}")

        if len(stack) != 1:
            raise ValueError("Parentheses do not match.")

        return stack[0]

    total = {}

    for part in formula.split("."):
        match = re.match(r"^(\d+)(.*)$", part)

        if match:
            multiplier = int(match.group(1))
            part = match.group(2)
        else:
            multiplier = 1

        parsed = parse_group(part)

        for element, count in parsed.items():
            total[element] = total.get(element, 0) + count * multiplier

    return total


def simplify_coefficients(coefficients):
    coefficients = [abs(int(x)) for x in coefficients]
    common = reduce(gcd, coefficients)
    return [x // common for x in coefficients]


def balance_equation(equation):
    equation = equation.replace("→", "=").replace("->", "=")

    if "=" not in equation:
        raise ValueError("The equation requires the use of = or →.")

    if equation.count("=") != 1:
        raise ValueError("An equation may contain only one = or →.")

    left, right = equation.split("=")

    reactants = [x.strip() for x in left.split("+") if x.strip()]
    products = [x.strip() for x in right.split("+") if x.strip()]

    if not reactants:
        raise ValueError("Reactants must not be empty.")

    if not products:
        raise ValueError("Products must not be empty.")

    compounds = reactants + products
    compositions = []

    for compound in compounds:
        composition = parse_formula(compound)

        if not isinstance(composition, dict):
            raise ValueError(f"Invalid formula: {compound}")

        compositions.append(composition)

    elements = set()

    for composition in compositions:
        elements.update(composition.keys())

    elements = sorted(elements)

    matrix = []

    for element in elements:
        row = []

        for index, composition in enumerate(compositions):
            count = composition.get(element, 0)

            if index >= len(reactants):
                count = -count

            row.append(count)

        matrix.append(row)

    matrix = Matrix(matrix)
    nullspace = matrix.nullspace()

    if not nullspace:
        raise ValueError("This equation cannot be balanced.")

    solution = nullspace[0]

    lcm = 1

    for value in solution:
        denominator = value.q
        lcm = lcm * denominator // gcd(lcm, denominator)

    coefficients = [
        int(value * lcm)
        for value in solution
    ]

    coefficients = simplify_coefficients(coefficients)

    if any(value <= 0 for value in coefficients):
        raise ValueError("Unable to obtain valid positive integer coefficients.")

    left_result = []

    for coefficient, compound in zip(
        coefficients[:len(reactants)],
        reactants
    ):
        if coefficient == 1:
            left_result.append(compound)
        else:
            left_result.append(f"{coefficient}{compound}")

    right_result = []

    for coefficient, compound in zip(
        coefficients[len(reactants):],
        products
    ):
        if coefficient == 1:
            right_result.append(compound)
        else:
            right_result.append(f"{coefficient}{compound}")

    return " + ".join(left_result) + " → " + " + ".join(right_result)
