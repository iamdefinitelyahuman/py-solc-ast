# solc-ast

A tool for exploring the Solidity abstrax syntrax tree as generated by the [solc](https://github.com/ethereum/solidity) compiler.

## Installation

Clone the repo and use ``setuptools``:

```bash
$ python setup.py install
```

## Usage

First, use [py-solc-x](https://github.com/iamdefinitelyahuman/py-solc-x) to compile your contracts to the [standard JSON output format](https://solidity.readthedocs.io/en/latest/using-the-compiler.html#output-description).

```python
>>> import json
>>> import solcx
>>> input_json = json.load(open('input.json'))
>>> output_json = solcx.compile_standard(input_json)
```

Next, import ``solcast`` and initialize using ``from_standard_output_json`` or ``from_standard_output``. This returns a list of ``SourceUnit`` objects, which each represent the base node in a Solidity AST.

```python
>>> import solcast
>>> nodes = solcast.from_standard_output(output_json)
```

From the initial objects, you can explore the AST:

```python
>>> nodes
[<SourceUnit iterable object 'contracts/Token.sol'>]
>>> s = nodes[0]
>>> s
<SourceUnit iterable object 'contracts/Token.sol'>

>>> s.keys()
['children', 'contract_id', 'contracts', 'depth', 'keys', 'name', 'node_type', 'offset', 'parent', 'path', 'value']

>>> s.contracts
[<ContractDefinition iterable 'Token'>]

>>> s[0]
<ContractDefinition iterable 'Token'>

>>> s['Token']
<ContractDefinition iterable 'Token'>

>>> s['Token'].keys()
['children', 'contract_id', 'depth', 'functions', 'keys', 'name', 'node_class', 'node_type', 'offset', 'parent', 'value']

>>> s['Token'].functions
[<FunctionDefinition iterable '<constructor>'>, <FunctionDefinition iterable '<fallback>'>, <FunctionDefinition iterable 'balanceOf'>, <FunctionDefinition iterable 'allowance'>, <FunctionDefinition iterable 'approve'>, <FunctionDefinition iterable 'transfer'>, <FunctionDefinition iterable 'transferFrom'>]

>>> s['Token']['transfer']
<FunctionDefinition iterable 'transfer'>

>>> s['Token']['transfer'].statements
[<ExpressionStatement.FunctionCall 'require(balances[msg.sender] >= _value, Insufficient Balance)'>, <ExpressionStatement.Assignment iterable uint256 'balances[msg.sender] = balances[msg.sender].sub(_value)'>, <ExpressionStatement.Assignment iterable uint256 'balances[_to] = balances[_to].add(_value)'>, <EmitStatement.FunctionCall 'Transfer'>, <Return.Literal bool 'true'>]
```

Use the ``Node.children`` and ``Node.parents`` methods to access and filter related nodes:

```python
>>> node = s['Token']['transfer']

>>> node.children(depth=1)
[<ExpressionStatement.FunctionCall 'require(balances[msg.sender] >= _value, Insufficient Balance)'>, <ExpressionStatement.Assignment iterable uint256 'balances[msg.sender] = balances[msg.sender].sub(_value)'>, <ExpressionStatement.Assignment iterable uint256 'balances[_to] = balances[_to].add(_value)'>, <EmitStatement.FunctionCall 'Transfer'>, <Return.Literal bool 'true'>]

>>> node.children(include_children=False, filters={'node_type': "FunctionCall", 'name': "require"})
[<ExpressionStatement.FunctionCall 'require(balances[msg.sender] >= _value, Insufficient Balance)'>]

>>> node.parents()
[<ContractDefinition iterable 'Token'>, <SourceUnit iterable object 'contracts/Token.sol'>]
```

Calling ``help`` on either of these methods provides a more detailed explanation of their functionality.

## Development

This project is still in development and should be considered an early alpha. All feedback and contributions are welcomed!

Not all nodes have been implemented yet. From any object, you can use the ``Node._unimplemented`` method to get a list of keys that contain AST nodes that have not yet been included. The raw json data is stored at ``Node._node``.

```python
>>> s['Token']['transfer']._unimplemented()
['parameters', 'returnParameters']

>>> s['Token']['transfer']._node['returnParameters']
{'id': 328, 'nodeType': 'ParameterList', 'parameters': [{'constant': False, 'id': 327, 'name': '', 'nodeType': 'VariableDeclaration', 'scope': 373, 'src': '1573:4:2', 'stateVariable': False, 'storageLocation': 'default', 'typeDescriptions': {'typeIdentifier': 't_bool', 'typeString': 'bool'}, 'typeName': {'id': 326, 'name': 'bool', 'nodeType': 'ElementaryTypeName', 'src': '1573:4:2', 'typeDescriptions': {'typeIdentifier': 't_bool', 'typeString': 'bool'}}, 'value': None, 'visibility': 'internal'}], 'src': '1572:6:2'}
```

See the Solidity documentation for information about the [AST grammar](https://solidity.readthedocs.io/en/latest/miscellaneous.html#language-grammar).

## License

This project is licensed under the [MIT license](LICENSE).
