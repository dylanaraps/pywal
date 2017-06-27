# Contributing

Welcome to `pywal`, here's how you can contribute.


### Environment Details

- Linux
- Python `3.6`


### Development Dependencies

All contributions and changes to `wal` must pass both `flake8` and `pylint` linters unless you have ample reason for disabling a specific message. Travis.ci will automatically run the tests every time you push a new commit to a Pull Request on the repo.

```py
pip install flake8 pylint
```


### Tests

`wal` can be tested by running `python setup.py test` in the root directory of the repo.


### Commit Message Style

I'm not fussed if you don't follow this one too closely as I'm guilty of forgetting at times. The commit style that should be used on this repo is as follows:

```sh
# topic: Short sentence about changes. Closes #issue_number
# Example:
git commit -m "export: Added export format for emacs. Closes #11"
```


### Comment Style

All comments must start with a capital letter and end with a full stop `.`.


### Running `pywal`

You can run `pywal` without properly installing it by using the following command:

```sh
# From the repo directory.
python -m pywal
```

