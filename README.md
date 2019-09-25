# Django Management Command Audit Log

App to enable simple auditing of Django management commands

## Background

This app wraps the standad Django management command base class to record the running of a command. It logs the name of the command, start and end time, and the output (if any). If the command fails with a Python exception, the error message is added to the record, and the exception itself is logged using `logging.exception`.

![Screenshot of admin list view](https://github.com/yunojuno/django-managment-command-log/blob/master/screenshots/detail-view.png")

![Screenshot of admin detail view](https://github.com/yunojuno/django-managment-command-log/blob/master/screenshots/detail-view.png")

See the `test_command` and `test_transaction_command` for examples.

## TODO

Documentation.
