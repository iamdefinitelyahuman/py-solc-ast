#!/usr/bin/python3

# This list is incomplete - feel free to add to it and open a pull request
# https://solidity.readthedocs.io/en/latest/miscellaneous.html#language-grammar

BASE_NODE_TYPES = {
    "ContractPart": [
        "StateVariableDeclaration",
        "UsingForDeclaration",
        "StructDefinition",
        "ModifierDefinition",
        "FunctionDefinition",
        "EventDefinition",
        "EnumDefinition",
    ],
    "Statement": [
        "IfStatement",
        "WhileStatement",
        "ForStatement",
        "InlineAssemblyStatement",
        "DoWhileStatement",
        "PlaceholderStatement",
        "Continue",
        "Break",
        "Return",
        "Throw",
        "EmitStatement",
        "SimpleStatement",
    ],
    "PrimaryExpression": [
        "BooleanLiteral",
        "NumberLiteral",
        "HexLiteral",
        "StringLiteral",
        "TupleExpression",
        "Identifier",
        "ElementaryTypeNameExpression",
    ],
    "Expression": [
        "BinaryOperation",
        "UnaryOperation",
        "Assignment",
        "Conditional",
        "VariableDeclaration",
        "NewExpression",
        "IndexAccess",
        "MemberAccess",
        "FunctionCall",
    ],
    "TypeName": [
        "ElementaryTypeName",
        "UserDefinedTypeName",
        "Mapping",
        "ArrayTypeName",
        "FunctionTypeName",
    ],
}
