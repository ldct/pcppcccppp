#!/usr/bin/env python3

import sys, ast

def cppFromA(a):
    if isinstance(a, ast.Module):
        return cppFromModule(a)
    elif isinstance(a, ast.Import):
        return 'import' + str(a)
    elif isinstance(a, ast.Assign):
        return cppFromAssign(a)
    elif isinstance(a, ast.Expr):
        return cppFromExpr(a)
    elif isinstance(a, ast.Name):
        return a.id
    elif isinstance(a, ast.FunctionDef):
        return cppFromFuncdef(a)
    elif isinstance(a, ast.Return):
        return cppFromReturn(a)
    elif isinstance(a, ast.Call):
        return cppFromCall(a)
    elif isinstance(a, ast.BinOp):
        return cppFromA(a.left) + " + " + cppFromA(a.right)
    else:
        return 'unknown: ' + str(a) + ast.dump(a)

def cppFromReturn(ret):
    return "return " + cppFromA(ret.value) + ";"

def cppFromCall(call):
    if call.func.id == 'print':
        return cppFromPrint(call.args)
    else:
        return "cppFromCall"


def cppFromTypeString(typeString):
    if typeString == "str":
        return "string"
    elif typeString == "int":
        return "int"

def cppFromArg(arg):
    argType = cppFromTypeString(arg.annotation.id)
    argName = arg.arg
    return " ".join([argType, argName])

def cppFromFuncdef(funcdef):

    returnType = cppFromTypeString(funcdef.returns.id)
    name = funcdef.name
    argList = (cppFromArg(arg) for arg in funcdef.args.args)

    body = [cppFromA(elem) for elem in funcdef.body]

    return returnType + " " + name + "(" + ', '.join(argList) + ")" + "{" + '\n'.join(body) + "}"

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
    return cppFromA(expr.value)

def cppFromPrint(args):
    return 'cout << ' + ' << '.join(cppFromA(a) for a in args) + ' <<< endl;'

tree = ast.parse(sys.stdin.read())
print(cppFromA(tree))