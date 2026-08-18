from calculator import add, multiply, subtract


def main():
    print("Simple Calculator")
    try:
        a = float(input("Enter first number: "))
        b = float(input("Enter second number: "))
    except ValueError:
        print("Please enter valid numbers.")
        return

    op = input("Enter '+' to add, '-' to subtract, or '*' to multiply: ").strip()
    if op == '+':
        print("Result:", add(a, b))
    elif op == '-':
        print("Result:", subtract(a, b))
    elif op == '*':
        print("Result:", multiply(a, b))
    else:
        print("Unknown operator. Use +, -, or *.")


if __name__ == "__main__":
    main()
