Unstructured list of future improvements or corrections

TODO:
- [x] fix notebook 'titles' from '##' to '#' for exceptions and io.
- [ ] dedicated test module in jklab-core.
- [ ] manual/visual tests in older test notebooks.

MAYBE TODO:
- [cancelled] core/exceptions.py: introduce a '\n' at begin of warning message.

REVIEW:
- [ ] .vscode rep structure when introducing dedicated venvs for multiple
    packages. At the moment we'll leave one vscode folder at root level
    with dedicated details for each package venv.
    Then remove .vscode/ from .gitignore.