=============
pytest-tytest
=============

.. image:: https://img.shields.io/pypi/v/pytest-tytest.svg
    :target: https://pypi.org/project/pytest-tytest
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-tytest.svg
    :target: https://pypi.org/project/pytest-tytest
    :alt: Python versions

.. image:: https://travis-ci.org/mbranko/pytest-tytest.svg?branch=master
    :target: https://travis-ci.org/mbranko/pytest-tytest
    :alt: See Build Status on Travis CI

.. image:: https://ci.appveyor.com/api/projects/status/github/mbranko/pytest-tytest?branch=master
    :target: https://ci.appveyor.com/project/mbranko/pytest-tytest/branch/master
    :alt: See Build Status on AppVeyor


Typhoon HIL plugin for pytest
=============================


Features
--------

* specify test parameters in a python module
* reference them in `pytest.mark.parametrize` decorators
* mark tests as Jira+Xray issues
* send test reports directly to Xray using Xray's REST API


Requirements
------------

* pytest 5+
* pytz, tzlocal
* requests 2.23+


Installation
------------

You can install "pytest-tytest" via `pip`_ from `PyPI`_::

    $ pip install pytest-tytest


Usage
-----

Put credentials needed to access Jira and Xray in environment variables or a
file.

* `XRAY_HOST`: Xray URL, defaults to `https://xray.cloud.xpand-it.com`
* `XRAY_CLIENT_ID`: Client ID of your Xray API key
* `XRAY_CLIENT_SECRET`: Client secret of your Xray API key
* `JIRA_HOST`: Your Jira host, probably `https://mycompany.atlassian.net`
* `JIRA_USER`: Your Jira account username, probably your email address
* `JIRA_PASSWORD`: Your Jira account password

You can define credentials as environment variables::

    export XRAY_CLIENT_ID=...
    export XRAY_CLIENT_SECRET=...


Or you can store credentials in a file::

    XRAY_CLIENT_ID=...
    XRAY_CLIENT_SECRET=...
    ...


Create one or more run configuration files as Python modules, such as this::

    # runconfig1.py
    import numpy as np

    v_range = [277.0]
    f_range = np.arange(58, 63, 0.2)
    vdc_range = [820.0]

    class StayConnected:
        voltage_dip_perc = [22, 45, 85, 95]
        dip_total_time_pu = 0.95


All module attributes will be available at runtime as
`runtime_settings.Config.attr_name`, for example::


    from runtime_settings import Config as C

    @python.mark.parametrize('v_range', C.v_range)
    def test_something(v_range):
        pass


Mark your tests with Jira issue keys, such as this::

    @pytest.mark.xray(test_key='PRJ-123')
    def test_something():
        pass

pytest invocation now has some additional command line parameters::


  --runconfig=RUNCONFIG
                        Specify test config script
  --secrets=SECRETS     Full path to secrets file
  --xray-plan-key=XRAY_PLAN_KEY
                        Key of the Xray issue that represents the test plan that is being run
  --xray-fail-silently=XRAY_FAIL_SILENTLY
                        Ignore Xray communication errors

An example of invoking `pytest`::

    pytest --runconfig=myconfig.py --secrets=/private/secrets --xray-plan-key=PRJ-321 --xray-fail-silently=True

Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `MIT`_ license, "pytest-tytest" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/mbranko/pytest-tytest/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
