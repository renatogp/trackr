===============================
trackr
===============================


.. image:: https://img.shields.io/pypi/v/trackr.svg
        :target: https://pypi.python.org/pypi/trackr

.. image:: https://img.shields.io/travis/rpedigoni/trackr.svg
        :target: https://travis-ci.org/rpedigoni/trackr

.. image:: https://readthedocs.org/projects/trackr/badge/?version=latest
        :target: https://trackr.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/rpedigoni/trackr/shield.svg
     :target: https://pyup.io/repos/github/rpedigoni/trackr/
     :alt: Updates




* Free software: MIT license
* Documentation: https://trackr.readthedocs.io.


``trackr`` is a lightweight Python lib to access carriers' tracking information.

Installation
------------

``pip install trackr``

Works with Python `2.7`, `3.3`, `3.4` and `3.5`.


Usage
-------

.. code-block:: python

    from trackr import Trackr

    package = Trackr.track('ect', 'PN871429404BR')

    for t in package.tracking_info:
        print t.location, t.status


Or also using Trackr cli:

.. code-block:: sh
    
    $ trackr --carrier=ect --object-id=PN871429404BR


Available carriers
------------------

* ``ect`` (brazilian "Correios")
* ``fake`` (for testing purposes)


ECT
~~~

Data is retrieved from Correios using its SOAP webservice. For that you'll need an username and password. Get in touch with your ECT representative to gain acess.

The easiest way to provide the credentials is exporting as env variable:

.. code-block:: sh
    
    export TRACKR_ECT_USERNAME=**
    export TRACKR_ECT_PASSWORD=**


You can also pass a function keyword args:

.. code-block:: python

    package = Trackr.track('ect', 'PN871429404BR', ect_username='**', ect_password='**')


Fake
~~~~

Fake carrier is meant to be used when testing and developing integrations. It will always return as package found with 4 tracking info rows. Example

.. code-block:: sh

    $ trackr --carrier=fake --object-id=123456789

.. code-block:: sh

    Package found!
    2017-04-23 15:12:23.521052 - City 1 - In transit 1
    2017-04-23 15:12:23.521075 - City 2 - In transit 2
    2017-04-23 15:12:23.521081 - City 3 - In transit 3
    2017-04-23 15:12:23.521086 - City 4 - In transit 4


Integrating a new carrier
~~~~~~~~~~~~~~~~~~~~~~~~~

To add a new carrier, inherit `carriers.base.BaseCarrier` and fillout the `track()` method, it must return a `carriers.base.Package` instance. See an example below:

.. code-block:: python

    from datetime import datetime
    from .base import BaseCarrier


    class MyOwnCarrier(BaseCarrier):
        id = 'mycarrier'
        name = 'My Carrier'

        def track(self, object_id):

            # ... fetch data from carrier's data source

            package = self.create_package(
                object_id=object_id,
                service_name='Express service',
            )

            package.add_tracking_info(
                date=datetime(2017, 1, 1, 10, 00),
                location='Last Location',
                status='In transit to another location'
                description='Get ready!',
            )

            package.add_tracking_info(
                date=datetime.now(),
                location='Current Location',
                status='Delivered'
                description='Finally',
            )


            return package

Then update the carrier mapping on ``trackr/carriers/__init__.py`` (this should be improved with some autodiscover feature). Remember to write tests!


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

