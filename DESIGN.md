Goals:
- simply describe and enforce separation of concerns between modules
- supports
  - describing one way imports AKA disallowing exports of a module for example for a module that describes extensions of a framework
  - describing a modules public interface i.e. what is allowed to be exported
  - a grandfather file that whitelists specific imports that should be exceptions to a given import rule

Demonstration:
```python
from strangler import Boundary
to_strangle = Boundary(module_root, allowed_exports=[sub_modules, ...])
to_strangle.grandfather_violations() # w
to_strangle.enforce() # raises an import error if there are any violations of allowed_exports

# You can also define module interfaces as a dict
# Defining what is public will allow you to check that nothing that is NOT
# public is exported from the interfaces you defined for your modules

# Interfaces can be nested within interfaces i.e. you can define an interface
# for a submodule contained within another interface
interfaces = {
  'rootA': ['submoduleA', 'submoduleB'], # these submodules are public
  'rootB': ['rootA'] # the submodule rootA is public
  'rootC': [] # there is no public interface
  'rootD': ['rootD'] # this entire module is public
}

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

# What doesn't make sense is to define both public and what is private UNLESS
# you want to describe some submodule of a submodule that is entirely public
# but one part of which should be private. In this case, what is recommended
# is to just have that submodule be a root entry in your interfaces.

# Therefore, is never makes sense to BOTH describe what is public and
# what is private. Just describe your public interface or your black listed
# modules -- whichever is more concise and easy to understand

# It is assumed by default you are defining a public interface, you can
# define the interface inversely like so:
interfaces = {
  'rootA': {'private': True, 'submodules': [...]}
}

'''
I still don't understand, why can't I define what is public and what is private
for the same root module. To do this is unnecessarily complicated. We would
need to search for all the patterns you have defined, then cross reference
that with any intersecting patterns that touch black listed files.

A -> B1 -> C
           D
  -> B2 -> E

If I want B1 to be public but B1.C2 to be an exception and blacklisted from being
exported from A, but I want it to be locally importable to other submodules in
A then I can define A as public and define D as private. Alternatively, I could
define D as private. And the rest is inferred. Now you could imagine this makes
sense to do both for a larger more complciated example, where I want D to be
private and I want B2 to be private, but I want B1 to be public.
'''
```
