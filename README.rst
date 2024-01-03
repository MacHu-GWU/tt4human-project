
.. image:: https://readthedocs.org/projects/tt4human/badge/?version=latest
    :target: https://tt4human.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/tt4human-project/workflows/CI/badge.svg
    :target: https://github.com/MacHu-GWU/tt4human-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/tt4human-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/tt4human-project

.. image:: https://img.shields.io/pypi/v/tt4human.svg
    :target: https://pypi.python.org/pypi/tt4human

.. image:: https://img.shields.io/pypi/l/tt4human.svg
    :target: https://pypi.python.org/pypi/tt4human

.. image:: https://img.shields.io/pypi/pyversions/tt4human.svg
    :target: https://pypi.python.org/pypi/tt4human

.. image:: https://img.shields.io/badge/Release_History!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/tt4human-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/tt4human-project

------

.. image:: https://img.shields.io/badge/Link-Document-blue.svg
    :target: https://tt4human.readthedocs.io/en/latest/

.. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://tt4human.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/tt4human-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/tt4human-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/tt4human-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/tt4human#files


Welcome to ``tt4human`` Documentation
==============================================================================
📔 See `Full Documentation HERE <https://tt4human.readthedocs.io/index.html>`_.

.. image:: https://tt4human.readthedocs.io/en/latest/_static/tt4human-logo.png

A `Truth Table <https://en.wikipedia.org/wiki/Truth_table>`_ is like a cheat sheet that helps us figure out if something is true or false based on certain **"conditions"**. We call a specific combination of conditions a **"case."** The outcome, whether it's true or false, is what we call the **"target."**

Imagine you're trying to decide whether or not you should go out. Two things could affect your decision: the weather and what time you wake up. So, in this situation, the weather and your wake-up time are the "conditions". When you combine these conditions, like if it's sunny and you woke up early, that combination is a "case." And the big question of whether you should go out or not is your "target." The Truth Table helps us organize all these cases and their outcomes to make decisions easier.

For example, we have two types of conditions: ``weather`` and ``get_up`` (when you get up). And we want to determine if you will go out. ``weather`` has two possible values: ``is_sunny`` and ``not_sunny``. ``get_up`` has three possible values: ``before_10``, ``10_to_2``, ``after_2``. Below is the truth table::

    weather     get_up      go_out
    is_sunny    before_10   1
    is_sunny    10_to_2     1
    is_sunny    after_2     0
    not_sunny   before_10   0
    not_sunny   10_to_2     0
    not_sunny   after_2     0

``tt4human`` provides some tools to work with Truth Table in Python.


.. _install:

Install
------------------------------------------------------------------------------

``tt4human`` is released on PyPI, so all you need is to:

.. code-block:: console

    $ pip install tt4human

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade tt4human
