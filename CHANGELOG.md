# CHANGELOG

All notable changes to this project are documented in this file.

This changelog format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased](https://github.com/iamdefinitelyahuman/py-solc-ast)

## [1.2.5](https://github.com/iamdefinitelyahuman/py-solc-ast/releases/tag/v1.2.5) - 2020-08-07
### Fixed
- structs and enums as contract dependencies


## [1.2.4](https://github.com/iamdefinitelyahuman/py-solc-ast/releases/tag/v1.2.4) - 2020-04-21
### Fixed
- recursion errors with more complex circular dependencies

## [1.2.3](https://github.com/iamdefinitelyahuman/py-solc-ast/releases/tag/v1.2.3) - 2020-04-07
### Fixed
- recursion error when a contract has itself as a dependency

## [1.2.2](https://github.com/iamdefinitelyahuman/py-solc-ast/releases/tag/v1.2.2) - 2020-04-03
### Fixed
- missing dependencies for complex inheritance trees

## [1.2.1](https://github.com/iamdefinitelyahuman/py-solc-ast/releases/tag/v1.2.1) - 2020-03-09
### Fixed
- `NodeBase.get` exception when target is `dict`

## [1.2.0](https://github.com/iamdefinitelyahuman/py-solc-ast/releases/tag/v1.2.0) - 2020-03-09
### Added
- `NodeBase.get` method

## [1.1.0](https://github.com/iamdefinitelyahuman/py-solc-ast/releases/tag/v1.1.0) - 2019-11-22
### Added
- `from_ast` method to generate a single `SourceUnit`

### Fixed
- Ensure no mutation of original AST when generating node objects

## [1.0.2](https://github.com/iamdefinitelyahuman/py-solc-ast/releases/tag/v1.0.2) - 2019-09-30
### Fixed
- unlinked libraries not properly mapping as dependencies

## [1.0.1](https://github.com/iamdefinitelyahuman/py-solc-ast/releases/tag/v1.0.1) - 2019-09-19
### Changed
- Do not reduce `ExpressionStatement` to `Expression`

## [1.0.0](https://github.com/iamdefinitelyahuman/py-solc-ast/releases/tag/v1.0.0) - 2019-09-19
### Changed
- Streamlined code using metaclasses
- Attributes more consistent with original AST
- Require Python 3.6 or greater

## [0.1.4](https://github.com/iamdefinitelyahuman/py-solc-ast/releases/tag/v0.1.4) - 2019-07-27
### Fixed
- properly handle `NoneType` when expecting node

## [0.1.3](https://github.com/iamdefinitelyahuman/py-solc-ast/releases/tag/v0.1.3) - 2019-07-01
### Fixed
- `typeName` for array types

## [0.1.1](https://github.com/iamdefinitelyahuman/py-solc-ast/releases/tag/v0.1.1) - 2019-06-30
### Fixed
- allow empty statement blocks

## [0.1.0](https://github.com/iamdefinitelyahuman/py-solc-ast/releases/tag/v0.1.1) - 2019-06-30
- Initial release
