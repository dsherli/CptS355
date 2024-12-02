# CptS355

PostScript Interpreter README
# Overview
This project implements a simple PostScript Interpreter in Python. The interpreter supports a subset of PostScript commands and implements both dynamic and lexical scoping behaviors for variable lookups and definitions.

This README will guide you through the steps to build and run the interpreter, as well as explain the scoping mechanism and how it can be toggled.

# Features
Stack-based evaluation model (operand stack and dictionary stack).
Supports basic arithmetic operations (addition, subtraction, multiplication, etc.).
Allows variable definition and lookup with scoping behavior.
Supports dictionary manipulation, control structures (if statements, loops), and procedures.
Prerequisites
Python 3.x (recommended version: 3.7+).
No external dependencies required, all functionality is built in.
How to Build and Run
Clone or download the repository:

Clone via git:
git clone https://github.com/dsherli/CptS355/tree/Postscript-Interpreter
cd your-repository-folder
Run the interpreter:

To execute the PostScript interpreter, simply run the Python script:

python postscript_interpreter.py
The interpreter will execute the code as defined in the script. You can modify the postscript_interpreter.py to test various PostScript operations and scoping behaviors.

# Interactive Use (Optional):

To interact with the interpreter and explore its features interactively, you can modify the script to prompt for input or use Python's interactive shell.
How the Interpreter Works
The PostScript interpreter follows the standard PostScript conventions with the following components:

Operand Stack: A stack that holds values (numbers, strings, lists, etc.) during execution.
Dictionary Stack: A stack that holds dictionaries. Variables are defined and looked up in these dictionaries.
Scoping: There are two scoping modes that control how variables are resolved:
Dynamic Scoping: Variables are looked up in the most recently pushed dictionary. This mimics traditional programming language behavior where variable lookup checks the current execution context.
Lexical Scoping: Variables are looked up in the topmost dictionary (the global dictionary, or the first dictionary in the stack).
Scoping Behavior
Dynamic Scoping (Default)
In dynamic scoping, variable lookups are resolved by searching through the dictionary stack from top to bottom. This means the most recently added dictionary takes precedence when searching for a variable.
When you define a variable using def_(), it is added to the topmost dictionary in the dictionary stack.
Example:

interpreter.push(10)
interpreter.dict()
interpreter.begin()  # Adds a new dictionary
interpreter.push("/y")
interpreter.push(15)
interpreter.def_()  # Define y in the new dictionary
print("Defined y in new scope:", interpreter.lookup("y"))  # Expected: 15
In the above code, the variable y is defined in a new dictionary created by the begin() operation. Since dynamic scoping is enabled by default, the variable y can be looked up correctly from the dictionary stack.

# Lexical Scoping
Lexical scoping, in contrast, restricts variable lookups to the first dictionary in the stack. In other words, it always checks the global dictionary for variable definitions and ignores other dictionaries that were added later (using begin()).
This mimics how variables are resolved in many functional languages (e.g., Python).
To switch to lexical scoping, set the dynamic_scope attribute to False.

Example:

interpreter.dynamic_scope = False
try:
    print("Lexical scoping lookup for y:", interpreter.lookup("y"))  # Should raise KeyError
except KeyError as e:
    print("KeyError as expected under lexical scoping:", e)
In this example, even though y was defined in a nested scope (due to begin()), trying to access it after switching to lexical scoping will result in a KeyError, because lexical scoping ignores the inner scope and only checks the global dictionary.

Switching Between Dynamic and Lexical Scoping
To toggle between dynamic and lexical scoping, modify the dynamic_scope attribute:

Enable Dynamic Scoping:

interpreter.dynamic_scope = True
Enable Lexical Scoping:

interpreter.dynamic_scope = False
Once you change the scoping mode, any subsequent variable lookups will follow the selected scoping behavior.

# PostScript Commands Supported
Here is a list of key PostScript commands supported by the interpreter:

Arithmetic: add, sub, mul, div, mod, abs, neg, ceiling, floor, round, sqrt, idiv.
Boolean: eq, ne, ge, gt, le, lt, and_, or_, not_.
Control Structures: if_, ifelse, for_, repeat.
Dictionary Manipulation: dict, length, maxlength, begin, end, def_.
Stack Operations: push, pop, exch, count, dup, copy, clear.
Procedures: execute, define, lookup, quit.
Other: print_, true, false.
Example Scenarios
Working with Dictionaries:

Dictionaries can be created and manipulated using the dict command. You can define and lookup variables in the current dictionary scope using def_() and lookup().
Nested Scopes:

Use begin() and end() to create nested scopes. The scoping behavior can be toggled between dynamic and lexical scoping to test how variable lookups are affected.
Procedures:

Procedures can be defined using lists of PostScript code. The interpreter allows you to pass arguments, execute code blocks, and interact with the operand stack.
