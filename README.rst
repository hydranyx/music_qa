Language Speech Technology: Music QA System
===========================================
|Python Versions|

This project was setup using `poetry`_. You can setup the dependencies specified in the `pyproject.toml`_ file manually, but using ``poetry`` is recommended.

Setup using ``poetry``
--------------------
After installing ``poetry``, navigate to the directory with the ``pyproject.toml`` file. Then execute the following:

.. code:: sh

   poetry install                          # Setup virtualenv and install dependencies
   poetry run python -m spacy download en  # Download the English language model for spacy
   poetry run pytest tests                 # Run tests and ensure everything is working
   poetry run main                         # Run the main

Setup using ``pip``
-----------------
Install the dependencies (specifying the correct versions) via ``pip``

.. code:: sh

   pip install --user dependency==X.X.X  # Install some dependency with the version X.X.X

After installing ``spacy``, don't forget to download the English language model.
   
.. code:: sh

   python -m spacy download en

After all the dependencies have been installed, you may run the tests or execute the main application.

.. code:: sh

   pytest tests  # Run tests and ensure everything is working
   python music_qa/main.py

.. |Python Versions| image:: https://img.shields.io/badge/python-3.5-blue.svg
.. _pyproject.toml: ./pyproject.toml
.. _poetry: https://poetry.eustace.io/
