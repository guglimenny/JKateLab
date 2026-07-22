======================================================================
# JKateLab_Software_Style_Guide.md
----------------------------------

# 0. Contents:

1. [Purpose](#1-purpose)
   - [1.1 Overview](#11-overview)
   - [1.2 Scope](#12-scope)
   - [1.3 Objectives](#13-objectives)
2. [Software architecture](#2-software-architecture)
   - [2.1 Component hierarchy](#21-component-hierarchy)
   - [2.2 Responsibilities](#22-responsibilities)
   - [2.3 Dependencies](#23-dependencies)
   - [2.3 Modularity](#24-modularity)
   - [2.3 Generalisation](#25-generalisation)
3. [Repository organisation](#3-repository-organisation)
   - [3.1 Repository philosophy](#31-repository-philosophy)
   - [3.2 Ecosystem structure](#32-ecosystem-structure)
   - [3.3 Repository structure](#33-repository-structure)
4. [Naming conventions](#4-naming-conventions)
   - [4.1 General principles](#41-general-principles)
   - [4.2 Repositories](#42-repositories)
   - [4.3 Packages](#43-packages)
   - [4.4 Modules](#44-modules)
   - [4.5 Functions](#45-functions)
   - [4.6 Classes](#46-classes)
   - [4.7 Variables](#47-variables)
   - [4.8 Constants](#48-constants)
   - [4.9 Exceptions](#49-exceptions)
   - [4.10 Type aliases](#410-type-aliases)
   - [4.11 File and directory names](#411-file-and-directory-names)
5. [Documentation standards](#5-documentation-standards)
   - [5.1 General philosophy](#51-general-philosophy)
   - [5.2 Documentation hierarchy](#52-documentation-hierarchy)
   - [5.3 Library documentation](#53-library-documentation)
   - [5.4 Module headers](#54-module-headers)
   - [5.5 Functions](#55-functions)
   - [5.6 Classes](#56-classes)
   - [5.7 Examples](#57-examples)
6. [Implementation guidelines](#6-implementation-guidelines)
   - [6.1 General philosophy](#61-general-philosophy)
   - [6.2 Module organisation](#62-module-organisation)
   - [6.3 Imports](#63-imports)
   - [6.4 Constants](#64-constants)
   - [6.5 Type aliases](#65-type-aliases)
   - [6.6 Functions](#66-functions)
   - [6.7 Classes](#67-classes)
   - [6.8 Exceptions](#68-exceptions)
   - [6.9 Type hints](#69-type-hints)
   - [6.10 Performance](#610-performance)
   - [6.11 Scientific programming](#611-scientific-programming)

======================================================================

# 1. Purpose

---

## 1.1 Overview

This guide defines the conventions adopted by the Python libraries 
developed under the JKateLab project.

Within this guide, a *library* is intended as a coherent collection
of related Python modules implementing a common set of
functionalities.

The guide establishes mandatory rules regarding software
organisation, naming conventions and coding style, while also
providing recommendations for implementation details and software
architecture.

---

## 1.2 Scope

The JKateLab ecosystem aims to provide reusable scientific software
organized into multiple abstraction layers according to their degree
of generality.

The abstraction layers are **Basic**, **Domain** and **Project**.

- **Basic** libraries provide domain-independent functionalities
  commonly required in scientific programming (e.g., input/output,
  random number generation, statistics, plotting, formatting,
  validation, etc.). These libraries should prioritize simplicity,
  modularity, long-term maintainability and API stability.
  Consequently, they should have a low refactoring tolerance.

- **Domain** libraries provide reusable frameworks for a specific
  scientific domain (e.g., molecular dynamics or Monte Carlo
  simulations). They should remain sufficiently modular to
  accommodate different algorithms, models or external components
  without requiring structural modifications.

- **Project** libraries are tailored to a specific research project
  or simulation code, typically with a strong focus on data analysis
  or workflow automation. They may intentionally adopt
  project-specific terminology, assumptions and constants whenever
  this improves readability and development efficiency.

As a general design principle, generality shall increase down the
dependency hierarchy:

    Basic
      ↑
    Domain
      ↑
    Project

Consequently, the lower a library sits in the hierarchy, the more
general, reusable, stable and carefully designed it should be.

---

## 1.3 Objectives

The main objectives of this guide are:

- establish a consistent software architecture across the JKateLab
  ecosystem;
- define naming conventions and coding standards;
- distinguish mandatory rules from recommended practices;
- encourage modular, reusable and maintainable software design;
- document the rationale behind important architectural decisions.

======================================================================

# 2. Software architecture

---

## 2.1 Component hierarchy

The JKateLab ecosystem is organised as a hierarchy of software
components.

In the context of this guide, the JKateLab ecosystem refers to the
Python software ecosystem developed under the JKateLab project. The
hierarchy and terminology defined in this section are therefore
intended primarily for the organisation of Python software.

The software components are defined as follows:

* **Ecosystem**: the complete collection of related libraries,
  packages, tools and supporting components developed under a common
  software project.

* **Library**: a coherent software component composed of one or more
  related packages, providing a reusable set of functionalities.

* **Package**: a coherent collection of related modules implementing a
  common set of functionalities.

* **Module**: a Python source file grouping classes, functions and
  constants related to the same concept.

* **Function**: a reusable implementation of a specific operation.

* **Class**: a definition of a well-defined concept together with its
  associated data and operations.

* **Constant**: a named value representing a fixed property or
  configuration parameter that is not intended to change during
  program execution.

The software hierarchy is therefore organised from the broadest
component to the most specific implementation component: the ecosystem
contains libraries, libraries contain packages, and packages contain
modules. Modules, in turn, contain classes, functions and constants.
Classes, functions and constants should not be considered strict
hierarchical levels, as they may be organised within modules according
to their implementation.

The component hierarchy is illustrated by the following tree:

```
JKateLab Python ecosystem
│
├── jklab-core library
│   ├── package 1
│   │   ├── module.py
│   │   └── ...
│   └── package 2
│       └── ...
│
├── jklab-md library
│   └── ...
│
└── jklab-qmep library
    └── ...
```

The hierarchy described above defines the organisation of the Python
software developed under JKateLab. The broader JKateLab project may
eventually include software written in other programming languages.
Language-specific software may be organised in separate repositories
for clarity and maintainability, while remaining part of the same
overall JKateLab ecosystem.

The separation of repositories by programming language does not imply
that future JKateLab components must be restricted to a single
language. Where appropriate, different language ecosystems may
interact, for example through a Python library providing an interface
to a high-performance C++ implementation.


---

## 2.2 Responsibilities

The fundamental structural rule of JKateLab is that every software
component shall own exactly one concept.

Owning a concept means being solely responsible for its
implementation. Other components may use that functionality but
shall not reimplement it.

Consequently, software components shall be designed to be as modular
and independent as reasonably possible.

Each component should expose the smallest public interface necessary
to fulfil its responsibilities.

---

## 2.3 Dependencies

Dependencies shall remain as limited as possible.

A software component shall only depend on the components required to
fulfil its own responsibilities.

Dependencies between libraries shall follow the abstraction
hierarchy defined in Section 1.

Modules within the same library shall avoid unnecessary imports and
shall not introduce circular dependencies.

---

## 2.4 Modularity

A module should represent a single, well-defined andself-consistent 
concept.

Whenever a module begins to implement multiple independent concepts,
it should be decomposed into multiple cooperating modules.

Large modules should result from the complexity of a single concept,
rather than from the accumulation of unrelated functionalities.

---

## 2.5 Generalisation

The JKateLab ecosystem aims to provide the most fundamental building
blocks possible for future software development.

Generalisation shall be driven by demonstrated reuse rather than by
speculation.

Whenever a functionality proves useful across multiple independent
libraries, it should be refactored into a more general module,
possibly belonging to a lower abstraction layer.

Premature generalisation should be avoided, as it often increases
complexity without providing practical benefits.

======================================================================

# 3. Repository organisation

---

## 3.1 Repository philosophy

The JKateLab Python ecosystem is organized as a collection of
independent Python libraries.

Each library shall be developed and distributed as an independent
repository. Consequently, every library shall have its own version,
documentation, tests and release cycle.

Dependencies between libraries shall follow the abstraction
hierarchy defined in Section 1.

The JKateLab ecosystem itself shall only define the common software
architecture and coding conventions adopted by all libraries.

---

## 3.2 Ecosystem structure

The JKateLab Python ecosystem structure shall be organized as follows:

    JKateLab/
    │
    ├── docs/
    │
    ├── jklab-core/
    ├── jklab-md/
    ├── jklab-qmep/
    │
    └── ...

The `docs/` directory contains documentation shared by the entire
ecosystem, including this Software Style Guide.

Each `jklab-*` directory corresponds to an independent software
library.

Additional libraries may be added to the ecosystem without
modifying the existing directory structure.

---

## 3.3 Repository structure

Every JKateLab repository shall follow the same directory layout.

    repository/
    │
    ├── README.md
    ├── LICENSE
    ├── pyproject.toml
    │
    ├── docs/
    ├── src/
    ├── tests/
    └── examples/

The purpose of each component is summarized below.

- `README.md` provides a general overview of the library.

- `LICENSE` defines the software license.

- `pyproject.toml` defines the package configuration and build
  system.

- `docs/` contains library-specific documentation.

- `src/` contains the library source code.

- `tests/` contains the library test suite. Tests may be provided
  either as automated scripts or as interactive notebooks for
  development and validation.

- `examples/` contains example scripts and notebooks illustrating
  the use of the library.

Using a common repository structure across all libraries improves
maintainability and allows developers to navigate different
repositories using the same conventions.

======================================================================

# 4. Naming conventions

---

## 4.1 General principles

The naming conventions adopted by the JKateLab Python ecosystem aim
to provide a clear, coherent and unambiguous public interface across
all libraries.

The following mandatory rules shall be respected:

1. Names shall describe clearly and synthetically the concept
   represented by the corresponding software component.

2. Names shall be sufficiently specific to uniquely identify the
   represented concept whenever practical.

3. The same concept shall always be referred to by the same name
   throughout the ecosystem.

The following recommendations should be followed whenever possible:

1. Prefer clarity over brevity.

2. Prefer established scientific terminology whenever applicable.
   In particular, scientific quantities should follow the notation
   commonly adopted in the corresponding literature.

3. Avoid abbreviations unless they belong to one of the accepted
   abbreviation categories defined below.

### Accepted abbreviations

Abbreviations are divided into three categories.

**General abbreviations** may be used throughout the ecosystem.

| Abbreviation | Meaning |
|--------------|---------|
| `api` | Application Programming Interface |
| `avg` | Average |
| `cfg` | Configuration |
| `idx` | Index |
| `io`  | Input/Output |
| `mc`  | Monte Carlo |
| `md`  | Molecular Dynamics |
| `max` | Maximum |
| `min` | Minimum |
| `num` | Number |
| `std` | Standard deviation |
| `txt` | Text |

**Domain abbreviations** correspond to widely accepted terminology
within a scientific field (e.g., `LJ`, `PBC`, `FFT`, `RDF`).

**Project abbreviations** are specific to a given project and may be
used only inside the corresponding library. Such abbreviations shall
be documented in the appropriate project guide.

---

## 4.2 Repositories

Repository names shall follow the convention

```
jklab-<library_name>
```

Examples:

```
jklab-core
jklab-md
jklab-qmep
```

Repository names shall:

- use lowercase letters only;
- separate words using hyphens (`-`);
- begin with the prefix `jklab-`.

---

## 4.3 Packages

All JKateLab Python packages belong to the common namespace

```python
jklab
```

Each library occupies the second namespace level.

Examples:

```python
import jklab.basic as jkba
import jklab.md as jkmd
import jklab.qmep as jkqm
```

The package aliases listed above are the official aliases adopted
throughout the ecosystem and should be preferred in all examples,
tests and library development.

Package names shall:

- use lowercase letters only;
- consist of a single descriptive word whenever possible.

---

## 4.4 Modules

A module represents one well-defined software concept and shall be
named accordingly.

Module names shall:

- use lowercase letters only;
- follow the `snake_case` convention when composed of multiple words;
- be nouns describing the module content.

Examples:

```
io.py
paths.py
statistics.py
plotting.py
particle.py
potential.py
```

Whenever possible, module names should remain concise while still
clearly identifying their purpose.

Module names belonging to different libraries may coincide whenever
they naturally represent the same concept.

---

## 4.5 Functions

Functions represent actions and shall therefore be named using action
verbs.

Function names shall:

- use the `snake_case` convention;
- begin with an action verb;
- identify both the performed action and the corresponding concept.

Examples:

```python
load_txt()
save_txt()

compute_energy()
compute_force()

build_neighbor_list()
find_neighbors()
```

Generic one-word function names should be avoided whenever a more
specific name can better describe the performed operation.

Example:

```python
potential_lennard_jones()
```

is preferred over

```python
potential()
```

---

## 4.6 Classes

Classes represent software entities and shall therefore be named as
nouns.

Class names shall:

- follow the `PascalCase` convention;
- begin with a capital letter.

Examples:

```python
Particle
NeighborList
SimulationBox
BatchHandle
```

---

## 4.7 Variables

Variable names shall follow the same general rules adopted for
functions.

Variables shall:

- use the `snake_case` convention;
- describe the represented quantity;
- place qualifiers after the corresponding concept.

Examples:

```python
pt_label
pt_idx
pt_num
pt_list
```

are preferred over

```python
label_pt
idx_pt
num_pt
list_pt
```

### Collection variables

Collections shall preserve the singular form of the represented
concept.

Examples:

```python
particle_list
particle_mat

pt_label_list
pt_force_mat
```

The plural form should not be used.

Examples:

```python
particles_list
pt_labels_list
```

The following suffixes are mandatory:

- `_list` : one-dimensional sequential containers;
- `_mat` : multidimensional numerical containers;
- `_dict` : dictionaries.

Additional suffixes (e.g., `_tuple`, `_set`) may be introduced
whenever they improve readability.

### Counting variables

Two naming conventions are distinguished.

Intrinsic quantities describing a software object shall use the
suffix `_num`.

Examples:

```python
particle_num
pt_num
rea_num
```

Temporary counting variables shall use the prefix `n_`.

Examples:

```python
n_steps
n_iter
n_trials
```

### Short variable names

Very short variable names should generally be avoided.

Exceptions are made for:

- universally accepted mathematical notation;
- loop indices;
- variables whose scope is very limited.

---

## 4.8 Constants

Constant names shall use uppercase letters only and separate words
using underscores.

Examples:

```python
DEFAULT_FONT_SIZE
DEFAULT_LINE_WIDTH

BOLTZMANN_CONSTANT
```

The same convention shall be used for module-wide, class-wide and
function-local constants.

---

## 4.9 Exceptions

Exception classes shall:

- follow the `PascalCase` convention;
- end with the suffix `Error`.

Examples:

```python
InvalidPathError
UnsupportedFormatError
MissingFieldError
```

The structure and formatting of exception messages are specified in
the Error Handling chapter.

---

## 4.10 Type aliases

Type aliases shall follow the same naming convention adopted for
classes.

Examples:

```python
PathLike
ArrayLike
VectorLike
```

---

## 4.11 File and directory names

Documentation files shall use descriptive names following the
`Pascal_Case.md` convention.

Examples:

```
User_Guide.md
API_Guide.md
Software_Style_Guide.md
```

Temporary files, notebooks and auxiliary scripts are not required to
follow these conventions but should remain consistent within each
project.

======================================================================

# 5. Documentation standards

---

## 5.1 General philosophy

The JKateLab Python ecosystem shall be provided with documentation
aimed at describing, contextualising and maintaining the software.

Documentation is organised into three hierarchical levels:

* **Ecosystem documentation**, describing the general principles,
  architecture and conventions adopted throughout the ecosystem.

* **Library documentation**, describing the objectives, functionalities
  and design choices of each library.

* **Module documentation**, describing the purpose and public interface
  of individual source files.

The documentation hierarchy is discussed in detail in Section 5.2.

### Mandatory rules

The following rules shall be respected throughout the ecosystem.

1. Public software components shall be documented through the
   appropriate documentation levels.

2. Documentation shall describe the purpose, scope and rationale of
   the documented component. Implementation details shall only be
   included when necessary to understand, maintain or extend the
   software.

3. Documentation shall remain synchronised with the corresponding code
   and shall be updated whenever the software is modified.

4. Documentation shall assume that the reader is familiar with the
   corresponding application domain, but not with the internal
   implementation of the software.

5. Documentation shall, whenever applicable, establish a clear
   correspondence between the scientific concepts, mathematical
   definitions and terminology used in the relevant literature and
   their representation in the code.

### Recommendations

The following recommendations should be followed whenever possible.

1. Documentation should be concise, coherent and well structured.

2. Documentation should provide sufficient context to understand the
   role of the documented component within the ecosystem.

3. Non-obvious implementation choices should be documented together
   with the rationale behind the adopted solution.

4. Documentation should avoid duplicating information already
   available at higher documentation levels. Each documentation level
   should complement, rather than repeat, the others.

---

## 5.2 Documentation hierarchy

Documentation shall be organised hierarchically, from the most
general to the most specific level. Each documentation level shall
assume that the information provided by the previous levels is
already known.

The documentation hierarchy adopted throughout the JKateLab
ecosystem is the following:

```text
Repository
    ↓
Library guide
    ↓
Module header
    ↓
Class docstring
    ↓
Function docstring
    ↓
Inline comments
```

The purpose of each documentation level is summarised below.

| Level | Purpose |
|-------|---------|
| **Repository** | General presentation of the project, installation instructions and repository-specific information. |
| **Library guide** | Objectives, architecture, public interface and design choices of the library. |
| **Module header** | Purpose of the module, dependencies and overview of the provided software components. |
| **Class docstring** | Description of the represented abstraction, its role and its main public interface. |
| **Function docstring** | Description of the function purpose, interface, parameters and returned values. |
| **Inline comments** | Local implementation notes intended to improve code readability. |

Each documentation level shall focus on its own level of
abstraction and shall avoid duplicating information already
available at higher levels. This hierarchy minimises duplicated
documentation while ensuring that each software component is
documented at the appropriate level.

---

## 5.3 Library documentation

Each library shall provide its own documentation describing its
objectives, architecture and public interface. Library
documentation complements the ecosystem documentation by providing
implementation-specific details while remaining consistent with the
general principles defined in this guide.

Within the current JKateLab repository, library documentation is
stored in the `docs/` directory.

Whenever possible, implementation questions should be answerable by
consulting the corresponding library documentation.

### Mandatory rules

The following rules shall be respected.

1. Each library shall provide its own documentation.

2. Library documentation shall describe the scope, objectives and
   design choices of the corresponding library.

3. Library documentation shall explicitly state both the internal
   and external dependencies required by the library.

4. Library documentation shall remain synchronised with the
   corresponding source code.

### Recommendations

The following recommendations should be followed whenever possible.

1. Library documentation should follow a common structure throughout
   the ecosystem.

2. The intended audience of the library should be clearly stated.

3. Usage examples should be provided whenever they improve the
   understanding of the library interface.

### Suggested structure

The following layout is recommended for all library guides.

```text
Overview

Objectives

Architecture

Dependencies

Modules

Public API

Examples

Notes
```

### Ecosystem index

The ecosystem documentation should provide an alphabetical index of
all available libraries together with a brief description of their
purpose. The index acts as the primary entry point for navigating
the JKateLab ecosystem.

---

## 5.4 Module headers

Each module shall begin with a standard header summarising its
purpose, public interface and implementation context.

The exact layout of the header is left to the official JKateLab
header template. Regardless of its visual appearance, every module
header shall contain the information specified below.

### Mandatory rules

The following rules shall be respected.

1. Every public module shall begin with a module header.

2. The module shall be identified by its package-relative path in the
   form

   ```text
   package/module.py
   ```

3. The module header shall contain the following information:

   * Module
   * Purpose
   * Dependencies
   * Public API
   * Implementation notes
   * References
   * Maintainer

4. The header shall document only the public interface of the module.
   Private helper functions and implementation details shall remain
   within the source code.

5. The header shall remain synchronised with the corresponding source
   code.

### Recommendations

The following recommendations should be followed whenever possible.

1. Dependencies should distinguish between internal JKateLab
   libraries and external packages whenever this improves clarity.

2. Implementation notes should briefly describe relevant implementation
   choices, technical constraints, assumptions or conventions whenever
   they are necessary to understand the code.

3. References to books, scientific publications or external
   documentation should be provided whenever they motivate the
   implementation, establish the scientific context or facilitate
   further study.

4. A `NOTE` section may be added whenever temporary information
   relevant to developers is present, such as known limitations,
   temporary workarounds, planned refactoring or incomplete
   implementations.

### Public API

The **Public API** section shall list all publicly exposed software
components provided by the module. Depending on the module, these may
include:

* classes;
* functions;
* constants;
* type aliases;
* other public objects.

Private software components shall not appear in the module header.

The official JKateLab module header template is provided separately
from this guide and shall be adopted consistently throughout the
ecosystem.

---

## 5.5 Functions

Functions implement a single well-defined operation. Every public
function shall begin with a docstring describing its purpose,
interface and usage.

The JKateLab ecosystem adopts the **NumPy docstring convention** for
all public functions.

### Mandatory rules

The following rules shall be respected.

1. Every public function shall begin with a docstring.

2. The docstring shall describe the purpose and scope of the
   function.

3. All input parameters shall be documented together with their

   - name;
   - type;
   - meaning;
   - expected units, where applicable;
   - expected shape, where applicable.

4. All returned values shall be documented together with their

   - type;
   - meaning;
   - shape, where applicable.

5. Public exceptions raised by the function shall be documented
   together with the conditions under which they may occur.

6. The docstring shall remain synchronised with the corresponding
   source code.

### Recommendations

The following recommendations should be followed whenever possible.

1. The docstring should describe the purpose of the function rather
   than its implementation.

2. Numerical assumptions, scientific conventions and implementation
   choices should be documented whenever they are necessary to
   correctly use the function.

3. Physical units, coordinate conventions and indexing conventions
   should be explicitly documented whenever applicable.

4. Short usage examples should be provided whenever they improve the
   understanding of the function interface.

5. References to scientific publications, textbooks or external
   documentation should be provided whenever they motivate the
   implementation or facilitate further study.

6. Function docstrings should assume that the context provided by
   the module header and the corresponding class documentation is
   already known and should avoid repeating such information.

### NumPy docstring convention

Public functions should follow the NumPy docstring convention,
including the following sections whenever applicable:

- Summary
- Parameters
- Returns
- Raises
- Notes
- References
- Examples

Additional sections may be included whenever they improve the
clarity of the documentation.

---

## 5.6 Classes

Every public class shall begin with a docstring describing the
software abstraction represented by the class.

### Mandatory rules

The following rules shall be respected.

1. Every public class shall begin with a docstring.

2. The docstring shall describe the purpose of the class and the
   abstraction it represents.

3. The docstring shall document the important attributes and public
   properties of the class whenever they are necessary to understand
   its role.

4. The class docstring shall remain synchronised with the
   corresponding source code.

### Recommendations

The following recommendations should be followed whenever possible.

1. Class docstrings should describe the represented abstraction
   rather than its implementation.

2. The class should be documented from the user's point of view
   rather than the developer's point of view.

3. Public methods should be documented individually. The class
   docstring should only describe the public interface when this
   significantly improves the understanding of the class.

4. Class docstrings should assume that the context provided by the
   module header is already known and should avoid repeating such
   information.

---

## 5.7 Inline comments

Inline comments are intended to improve code readability by
explaining decisions that cannot be inferred directly from the
source code.

Whenever possible, expressive names, modular functions and clear
software structure should be preferred over explanatory comments.

### Mandatory rules

The following rules shall be respected.

1. Inline comments shall explain the rationale behind the
   implementation rather than describing what the code does.

2. Comments shall remain synchronised with the corresponding source
   code.

3. Temporary workarounds, known limitations and implementation
   issues shall be documented through clearly identifiable comment
   tags.

### Recommendations

The following recommendations should be followed whenever possible.

1. Inline comments should explain non-obvious implementation
   choices, mathematical derivations or scientific conventions.

2. Performance-related implementation choices should be documented
   whenever they are not immediately evident from the code.

3. Long functions may be divided into logical sections through
   concise inline comments whenever this improves readability.

4. Comments should describe concepts rather than the relative
   position of the code (e.g., "the following line"), since the code
   structure may change over time.

5. Comments should avoid repeating information that is already
   evident from expressive variable names or function calls.

### Comment tags

The following comment tags are recommended throughout the JKateLab
ecosystem.

- `TODO:` Planned improvements or missing functionality.
- `FIXME:` Known bugs or incorrect behaviour requiring correction.
- `NOTE:` Important implementation information for developers.

---

## 5.8 Examples

The JKateLab Python ecosystem shall be provided with suitable
examples illustrating, contextualising and demonstrating the correct 
use of its libraries.

All examples shall be self-consistent and executable without
requiring external material not distributed with the corresponding
library.

Whenever example files are required, they should be organised into
dedicated `input/` and `output/` directories whenever appropriate.

Each library shall provide at least one complete example
demonstrating its intended use.

### Recommendations

The following recommendations should be followed whenever possible.

1. Examples should remain concise, readable and representative of
   realistic use cases.

2. Examples should progressively increase in complexity whenever
   multiple examples are provided.

3. Libraries belonging to the Basic abstraction layer should provide
   examples that remain as general and reusable as possible.

4. Libraries belonging to the Domain and Project abstraction layers
   should preferably provide examples based on realistic or real
   datasets distributed together with the library.

5. Examples should follow the naming conventions and programming
   practices defined throughout this guide.

======================================================================

# 6. Implementation guidelines

---

## 6.1 General philosophy

The JKateLab Python ecosystem aims at the development of a coherent,
modular and extensible scientific software library. Its objective is
not only to provide functional code, but also to establish sound
software engineering practices allowing the ecosystem to evolve
progressively towards a professional implementation.

To achieve this goal, the ecosystem shall enforce the following
principles.

0. **Correctness**. The primary objective of the JKateLab ecosystem is
   to produce scientifically correct and reproducible software.

   Scientific software is valuable only if its results are correct.
   Whenever behaviour is undefined, ambiguous or inconsistent, the
   code shall explicitly report the problem rather than silently
   producing an incorrect result.

   **Undefined behaviour is a bug.**

1. **Readability**. Code should be easy to read and understand by
   developers unfamiliar with its implementation.

   Readable code is easier to review, debug and extend. Layout,
   formatting and naming conventions should reduce cognitive load
   while remaining flexible enough to avoid local ambiguity.

   Layout conventions should normally be followed. However, local
   deviations are acceptable whenever they significantly improve
   readability.

2. **Consistency**. Similar concepts should be implemented in similar
   ways throughout the ecosystem.

   Consistency makes the library predictable. Developers should be
   able to infer how a component is implemented from previous
   experience with other parts of the ecosystem.

   When consistency is maintained, the correct implementation of a
   component should often be recognisable at first glance.

3. **Modularity**. Every software component should represent one
   well-defined concept and interact with other components through
   explicit interfaces.

   Modular software is easier to test, reuse and extend. Components
   should depend only on the information required to perform their
   own task.

   Components should be designed around the concepts they represent
   rather than the specific application in which they are currently
   used.

4. **Abstraction hierarchy**. The required level of generality
   increases with the abstraction layer, as shown:

   ```text
    Basic
      ↓
   Domain
      ↓
   Project
   ```

   The required degree of modularity and generality increases with
   the abstraction level.

   Basic libraries should provide reusable building blocks suitable
   for future libraries. Domain libraries should remain flexible
   within their scientific field. Project libraries may contain
   specialised implementations whenever justified by the application.

5. **Long-term maintainability**. Implementation decisions should
   minimise the need for future refactoring.

   JKateLab is intended to evolve over time. Clear interfaces,
   modular design and stable abstractions reduce maintenance effort
   as the ecosystem grows.

6. **Explicit interfaces**. Software components should communicate
   through explicit and meaningful interfaces.

   Functions and classes should require only the information
   necessary to perform their task. Dependencies should be visible
   from the public interface rather than hidden inside unrelated
   objects.

   Components should receive only the information required to perform
   their task, avoiding unnecessary coupling with higher-level
   abstractions.

7. **Performance**. Significant and well-established performance
   improvements should be adopted whenever they do not compromise
   correctness or maintainability.

   Scientific software must eventually scale to realistic problems.
   Whenever substantial performance gains are available, they should
   be preferred even if they require a more sophisticated
   implementation, provided that the code remains understandable
   through adequate documentation.

   Performance optimisations shall never compromise the correctness
   of the implementation.

8. **Professional scalability**. Whenever possible, implementations
   should remain compatible with a future professional
   implementation.

   Reference implementations may initially favour simplicity, but
   they should not prevent future extensions such as improved
   algorithms, additional features or higher-performance
   implementations.


---

## 6.2 Module organisation

Every module in the ecosystem shall follow a common internal
structure. The objective of this organisation is to standardise the
implementation of modules in order to improve readability,
maintainability and code navigation.

The order of the sections should reflect the natural progression
through the module, introducing concepts before the components that
depend on them. Sections which are not required for a specific module
may simply be omitted.

The suggested module structure is the following:

0. Header
1. Imports
2. Module constants
3. Functions
4. Classes

Functions and classes occupy the same abstraction level. Their order
may be exchanged whenever this improves the logical flow of the
module. In general, concepts should be introduced before the
components that depend on them.

Private helper functions and classes should be located close to the
public component that uses them whenever practical. Helpers shared by
multiple components should generally appear before the public
interface.

The visual structure of the source code should mirror its logical
structure. Consequently, modules should be visually divided into
sections and, whenever appropriate, into smaller implementation
blocks.

The following separators are recommended.

Major sections:

```python
# ============================================================================
# Section name
# ============================================================================
```

Intermediate blocks:

```python
# ---------------------------------------------------------------------------
# Block name
# ---------------------------------------------------------------------------
```

Implementation steps:

```python
# === Step name ===
```

Long sections should be divided into smaller logical blocks using the
appropriate separators. Each block should correspond to a well-defined
implementation step, allowing the reader to quickly identify the
overall structure of the code.


---

## 6.3 Imports

The import section shall be organised into three consecutive blocks:

1. Standard library modules;
2. Third-party modules;
3. Internal JKateLab modules.

Each block shall be arranged alphabetically and separated from the
following one by a single blank line.

Whenever applicable, external modules should be imported using their
universally recognised aliases in order to maintain consistency across
the scientific Python ecosystem.

Examples include:

```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy as sc
```

Internal modules shall be imported using absolute imports and aliased
according to the convention `jk...`, where the suffix is a concise and
meaningful abbreviation of the imported module.

Examples include:

```python
import jklab.basic.io as jkio
import jklab.basic.paths as jkpa
import jklab.basic.plotting as jkplot
```

Three- to four-letter abbreviations will generally provide a good
balance between brevity and readability, although longer
abbreviations are acceptable whenever they improve clarity.

The statement `from module import object` should be reserved for a
limited number of widely recognised objects whose origin is
immediately obvious or whose repeated qualification would unnecessarily
reduce readability. In all other cases, importing the whole module is
preferred in order to keep the origin of names explicit.

Wildcard imports (`from module import *`) shall never be used.

Absolute imports should be preferred over relative imports throughout
the ecosystem.

Example of the recommended import layout:

```python
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import jklab.core.io as jkio
import jklab.core.paths as jkpa
```


---

## 6.4 Constants

Constants represent immutable values shared within a module. They
should be defined at the beginning of the module, immediately after
the import section, and grouped according to their conceptual
purpose.

Module-wide constants shall be named using the `UPPER_SNAKE_CASE`
convention. Whenever possible, names should clearly describe the
meaning of the constant rather than only its numerical value.

Related constants should be grouped together and separated by
appropriate section comments. Typical groups include configuration
defaults, numerical tolerances and physical constants.

Magic numbers should be avoided throughout the ecosystem. Whenever a
numerical value has a specific meaning or is expected to be reused, it
should instead be defined as a named constant.

Constants should generally remain local to the module that uses them.
Only constants shared by multiple modules should be moved to a common
location.

Configuration constants whose purpose is immediately apparent from
their name generally do not require additional documentation.

Scientific constants, model parameters and convention-dependent
quantities should instead be accompanied by a concise comment
describing their physical meaning and, whenever applicable, the
adopted units or conventions.

Example:

```python
# ============================================================================
# Plot defaults
# ============================================================================

DEFAULT_FONT_SIZE = 18
DEFAULT_LINE_WIDTH = 2

# ============================================================================
# Physical constants
# ============================================================================

# Boltzmann constant (J K^-1)
BOLTZMANN_CONSTANT = 1.380649e-23

# Default Lennard-Jones cut-off radius (σ units)
DEFAULT_CUTOFF_RADIUS = 2.5
```


---

## 6.5 Type aliases

Type aliases provide meaningful names for commonly used or complex
types. Their primary objective is to improve readability,
consistency and maintainability by introducing a common vocabulary
throughout the ecosystem.

Type aliases should be used whenever they significantly simplify type
annotations or represent recurring concepts within a package. They
should not be introduced solely to rename primitive Python types.

Whenever possible, type aliases should be named descriptively.
However, since they often appear in function signatures and type
annotations, concise domain-specific abbreviations are acceptable
provided that their meaning is clearly documented where they are
defined.

The definition of a type alias should therefore be preceded by a
concise comment reporting its full meaning whenever the alias is not
immediately self-explanatory.

Examples:

```python
# Path to a local file or directory.
PathLike = str | pathlib.Path

# Particle position array.
PtPos = np.ndarray

# Mapping between observable names and measured values.
ObservableDict = dict[str, float]
```

Type aliases should become part of the conceptual vocabulary of the
ecosystem. Consequently, they should be reused consistently throughout
the codebase whenever the corresponding concept appears.


---

## 6.6 Functions

Functions are the fundamental building blocks of the JKateLab
ecosystem. They should encapsulate reusable scientific or
computational operations through explicit, stable and well-defined
interfaces.

The implementation of functions shall reflect the abstraction layer of
the package in which they are defined.

At the **Basic** layer, functions should provide generic and reusable
operations suitable for any present or future package of the
ecosystem.

At the **Domain** layer, functions should specialise these operations
to a particular scientific domain while preserving a high degree of
reusability.

At the **Project** layer, functions may be tailored to the
requirements, conventions and workflows of a specific project.

Functions should behave as compact software bricks, each performing a
single, well-defined task. Whenever a workflow naturally consists of
multiple independent operations, these should generally be implemented
as separate functions and composed together rather than merged into a
single implementation.

Example:

```text
Basic

load()
    ↓
filter()
    ↓
average()
    ↓
plot()

Project (QMEP)

qmep_load()
      ↓
qmep_filter()
      ↓
qmep_average()
      ↓
qmep_workflow()
```

Workflow functions should generally be avoided in the Basic layer,
where modularity and reusability take priority. Conversely, they are
encouraged at the Project layer, where they provide convenient access
to complete analysis pipelines while internally relying on reusable
building blocks.

Functions should represent reusable scientific or computational
operations rather than isolated implementation details. Consequently,
new functions should only be introduced when they define a meaningful
operation, improve readability, simplify maintenance or are expected
to be reused. Trivial wrappers around existing library functions
should generally be avoided.

Function interfaces should remain as stable as reasonably possible.
Input parameters should describe the information required by the
operation itself rather than the implementation currently using it.
Whenever new requirements arise, extending the abstraction through
additional wrappers or higher-level functions should generally be
preferred over continuously expanding existing interfaces.

Function parameters should require only the information necessary to
perform the requested operation. Their names should remain intuitive
within the abstraction level of the package. Generic names are
preferred in the Basic layer, whereas progressively more specialised
names are appropriate in the Domain and Project layers.

Whenever possible, functions should return their results explicitly
rather than modifying unrelated objects or global variables.
Unexpected side effects are forbidden throughout the ecosystem.

Private helper functions should encapsulate implementation details
that are not intended to form part of the module's public interface.
Such functions shall begin with a leading underscore (`_`) and should
remain compact and focused on a single task.

Functions should be sufficiently compact that their purpose and
behaviour can be understood without simultaneously reasoning about
multiple unrelated operations.

Any invalid, ambiguous or inconsistent situation shall raise an
appropriate exception rather than allowing execution to continue.
Warnings should be reserved for exceptional situations where the
computation remains valid but the user should nevertheless be informed
of potentially unexpected behaviour. Warnings should not be used as a
substitute for proper error handling.


---

## 6.7 Classes

Classes represent persistent software objects whose state and
behaviour naturally belong together. They should be introduced only
when they provide a clearer abstraction than an equivalent functional
implementation.

The implementation of classes shall follow the abstraction hierarchy
of the ecosystem.

At the **Basic** layer, classes should represent generic and reusable
objects suitable for any present or future package.

At the **Domain** layer, classes should specialise these objects to a
particular scientific domain while preserving a high degree of
reusability.

At the **Project** layer, classes may represent project-specific
objects, handles and data structures tailored to the corresponding
workflow.

Classes should model objects rather than procedures. Consequently,
they should primarily encapsulate state, while the operations acting
on that state should generally remain implemented as standalone
functions whenever they do not naturally belong to the object itself.

Methods should therefore operate primarily on the internal state of
their object. If a method does not meaningfully depend on the state of
the class, it should generally be implemented as a standalone
function.

Classes should remain lightweight and cohesive. They should contain
only the attributes required to represent their own abstraction.
Attributes that are meaningful only for specialised objects should not
be introduced in a more general class solely to accommodate future
extensions.

Whenever possible, constructors should only initialise a valid object.
Operations such as file loading, data processing or computational
workflows should instead be implemented as dedicated methods or
standalone functions.

When multiple classes share a substantial amount of common state,
composition should generally be preferred over inheritance.
Lightweight objects representing the shared state may be embedded
inside more specialised classes whenever this improves modularity and
maintainability.

Collections containing a very large number of equivalent entities
should generally favour data-oriented representations over collections
of Python objects. For example, in performance-critical scientific
applications, separate arrays storing positions, velocities and masses
are generally preferred over large lists of particle objects. This
approach improves memory locality, vectorisation and computational
performance while remaining consistent with the modular design of the
ecosystem.

Objects should always remain internally consistent. Invalid states
shall not be silently accepted, and inconsistent modifications should
raise appropriate exceptions whenever necessary.

Simple classes whose primary purpose is to store data should
preferably be implemented as dataclasses.

Temporary utility classes may be useful during development to organise
ideas or prototype interfaces. However, they should generally
disappear from the public implementation before release.

---

## 6.8 Exceptions

Exceptions are the standard mechanism used throughout the JKateLab
ecosystem to report invalid, ambiguous or inconsistent situations.
Whenever the assumptions required by an operation are violated,
execution shall fail explicitly rather than continuing with undefined
behaviour.

Invalid situations shall therefore raise an appropriate exception as
soon as they are detected. Input parameters, object states and other
critical assumptions should be validated early in the execution of a
function whenever this improves correctness and the clarity of error
messages.

Exceptions shall be chosen according to the nature of the problem.
Whenever possible, specific exception types (e.g., `ValueError`,
`TypeError` or `FileNotFoundError`) should be preferred over generic
exceptions.

Exception messages shall be clear, informative and sufficient to
identify the origin of the problem. Their formatting and content shall
follow the recommendations presented in Section 4.

Exceptions should only be intercepted when the program can perform a
meaningful recovery or provide additional contextual information.
Errors shall never be silently ignored, and exception handlers that
simply suppress failures without justification shall be avoided.

Warnings should be reserved exclusively for unusual situations where
the computation remains valid and the produced results are still
reliable. They shall not be used as a substitute for proper error
handling.

The JKateLab ecosystem follows a fail-fast philosophy. Whenever
correct execution cannot be guaranteed, terminating the computation
with an explicit exception is preferred over silently producing
potentially incorrect scientific results.

---

## 6.9 Type hints

Type hints should be used throughout the JKateLab ecosystem to
explicitly communicate the expected types of variables, function
arguments, return values and class attributes.

In the ideal implementation, all variables should be provided with
appropriate type hints, including local variables and variables used
within private functions. Type hints should nevertheless be introduced
with consideration for readability: they should not be forced when
their presence makes the code less clear or significantly increases
its complexity.

Type hints should be progressively completed during development and
testing. Before a component is considered ready for release, all
variables for which a meaningful and unambiguous type can be specified
should preferably be annotated.

Whenever a variable is expected to have a specific type, that type
should be explicitly indicated. Type hints should not be artificially
restricted when a variable legitimately accepts multiple unrelated
types or when such an annotation would reduce readability.

Commonly recurring combinations of types should be represented through
meaningful type aliases whenever this improves readability and
consistency. Type aliases should be introduced only when their use is
justified by repeated occurrence or by the conceptual meaning of the
type they represent. The ecosystem should avoid creating large numbers
of artificial aliases for types that are used only occasionally.

Type hints should document the expected interface of the code but do
not replace runtime validation. Functions and classes shall still
validate critical assumptions and raise appropriate exceptions when
invalid or inconsistent input is detected.

Type hints should be used consistently with the type aliases defined
in Section 6.5.


---

## 6.10 Performance

Performance is a fundamental objective of the JKateLab ecosystem.
Implementations should be developed with the long-term objective of
being capable of handling realistic scientific problems, potentially
including simulations executed on personal computers.

When the choice between correctness, performance and readability is
necessary, the following priority shall apply:

```text
Correctness
     ↓
Performance
     ↓
Readability
```

Correctness shall never be sacrificed for performance. However, when a
significant and well-established performance improvement conflicts with
code readability, performance may take precedence. In such cases, the
loss of readability should be compensated through appropriate
documentation in the module header, function docstrings and inline
comments.

Optimisation should be performed progressively. A simple initial
implementation may be developed first, followed by increasingly
optimised implementations as required. The modular structure of the
ecosystem should allow implementations to be replaced or improved
without requiring extensive modifications to unrelated components.

The initial implementation should, whenever reasonably possible, leave
open a clear path for future optimisation. Simplicity during early
development should therefore not unnecessarily constrain the
architecture of future, more efficient implementations.

The ecosystem should avoid premature micro-optimisation while
encouraging performance-conscious architectural decisions from the
beginning. In particular, fundamental choices concerning data
representation, algorithmic complexity and modular interfaces should
consider their potential impact on future performance.

The following recommendations should generally be followed whenever
applicable:

* **Prefer algorithmic optimisation over micro-optimisation.**
  Improvements to the computational complexity of an algorithm should
  generally be prioritised over optimisations of individual operations
  or lines of code.

* **Prefer vectorised operations for large numerical data.** When
  working with numerical arrays, operations provided by optimised
  numerical libraries should generally be preferred over equivalent
  Python-level loops.

* **Prefer data-oriented representations for large collections.**
  When large collections of homogeneous data are expected to scale
  significantly, a Structure-of-Arrays (SoA) representation should
  generally be preferred over an Array-of-Structures (AoS)
  representation when this improves memory locality, vectorisation or
  computational performance.

* **Avoid unnecessary data copies.** Large numerical data should not
  be copied unnecessarily, particularly inside performance-critical
  sections.

* **Avoid unnecessary memory allocations.** Repeated allocation of
  temporary objects or arrays inside performance-critical loops should
  generally be avoided when memory can safely be reused.

* **Move invariant computations outside performance-critical loops.**
  Quantities that do not change during an iterative computation should
  generally be calculated once and reused.

* **Follow established scientific-programming practices.** Whenever
  applicable, established recommendations from scientific-programming
  literature and well-established scientific software projects should
  be considered when designing performance-critical implementations.

* **Use profiling and benchmarking to guide optimisation.** Significant
  optimisation efforts should be based on measured performance rather
  than assumptions about the source of computational bottlenecks.

* **Preserve correctness during optimisation.** Optimised
  implementations must preserve the correctness and reproducibility
  of the original computation. Any approximation or numerical change
  introduced for performance reasons must be explicitly justified and
  documented.

* **Keep optimisations modular.** An optimised implementation should,
  whenever possible, replace or extend an existing component without
  unnecessarily modifying the interfaces of unrelated components.

The recommendations above are intended as strong guidance rather than
strict requirements. Their application should depend on the specific
problem, data structures and computational context. The list may be
extended as the ecosystem develops and new performance considerations
are encountered.


---

## 6.11 Scientific programming

The JKateLab ecosystem is intended for scientific programming.
Consequently, its implementations should follow established practices
for scientific software whenever applicable.

Scientific code should not be considered only as a collection of
computational operations. It should also provide a traceable
correspondence between the scientific problem, its mathematical
formulation and its computational implementation.

The documentation shall therefore act as a bridge between scientific
literature and code. Its purpose is to allow a reader to move from
papers to documentation to implementation without having to
independently reconstruct the correspondence between scientific
concepts, mathematical definitions and code components.

This correspondence should be established through the following
principles.

### Scientific context

Scientific modules and components should provide sufficient context to
explain the problem, model or physical system they represent.

Documentation should briefly describe the relevant scientific concepts
and, whenever appropriate, provide references to the literature on
which the implementation is based.

The level of context should be appropriate to the abstraction layer.
Basic components should generally focus on their mathematical or
computational purpose, while Domain and Project components should
provide the scientific context necessary to understand their specific
application.

### Scientific quantities and code variables

The correspondence between scientific quantities and their
representation in code should be explicit.

Whenever a variable, parameter or object represents a quantity defined
in scientific literature, the documentation should identify the
corresponding scientific terminology and, when relevant, the notation
used in the literature.

For example, documentation should make clear correspondences such as:

```text
Scientific terminology       Code representation
-------------------------------------------------
strain amplitude             epst
number of realisations       rea_num
period                       period
configuration                config_mat
```

Code-specific abbreviations or naming conventions should therefore be
mapped explicitly to the corresponding scientific terminology.

### Mathematical definitions and implementation

Important scientific quantities and operations should be documented
together with their relevant mathematical definitions whenever this
improves understanding.

The documentation should establish a clear correspondence between the
scientific definition, its mathematical formulation and the function,
class or variable implementing it.

For example:

```text
Scientific concept
        ↓
Mathematical definition
        ↓
Code quantity
        ↓
Implementation
```

This is particularly important for Domain and Project components,
where the relationship between the scientific model and the code is
central to the purpose of the implementation.

### Implementation deviations

Differences between the scientific definition described in the
literature and its implementation in code shall be explicitly
documented.

Such differences may arise from numerical approximations,
discretisation, finite-size effects, boundary conditions, normalisation
conventions, implementation constraints or other practical
considerations.

Whenever the implementation does not directly correspond to the
definition or procedure presented in the relevant scientific reference,
the documentation should state:

* the scientific definition or reference implementation;
* the JKateLab implementation;
* the nature of the difference;
* the reason for the difference, whenever known or relevant.

The purpose is to prevent apparently equivalent scientific quantities
from being assumed to be identical when their computational definitions
actually differ.

### Units and conventions

Scientific quantities should have their units and relevant conventions
documented whenever applicable.

Documentation should explicitly state, when relevant:

* physical units;
* reduced or dimensionless units;
* normalisation conventions;
* sign conventions;
* coordinate conventions;
* indexing conventions;
* boundary conditions;
* relevant numerical conventions.

Hidden or implicit conventions should be avoided whenever they may
affect the interpretation or reproducibility of scientific results.

### Scientific terminology

Scientific terminology should be used consistently throughout the
documentation.

When the terminology used in the code differs from that used in the
scientific literature, the correspondence should be explicitly stated.
Documentation should preferably use established scientific terminology
while clearly identifying the corresponding code-specific names.

### References

Scientific implementations based on published models, algorithms,
methods or definitions should provide appropriate references.

References should be included whenever they are necessary to identify
the scientific origin or justification of an implementation. When
appropriate, documentation should indicate which component or
definition is associated with each reference.

### Reproducibility

Documentation should provide the information necessary to understand
and, whenever reasonably possible, reproduce a scientific computation.

Depending on the abstraction level and purpose of the component, this
may include relevant parameters, initial conditions, random seeds,
numerical methods, boundary conditions, units and other computational
assumptions.

The level of reproducibility documentation should be proportional to
the role of the component. Domain and Project implementations should
provide sufficient information to reproduce or interpret the relevant
scientific results.

The overall objective of these principles is to establish a direct and
traceable path between scientific literature and computational
implementation:

```text
Scientific literature
        ↓
Scientific concept
        ↓
Mathematical definition
        ↓
JKateLab documentation
        ↓
Code implementation
```

A reader should therefore be able to move from papers to documentation
to code, and back from code to the relevant scientific concepts,
without having to independently reconstruct the mapping between them.


---

## 6.12 Deprecation and backward compatibility

The JKateLab Python ecosystem shall allow software components to evolve
while minimising unnecessary disruption to existing users and
applications.

Public interfaces should remain stable whenever reasonably possible.
Substantial changes to existing interfaces should be introduced
carefully and their impact on existing code should be considered before
implementation.

### Mandatory rules

The following rule shall be respected.

1. Any substantial modification to an existing public interface shall,
   whenever applicable, be tested against the tests associated with the
   previous interface.

   When a new interface extends an existing one, the existing tests
   shall continue to validate the behaviour provided by the previous
   interface, while additional tests shall be introduced to validate
   the new functionality.

   The resulting validation should therefore follow a nested structure:

   ```text
   Existing interface
          ↓
   Existing tests
          ↓
   New interface
       ↙     ↘
   Existing   New
    tests    tests
   ```

### Recommendations

The following recommendations should be followed whenever possible.

1. Breaking changes to public interfaces should be avoided unless
   justified by substantial improvements in correctness, performance,
   maintainability or functionality.

2. When a public interface is intended to be replaced, the previous
   interface should preferably be explicitly deprecated before being
   removed.

3. Deprecated interfaces should be clearly identified in the
   documentation and, whenever practical, a replacement or migration
   path should be provided.

4. Changes to public interfaces should be documented whenever they
   affect existing usage or require modifications to user code.

5. Private or internal implementation details may be modified without
   maintaining backward compatibility, provided that the public
   interface and its documented behaviour remain unchanged.

Backward compatibility should not be maintained at the expense of
scientific correctness. If an existing interface produces incorrect,
ambiguous or otherwise unacceptable behaviour, the interface should be
corrected even when doing so requires a breaking change.

---

## 6.13 Future-proofing

The JKateLab Python ecosystem shall be developed with the expectation
that its software will evolve over time.

Future-proofing does not mean predicting every possible future
requirement or implementing functionality before it is needed.
Instead, implementations should avoid unnecessarily restricting
reasonable future extensions.

The following principles should be followed whenever possible.

1. Implement the simplest solution that correctly addresses the
   current problem while preserving reasonable directions for future
   extension.

2. Prefer modular boundaries that allow individual components to be
   replaced, extended or optimised without requiring unrelated
   components to be substantially modified.

3. Avoid premature generalisation. General abstractions should be
   introduced when justified by demonstrated reuse or when they
   provide a clear architectural benefit.

4. Avoid implementation choices that unnecessarily couple a component
   to a specific implementation when the underlying concept is more
   general.

5. When multiple implementation levels are expected, develop them as
   progressively replaceable layers whenever practical. For example,
   a simple implementation may later be replaced by one or more
   increasingly optimised implementations without changing the
   surrounding interface.

6. Future-proofing should be achieved primarily through clear
   abstractions, modularity and stable interfaces rather than through
   speculative features or unnecessary complexity.

The guiding principle is therefore:

> **Do not predict the future, but do not unnecessarily close it.**

Future-proofing should remain subordinate to correctness, practicality
and development efficiency. The purpose is not to eliminate the need
for future refactoring, but to reduce unnecessary refactoring and
ensure that reasonable future improvements remain possible.

======================================================================

# 7. Testing guidelines

Testing is an essential part of software development within the
JKateLab Python ecosystem. Tests should provide confidence in the
correctness, performance and scientific validity of the implemented
software while remaining sufficiently flexible to accommodate the
requirements of individual projects and development stages.

Testing should not be unnecessarily constrained by rigid rules.
During development, tests may be implemented freely and adapted to
the specific problem under investigation. As the software matures,
useful and stable tests should progressively be standardised and
automated to reduce the effort required to validate future
modifications.

Three principal categories of testing are distinguished throughout
the JKateLab ecosystem:

* **Functionality testing**, which verifies that software behaves as
  intended and implements the expected operations correctly.

* **Performance testing**, which evaluates computational performance
  and may compare alternative implementations or configurations.

* **Scientific testing**, which verifies that scientific software
  reproduces expected physical or scientific behaviour.

These categories may require different testing procedures and
conventions. Detailed guidelines for each category may be developed
as the corresponding requirements emerge during the development of
the ecosystem.

## 7.1 General philosophy

Testing should be considered an integral part of software development
rather than a final validation step performed only before release.

Tests should be developed progressively alongside the corresponding
software. During early development, exploratory or temporary tests
may be used freely to verify that an implementation behaves as
expected. Once the implementation becomes sufficiently stable, useful
tests should be converted into reproducible and maintainable tests
whenever practical.

Testing should primarily aim to provide meaningful confidence in the
software rather than to satisfy arbitrary coverage or formal
requirements.

The testing process should therefore evolve progressively:

```text
Implementation
      ↓
Exploratory testing
      ↓
Validation of functionality
      ↓
Stable test implementation
      ↓
Standardisation and automation
      ↓
Efficient validation of future modifications
```

The long-term objective is to reduce the effort required to validate
future changes by developing standardised testing procedures and
reusable testing utilities.

Testing should remain subordinate to the purpose of the software.
The specific implementation of a test may therefore be adapted to
the problem being investigated, provided that the resulting test is
reproducible and provides meaningful information about the behaviour
being evaluated.

## 7.2 Test organisation

Tests shall be organised in a consistent manner throughout the
JKateLab Python ecosystem while remaining sufficiently flexible to
accommodate the different requirements of individual modules.

Test files shall be stored in the `tests/` directory of the
corresponding repository.

Whenever appropriate, each module should have a dedicated testing
notebook. The notebook should provide a single entry point for
executing the tests associated with the module and should be organised
so that the tests can be run from beginning to end.

Test data required for functionality testing should be provided with
the corresponding package whenever reasonably practical and without
introducing excessive storage requirements. This allows tests to be
reproduced immediately without requiring developers to generate or
locate data manually.

When appropriate, test data should be organised into dedicated
`input/` and `output/` directories.

* `input/` contains data required by tests, such as files used to test
  loading, processing or visualisation functionality.

* `output/` contains data generated by tests or used to verify the
  results produced by the software.

Small test datasets should be stored directly within the repository
whenever practical. Large datasets that would unnecessarily increase
the repository size may instead be provided through a dedicated
external data location associated with the GitHub repository.

Scientific test data originating from publications or other external
scientific sources shall always be accompanied by an explicit
reference to its original source. The reference should allow the
origin and scientific context of the data to be identified and, where
possible, independently accessed.

Test organisation should distinguish between the three principal
categories of testing adopted by the JKateLab ecosystem:

* **Functionality testing**, which verifies that software behaves as
  intended;
* **Performance testing**, which evaluates computational performance
  and compares alternative implementations or configurations;
* **Scientific testing**, which verifies that scientific software
  reproduces expected physical or scientific behaviour.

The specific implementation and organisation of tests may differ
between these categories and should be adapted to the purpose of the
test.

## 7.3 Test implementation and automation

Testing procedures should progressively evolve from exploratory
development tests into stable and reproducible automated tests.

During development, tests may be implemented in any form that allows
the developer to efficiently verify the behaviour of the software.
Such tests may be temporary and may be modified or discarded as the
implementation evolves.

Once a module becomes sufficiently stable, useful tests should
progressively be implemented in a standardised form suitable for
repeated execution.

The long-term objective is for each module to provide a dedicated
testing notebook that can be executed from beginning to end and
produce a clear summary of the tests performed and their results.

A complete test execution should ideally provide an immediate overview
of the validation status of the module, for example by identifying
which individual tests have passed or failed and whether the module as
a whole has passed the available tests.

Testing utilities should progressively be developed to support this
process and to provide common functionality for test execution,
result reporting and other recurring testing operations.

The exact structure and implementation of such testing utilities are
left open until sufficient experience has been gained through the
development of the ecosystem.

The intended long-term workflow is therefore:

```text
Modify module
      ↓
Reload package
      ↓
Run module test notebook
      ↓
Execute standardised tests
      ↓
Review test summary
```

This approach should allow future modifications to be validated
efficiently without requiring developers to manually reconstruct the
testing procedure for each module.

## 7.4 Performance testing

Performance testing evaluates the computational characteristics of
software and may be used to compare alternative implementations,
algorithms or configurations.

Performance testing should be performed whenever computational
efficiency is relevant to the intended use of the software.

Depending on the problem, performance may be evaluated through direct
timing, memory usage, scalability studies or comparisons between
alternative implementations.

Performance tests should be designed to provide meaningful
information about the behaviour being investigated rather than merely
producing isolated benchmark values.

Detailed conventions for performance testing may be developed as the
performance requirements of the JKateLab ecosystem become clearer.

## 7.5 Scientific testing

Scientific testing evaluates whether scientific software reproduces
the physical or scientific behaviour expected from the underlying
model.

Scientific tests may include comparisons with:

* analytical solutions;
* known limiting cases;
* conservation laws or other physical constraints;
* published simulation results;
* experimental or real-world data.

Scientific testing is expected to become increasingly important as
the scientific simulations developed within the JKateLab ecosystem
mature.

Detailed guidelines for scientific testing are intentionally left for
future development. Such guidelines should be developed alongside
the corresponding scientific applications and should reflect the
specific requirements of the physical models being investigated.

Scientific test data originating from external publications or
datasets should always be accompanied by an explicit reference to its
source, as specified in Section 7.2.

## 7.6 Regression testing

Regression testing aims to ensure that modifications to existing
software do not unintentionally alter previously validated behaviour.

Whenever existing functionality is substantially modified, previously
implemented tests should be rerun whenever applicable.

Regression testing is closely connected to the backward-compatibility
principles defined in Section 6.12. Existing tests should be retained
and reused whenever the corresponding functionality remains part of
the public interface.

As the automated testing infrastructure matures, more systematic
regression-testing procedures may be introduced.

## 7.7 Numerical testing

Numerical software may require specialised testing procedures to
account for floating-point arithmetic, numerical tolerances and
approximate equality.

Numerical results should not generally be validated through exact
equality when floating-point errors may affect the result.

Detailed guidelines for numerical testing, including the selection of
appropriate tolerances and the validation of numerical stability,
should be developed as the numerical requirements of the ecosystem
become clearer.

**TODO:** Develop specific guidelines for numerical testing,
including floating-point tolerances, approximate equality and
numerical stability.

## 7.8 Test coverage

Code coverage metrics may provide useful information about the extent
to which a test suite exercises the corresponding source code.

However, coverage alone does not guarantee correctness or meaningful
testing. High coverage may still be obtained through tests that do
not adequately validate the behaviour of the software.

The usefulness of coverage metrics within the JKateLab ecosystem
should therefore be evaluated as the automated testing infrastructure
matures.

**TODO:** Consider whether code coverage metrics provide sufficient
practical value to justify their adoption within the JKateLab testing
workflow.

## 7.9 Testing notebooks

Testing notebooks are recognised as an official development and
validation tool within the JKateLab Python ecosystem.

A testing notebook may provide an interactive environment for
developing, inspecting and validating tests associated with a module.

Whenever appropriate, each module should have a corresponding
testing notebook that provides a convenient entry point for executing
the available tests.

Testing notebooks should progressively evolve from exploratory
development tools into stable and reproducible test interfaces as the
corresponding software matures.

The existence and purpose of module testing notebooks should be
documented clearly enough that new developers can identify and use
them without requiring prior knowledge of the development workflow.

Testing notebooks should follow the general repository and naming
conventions defined throughout this guide.

The precise structure and automation of testing notebooks may evolve
alongside the development of the JKateLab testing utilities.

**TODO:** Establish a standard naming convention and repository
location for module testing notebooks once the automated testing
workflow has been implemented.


======================================================================