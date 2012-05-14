Testing
=======

The tests are to be executed using `nosetests`

As some tests take lot of time, you can use `nosetests -a '!slow'` to avoid them
(this is useful especially when re-testing frequently)

Writing tests
=============

Just create a file called `test_xxx.py`, which contains classes called
`TestWhatever`.
Their methods follow conventions: `test_foo` is a test, `setUp` is a setup and
`tearDown` is a teardown

vim: set ft=markdown tw=80:
