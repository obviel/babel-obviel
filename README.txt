babel-obviel
============

Babel Obviel integrates Obviel_ with the Babel_ i18n tools. You can
then use the Babel extraction system to extract message ids from
Obviel Template (``.obvt``) files. Babel Obviel knows about Obviel
Template's rules for message id generation so should generate message
ids that work with Obviel Template's i18n system.

.. _Obviel: http://obviel.org

You can configure Babel for ``.js`` and ``.obvt`` files with a mapping
config file as follows::

  [javascript: **.js]
  extract_messages = _

  [obvt: **.obvt]

If you named this config file ``mapping.cfg``, you can run babel with
this config file like this::

  $ bin/pybabel extract -F mapping.cfg <some_directory>

You can also extract from a HTML file. The templates should be
embedded in script tags of type ``text/template`` like this::

  <html>
  <body>
    <script type="text/template" id="my_template">
       <p data-trans="">Hello world!</p>
    </script>
  </body>
  </html>

To enable this for all HTML files in your project, add this to your
configuration file::

  [obvt_html: **.html]

.. _babel: http://babel.edgewall.org
