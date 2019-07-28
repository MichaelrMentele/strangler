Strangler is a macro level tool to enable the 'strangling' of modules. Strangling is
the slow killing of modules. The intent is to strangle away the coupling of modules
and to create separation of concerns so you have the flexibility to manage them
orthogonally.

## Goals:
- simply describe and enforce incremental separation of concerns between modules
- allow for grandfathering of past invalid imports
- provides a simple interface for tracking progress and defining module boundaries

## Usecases
### Use Case 1: Enforcing one way imports
If a module defines an extension of some framework it is nice to be able to enforce that
extension does not export itself or couple itself in the reverse direction to
generic framework components. We can define this boundary as the entire module being
private.

### Use Case 2: Extracting services from a monolith
When a service or package starts out monolithic submodules can become unnecessarily
coupled due to cross imports creating unnecessary dependencies. Defining what is public
and grandfathering in violations can 1) ratchet down on further violations and
2) clarify the work remaining to decouple a module from a super module.

### Use Case 3: Preventing Abuse by Enforcing Information hiding and Boundaries
In general, it is useful to have APIs that pull down and hide information. By
defining explicitly what is public to a module to let consumers know how that
module is intended to be consumed preventing abuse and over amorous interactions
between modules.

## Use Demonstration: How to Strangle a Module
### As a Unit Test
```python
# in some config file at a location of your choosing, by default in cwd strangler/config.py

# When defining public submodules you can enter them in a few different ways
# Assumming that rootA has submodule{A,B} the following is valid:
# ['submoduleA', 'rootA.submoduleA']

# What would be invalid is if submoduleA was an ambiguous designator i.e.
# submoduleA existed elsewhere, so for this reason a full path (from the root)
# is required, but you need not include the root since this is implied

# What about blacklisting? That is, declaring something as private. What is
# private is inferred by what is public. The point of strangling something is
# to become clear about what is the interface, what should this module be
# exposing to the outside world? You could define this interface by defining
# a black list of what is invalid to export and in some cases it could be
# that this is the more concise description of the interface of your application.
#
#
# A -> B1 -> C
#            D
#   -> B2 -> E
#
# If I want B1 to be public but B1.C2 to be an exception and blacklisted from being
# exported from A, but I want it to be locally importable to other submodules in
# A then I can define A as public and define D as private. Alternatively, I could
# define D as private. And the rest is inferred. Now you could imagine this makes
# sense to do both for a larger more complciated example, where I want D to be
# private and I want B2 to be private, but I want B1 to be public.
interfaces_definition = {
  'rootA': {'private': [...], 'public': [...]}
  'rootA.rootB': {'private': [...], 'public': [...]}
}

# in a unit test like: test_module_interface_boundaries.py
from strangler import Strangler
# TODO: import the config

strangler = Strangler(interfaces_definition)

# You can decide to grandfather the violations when you record them which means
# you are whitelisting those violations. By default these are saved within
# strangler dir into a file that is named after the root module.
strangler.record_violations(grandfather=True)

# Searches for violations of the interface definition
strangler.find_interface_violations()

# raises an exception if any violations exist -- useful as a unittest
# if the violations are within the grandfather file, it excludes them
# if the violations are a subset of the grandfather file, the grandfather
# file will automatically be updated
to_strangle.enforce_interfaces()
```

## API Spec
```python
class Strangler:
  STRANGLER_DIR = os.getcwd()

  def __init__(self, interface_definitions: dict):
    if self.valid_interfaces(interface_definitions):
      self.interface_definitions = interface_definitions
    else:
      raise InvalidInterfaceDefinitions()

  def grandfather_violations(self):
    violations = self.find_interface_violations()
    self._save(violations)

  def find_interface_violations(self) -> list:
    '''
    Traverses the list of module roots in the interface definitions and
    searches for import patterns that violate those definitions.
    '''
    pass

  def enforce_interfaces(self):
    if len(self.find_interface_violations()) > 0:
      raise InterfaceViolation()
```

## Best Practices
This doesn't make sense:
{public: [], private: ['moduleA']}

Because private does not invalidate anything in the public space.

There is a general problem of what takes precedence, if public describes a supertree and private a super tree then you can blacklist that part of the tree, but what if the supertree is described as private and a subtree is described a public, is the reverse true? There needs to be a resolver that describes and matches up public and private based on specificity, or we can describe modules recursively.

We can have a list of rules. How about we simplify -- if it's public, it's whitelisted and you can privatize specific parts of something that is whitelisted. But you cannot declare something as private in a vacumn, it is private relative to some supernode which defaults to the root tree.

A module can have multiple interfaces defined. ('public pattern', exceptions)

This means you can specify the tree in multiple ways.

If there is no public pattern the whole tree is private.

## Extensions
- Atom/editor plugin that highlights strangled imports
