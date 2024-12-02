import math


class PostScriptInterpreter:
    def __init__(self, dynamic_scope=True):
        self.operand_stack = []  # The main stack
        self.dict_stack = [{}]  # Dictionary stack
        self.dynamic_scope = dynamic_scope  # Scoping flag

    def push(self, value):
        """Push value onto the operand stack."""
        self.operand_stack.append(value)

    def pop(self):
        """Pop value from the operand stack."""
        if not self.operand_stack:
            raise ValueError("Stack underflow")
        return self.operand_stack.pop()

    def define(self, name, value):
        """Define a variable in the top dictionary of the dictionary stack."""
        if self.dict_stack:
            self.dict_stack[-1][name] = value
        else:
            self.dict_stack.append({name: value})

    def lookup(self, key):
        """Lookup a variable in the dictionary stack."""
        if key.startswith("/"):
            key = key[1:]  # Remove the leading '/'
        if self.dynamic_scope:
            # Dynamic scoping: search from top to bottom
            for d in reversed(self.dict_stack):
                if key in d:
                    return d[key]
            raise KeyError(f"Name '{key}' not found")
        else:
            # Lexical scoping: search only in the topmost dictionary (current environment)
            if key in self.dict_stack[0]:
                dumb = self.dict_stack[0]
                return self.dict_stack[0][key]
            raise KeyError(f"Name '{key}' not found")

    def exch(self):
        """Exchange the top two elements on the operand stack."""
        if len(self.operand_stack) < 2:
            raise ValueError("Stack underflow")
        self.operand_stack[-1], self.operand_stack[-2] = (
            self.operand_stack[-2],
            self.operand_stack[-1],
        )

    def add(self):
        """Pop two numbers, push their sum."""
        b, a = self.pop(), self.pop()
        self.push(a + b)

    def sub(self):
        """Pop two numbers, push their difference."""
        b, a = self.pop(), self.pop()
        self.push(a - b)

    def div(self):
        """Pop two numbers, push their division."""
        b, a = self.pop(), self.pop()
        if b == 0:
            raise ValueError("Division by zero")
        self.push(a / b)

    def clear(self):
        """Clear the operand stack."""
        self.operand_stack = []

    def if_statement(self, condition, proc):
        """Execute a procedure if the condition is true."""
        if condition:
            self.execute(proc)

    def execute(self, code):
        """Execute a block of PostScript code."""
        for token in code:
            if isinstance(token, list):  # Procedure
                self.execute(token)
            elif callable(getattr(self, token, None)):
                getattr(self, token)()
            elif isinstance(token, str):
                if token.startswith("/"):  # Variable definition
                    name = token[1:]
                    value = self.operand_stack.pop()
                    self.define(name, value)
                else:
                    try:
                        resolved = self.lookup(token)
                        if isinstance(resolved, list):  # Procedure
                            self.execute(resolved)
                        else:
                            self.push(resolved)
                    except KeyError:
                        if callable(getattr(self, token, None)):
                            getattr(self, token)()
                        else:
                            self.push(token)
            elif isinstance(token, (int, float)):
                self.push(token)
            else:
                self.push(self.lookup(token))

    def count(self):
        """Push the number of elements in the operand stack onto the stack."""
        self.push(len(self.operand_stack))

    def dup(self):
        """Duplicate the top element of the operand stack."""
        if not self.operand_stack:
            raise ValueError("Stack underflow")
        self.push(self.operand_stack[-1])

    def copy(self):
        """Pop n from the stack and duplicate the top n elements."""
        if not self.operand_stack:
            raise ValueError("Stack underflow")
        n = self.pop()
        if not isinstance(n, int) or n < 0:
            raise ValueError("copy expects a non-negative integer")
        if n > len(self.operand_stack):
            raise ValueError("Not enough elements on the stack for copy")
        self.operand_stack.extend(self.operand_stack[-n:])

    def idiv(self):
        """Pop two numbers, push their integer division result."""
        b, a = self.pop(), self.pop()
        if b == 0:
            raise ValueError("Division by zero")
        self.push(a // b)  # Integer division

    def mul(self):
        """Pop two numbers, push their product."""
        b, a = self.pop(), self.pop()
        self.push(a * b)

    def mod(self):
        """Pop two numbers, push the remainder of their division."""
        b, a = self.pop(), self.pop()
        if b == 0:
            raise ValueError("Division by zero")
        self.push(a % b)

    def abs(self):
        """Pop a number, push its absolute value."""
        value = self.pop()
        self.push(abs(value))

    def neg(self):
        """Pop a number, push its negation."""
        value = self.pop()
        self.push(-value)

    def ceiling(self):
        """Pop a number, push the smallest integer greater than or equal to it."""
        value = self.pop()
        self.push(math.ceil(value))

    def floor(self):
        """Pop a number, push the largest integer less than or equal to it."""
        value = self.pop()
        self.push(math.floor(value))

    def round(self):
        """Pop a number, push the nearest integer."""
        value = self.pop()
        self.push(round(value))

    def sqrt(self):
        """Pop a number, push its square root."""
        value = self.pop()
        if value < 0:
            raise ValueError("Cannot compute square root of a negative number")
        self.push(math.sqrt(value))

    def dict(self):
        """Pop a number (size) from the stack and push an empty dictionary."""
        size = self.pop()
        if not isinstance(size, int) or size < 0:
            raise ValueError("dict expects a non-negative integer")
        self.push({})

    def length(self):
        """Pop a dictionary from the stack, push the number of key-value pairs."""
        d = self.pop()
        if not isinstance(d, dict):
            raise ValueError("length expects a dictionary")
        self.push(len(d))

    def maxlength(self):
        """Push the maximum number of elements that a dictionary can hold (unlimited in Python)."""
        self.push(
            float("inf")
        )  # Infinite since Python dictionaries have no fixed max length

    def begin(self):
        """Pop a dictionary from the stack and push it onto the dictionary stack."""
        d = self.pop()
        if not isinstance(d, dict):
            raise ValueError("begin expects a dictionary")
        self.dict_stack.append(d)

    def end(self):
        """Pop the top dictionary from the dictionary stack."""
        if len(self.dict_stack) == 1:
            raise ValueError("Cannot pop the base dictionary")
        self.dict_stack.pop()

    def def_(self):
        """Define a variable in the top dictionary of the dictionary stack."""
        value = self.pop()
        key = self.pop()
        if not isinstance(key, str):
            raise ValueError("def expects a string as the key")
        if key.startswith("/"):
            key = key[1:]  # Remove the leading '/'
        self.dict_stack[-1][key] = value

    def length(self):
        """Pop a string, list, or dictionary from the stack, push its length."""
        collection = self.pop()
        if isinstance(collection, (str, list, dict)):
            self.push(len(collection))
        else:
            raise ValueError("length expects a string, list, or dictionary")

    def get(self):
        """Pop an index and a string/list, push the element at the index."""
        index = self.pop()
        collection = self.pop()
        if not isinstance(collection, (str, list)):
            raise ValueError("get expects a string or list")
        if not isinstance(index, int):
            raise ValueError("get expects an integer index")
        if index < 0 or index >= len(collection):
            raise ValueError("Index out of range")
        self.push(collection[index])

    def getinterval(self):
        """Pop a start index, a count, and a string/list, push the sublist/substring."""
        count = self.pop()
        start = self.pop()
        collection = self.pop()
        if not isinstance(collection, (str, list)):
            raise ValueError("getinterval expects a string or list")
        if not all(isinstance(x, int) for x in [start, count]):
            raise ValueError("getinterval expects integer indices")
        if start < 0 or start + count > len(collection):
            raise ValueError("Range out of bounds")
        self.push(collection[start : start + count])

    def putinterval(self):
        """Pop a start index, a substring/sublist, and a string/list; modify the collection."""
        subcollection = self.pop()
        start = self.pop()
        collection = self.pop()
        if not isinstance(collection, (str, list)):
            raise ValueError("putinterval expects a string or list")
        if not isinstance(subcollection, (str, list)):
            raise ValueError(
                "putinterval expects a string or list as the subcollection"
            )
        if not isinstance(start, int):
            raise ValueError("putinterval expects an integer index")
        if start < 0 or start + len(subcollection) > len(collection):
            raise ValueError("Range out of bounds")

        # Modify the collection
        if isinstance(collection, list):
            collection[start : start + len(subcollection)] = subcollection
        elif isinstance(collection, str):
            # Strings are immutable; convert to a list and back
            temp = list(collection)
            temp[start : start + len(subcollection)] = subcollection
            collection = "".join(temp)

        self.push(collection)

    def eq(self):
        """Pop two values, push True if they are equal, else push False."""
        b = self.pop()
        a = self.pop()
        self.push(a == b)

    def ne(self):
        """Pop two values, push True if they are not equal, else push False."""
        b = self.pop()
        a = self.pop()
        self.push(a != b)

    def ge(self):
        """Pop two values, push True if the first is greater than or equal to the second."""
        b = self.pop()
        a = self.pop()
        self.push(a >= b)

    def gt(self):
        """Pop two values, push True if the first is greater than the second."""
        b = self.pop()
        a = self.pop()
        self.push(a > b)

    def le(self):
        """Pop two values, push True if the first is less than or equal to the second."""
        b = self.pop()
        a = self.pop()
        self.push(a <= b)

    def lt(self):
        """Pop two values, push True if the first is less than the second."""
        b = self.pop()
        a = self.pop()
        self.push(a < b)

    def and_(self):
        """Pop two values, push their logical AND result."""
        b = self.pop()
        a = self.pop()
        if not all(isinstance(x, bool) for x in [a, b]):
            raise ValueError("and expects boolean values")
        self.push(a and b)

    def not_(self):
        """Pop a value, push its logical NOT result."""
        a = self.pop()
        if not isinstance(a, bool):
            raise ValueError("not expects a boolean value")
        self.push(not a)

    def or_(self):
        """Pop two values, push their logical OR result."""
        b = self.pop()
        a = self.pop()
        if not all(isinstance(x, bool) for x in [a, b]):
            raise ValueError("or expects boolean values")
        self.push(a or b)

    def true(self):
        """Push True onto the stack."""
        self.push(True)

    def false(self):
        """Push False onto the stack."""
        self.push(False)

    def if_(self):
        """Pop a condition and two procedures (true and false branches), execute the appropriate one."""
        false_branch = self.pop()
        true_branch = self.pop()
        condition = self.pop()

        if condition:
            self.execute(true_branch)
        else:
            self.execute(false_branch)

    def ifelse(self):
        """Pop a condition and two procedures (true and false branches), execute the appropriate one."""
        false_branch = self.pop()
        true_branch = self.pop()
        condition = self.pop()

        if condition:
            self.execute(true_branch)
        else:
            self.execute(false_branch)

    def for_(self):
        """Pop a start value, end value, and a procedure, execute the procedure for each integer in the range."""
        proc = self.pop()
        end = self.pop()
        start = self.pop()

        if not isinstance(start, int) or not isinstance(end, int):
            raise ValueError("for expects integer start and end values")

        for i in range(start, end + 1):
            self.push(i)  # Push the current iteration value onto the stack
            self.execute(proc)  # Execute the procedure with the current value

    def repeat(self):
        """Pop a procedure and a count, repeat the procedure that many times."""
        count = self.pop()
        proc = self.pop()

        if not isinstance(count, int):
            raise ValueError("repeat expects an integer count")

        for _ in range(count):
            self.execute(proc)  # Execute the procedure for the specified count

    def quit(self):
        """Terminate the execution of the current procedure."""
        raise StopIteration("Execution terminated by quit")

    def print_(self):
        """Pop a value from the stack and print it."""
        value = self.pop()
        print(value)

    def equal(self):
        """Pop two values, push True if they are equal, else push False."""
        b = self.pop()
        a = self.pop()
        self.push(a == b)

    def double_equal(self):
        """Pop two values, push True if they are equal, else push False."""
        b = self.pop()
        a = self.pop()
        self.push(a == b)


# Demonstrating PostScript Interpreter with examples
interpreter = PostScriptInterpreter(dynamic_scope=True)

# Example 1: Working with dictionaries
interpreter.push(10)  # Push dictionary size
interpreter.dict()  # Create dictionary
interpreter.push("/x")  # Key for dictionary
interpreter.push(5)  # Value for key 'x'
interpreter.def_()  # Define in the current dictionary

# Confirm x is defined
print("Defined x (dynamic scope):", interpreter.lookup("x"))  # Expected: 5

# Example 2: Demonstrating dynamic scoping
interpreter.push(10)
interpreter.dict()
interpreter.begin()  # Add a new dictionary
interpreter.push("/y")
interpreter.push(15)
interpreter.def_()  # Define y in the new dictionary
interpreter.push("/x")
interpreter.push(20)
interpreter.def_()  # Define x in the new dictionary
print("Defined y in new scope:", interpreter.lookup("y"))  # Expected: 15

# Switch to lexical scoping
interpreter.dynamic_scope = False
try:
    print(
        "Lexical scoping lookup for y:", interpreter.lookup("y")
    )  # Should raise KeyError
except KeyError as e:
    print("KeyError as expected under lexical scoping:", e)

interpreter.dynamic_scope = True  # Switch back to dynamic scoping

# Example 3: Using functions and procedures
# Define the procedure with debug-friendly steps
add_proc = [
    "/a",
    "/b",  # Define variable 'a' (top of stack is its value)
    "a",
    "b",
    "add",
]
interpreter.define("add_numbers", add_proc)

# Provide values for 'a' and 'b'
interpreter.push(8)  # Value for 'b'
interpreter.push(7)  # Value for 'a' (due to 'exch')

# Execute the procedure
interpreter.execute(["add_numbers"])

# Output the result
print("Procedure result (8 + 7):", interpreter.pop())  # Expected: 15

# Example 4: Scoping example with nested dictionaries
interpreter.push(20)
interpreter.dict()
interpreter.begin()
interpreter.push("/z")
interpreter.push(25)
interpreter.def_()
print("Nested scope, defined z:", interpreter.lookup("z"))  # Expected: 25
interpreter.end()  # Pop the dictionary stack
try:
    print(interpreter.lookup("z"))  # Should raise KeyError
except KeyError as e:
    print("KeyError for z after popping scope:", e)
