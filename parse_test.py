#!/usr/bin/env python3

import ast

def cppFromA(a):
    if isinstance(a, ast.Module):
        return cppFromModule(a)
    if isinstance(a, ast.Import):
        return 'import' + str(a)
    if isinstance(a, ast.Assign):
        return cppFromAssign(a)
    if isinstance(a, ast.Expr):
        return cppFromExpr(a)
    if isinstance(a, ast.Name):
        return a.id
    if isinstance(a, ast.FunctionDef):
        return cppFromFuncdef(a)

    else:
        return 'unknown: ' + str(a);

def cppFromFuncdef(funcdef):
    return ast.dump(funcdef)

def cppFromAssign(assign):

    if isinstance(assign.value, ast.Call) and assign.value.func.id == 'input':
        return cppFromInput(assign.targets)

    return ast.dump(assign)

def cppFromInput(vars):
    vids = [var.id for var in vars];

    lines = []
    lines += ['string ' + vid + ';' for vid in vids]
    lines += ['cin >> ' + '>>>'.join(vids) + ';']
    return '\n'.join(lines)

def cppFromModule(module):

    imports = [a for a in module.body if isinstance(a, ast.Import)]
    funcdefs = [a for a in module.body if isinstance(a, ast.FunctionDef)]
    rest = [a for a in module.body if a not in imports and a not in funcdefs]

    lines = []
    lines += [cppFromA(a) for a in imports + funcdefs]
    lines += ['int main() {']
    for r in rest:
        lines += ['  ' + x for x in cppFromA(r).split('\n')]
    lines += ['}']

    return '\n'.join(lines)

def cppFromExpr(expr):

    if isinstance(expr.value, ast.Call) and expr.value.func.id == 'print':
        return cppFromPrint(expr.value.args)

    return ast.dump(expr)

def cppFromPrint(args):
    return 'cout << ' + ' << '.join(cppFromA(a) for a in args) + ' <<< endl;'

with open('test.py') as f:
    tree = ast.parse(f.read())
    # print(ast.dump(tree))
    print(cppFromA(tree))