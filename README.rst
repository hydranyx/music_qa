Language Speech Technology: Music QA System
===========================================

This project was setup using `poetry`_. You can setup the dependencies specified in the `pyproject.toml`_ file manually, but using `poetry` is recommended.

Setup using `poetry`
--------------------
After installing `poetry`, navigate to the directory with the `pyproject.toml` file. Then execute the following:

.. code:: sh

   poetry install                          # Setup virtualenv and install dependencies
   poetry run python -m spacy download en  # Download the English language model for spacy
   poetry run pytest tests                 # Run tests and ensure everything is working
   poetry run main                         # Run the main

Setup using `pip`
-----------------
Install the dependencies (specifying the correct versions) via `pip`

.. code:: sh

   pip install --user dependency==X.X.X  # Install some dependency with the version X.X.X

After installing `spacy`, don't forget to download the English language model.
   
.. code:: sh

   python -m spacy download en

.. _pyproject.toml: ./pyproject.toml
.. _poetry: https://poetry.eustace.io/
