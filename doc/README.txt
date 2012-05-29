babel-obviel
============

Babel Obviel integrates with the Babel_ i18n tools. You can then use
the Babel extraction system to extract message ids from Obviel
Template (``.obvt``) files. Babel Obviel knows about Obviel Template's
rules for message id generation so should generate message ids that
work with Obviel Template's i18n system.

You can configure Babel for JavaScript and ``.obvt`` files with a
mapping config file as follows::

  [javascript: **.js]
  extract_messages = _

  [obvt: **.obvt]

If you named this config file ``mapping.cfg``, you can run babel with
this config file like this::

  $ bin/pybabel extract -F mapping.cfg <some_directory>

.. _babel: http://babel.edgewall.org
