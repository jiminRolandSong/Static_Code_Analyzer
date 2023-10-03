# write your code here
import re
import os
import sys
import ast


def one(name, line, index):
    if len(line) > 79:
        print("{}: Line {}: S001 Too long".format(name, index))


def two(name, line, index):
    blank = 0
    for c in line:
        if c == " ":
            blank += 1
        else:
            break
    if blank % 4 != 0:
        print("{}: Line {}: S002 Indentation is not a multiple of four;".format(name, index))


def three(name, line, index):
    code = line
    if '#' in line:
        list = line.split("#")
        code = list[0]
    string_catch = re.search("\'.+;\'", code) is None and re.search("\".+;\"", code) is None
    if ';' in code and string_catch:
        print("{}: Line {}: S003 Unnecessary semicolon".format(name, index))


def four(name, line, index):
    inline = re.search(".+#", line)
    regex = re.search(r'\s\s+#', line)
    if inline is not None and regex is None:
        print("{}: Line {}: S004 At least two spaces required before inline comments".format(name, index))


def five(name, line, index):
    low = line.lower()
    inline = re.search("#.*todo", low) is not None
    todo = "todo" in low
    string_catch = re.search("\'.?todo.?\'", low) is None and re.search("\".?todo.?\"", low) is None
    if todo and inline and string_catch:
        print("{}: Line {}: S005 TODO found".format(name, index))


def seven(name, line, index):
    line = line.lstrip()
    regex_c = re.search(r'class\s\s.+.+', line)
    regex_d = re.search(r'def\s\s+.+', line)
    if regex_c is not None:
        print("{}: Line {}: S007 Too many spaces after 'class'".format(name, index))
    elif regex_d is not None:
        print("{}: Line {}: S007 Too many spaces after 'def'".format(name, index))


def eight(name, line, index):
    line = line.lstrip()
    regex = re.search(r'class\s+[a-z].+', line)
    if regex is not None:
        class_name = line.split(" ")[1].replace(":\n", "")
        print("{}: Line {}: S008 Class name '{}' should use CamelCase".format(name, index, class_name))


def nine(name, line, index):
    line = line.lstrip()
    regex = re.search(r'.*def\s[A-Z].+', line)
    if regex is not None:
        def_name = line.split(" ")[1].replace("():\n", "")
        print("{}: Line {}: S009 Function name '{}' should use snake_case".format(name, index, def_name))


def printer(name, file, tree):
    index = 1
    line_blanks = 0

    for line in file:
        one(name, line, index)
        two(name, line, index)
        three(name, line, index)
        four(name, line, index)
        five(name, line, index)

        strip = line.strip()
        if strip != "" and index > 2 and line_blanks > 2:
            print("{}: Line {}: S006 More than two blank lines used before this line".format(name, index))
            line_blanks = 0
        elif strip == "":
            line_blanks += 1
        else:
            line_blanks = 0

        seven(name, line, index)
        eight(name, line, index)
        nine(name, line, index)

        index += 1

    nodes = ast.walk(tree)
    for node in nodes:
        if isinstance(node, ast.FunctionDef):
            args = [arg.arg for arg in node.args.args]
            for a in args:
                regex = re.match(r'[A-Z].*', a)
                if regex is not None:
                    print("{}: Line {}: S010 Argument name '{}' should be snake_case".format(name, node.lineno, a))
            for a in node.args.defaults:
                if isinstance(a, ast.List):
                    print("{}: Line {}: S012 Default argument value is mutable".format(name, node.lineno))
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            n = node.id
            regex = re.match(r'[A-Z].*', n)
            if regex is not None:
                print("{}: Line {}: S011 Variable '{}' in function should be snake_case".format(name, node.lineno, n))

    file.close()


args = sys.argv
file_name = args[1]
try:
    file = open(file_name, 'r')
    with open(file_name, 'r') as f:
        source_code = f.read()
    tree = ast.parse(source_code)
    printer(file_name, file, tree)
except PermissionError:
    files = os.listdir(file_name)
    for file in files:
        newname = file_name + "\\" + file
        opened = open(newname, 'r')
        with open(newname, 'r') as f:
            source_code = f.read()
        tree = ast.parse(source_code)
        printer(newname, opened, tree)
