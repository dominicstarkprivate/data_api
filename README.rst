# Installation

  To install the package, follow these steps:
1) Make sure `python3.10` is installed on your system.
2) Create a virtual environment with the tool of your choice, e.g. `virtualenv -p python3.10 project_env`
3) Activate your virtual environment, `cd` into the `data_api` top level folder, and run `make install`
4) Initialize the database by running `make reset_db`
5) Start the server by running `make run`


# Test

To run the unittests, use `make unit_tests`.

For manual testing, make sure you have a clean db (`make reset_db` and a running server `make run`). Then you can use any tool (e.g. Postman, curl, python script, ...) to make requests to any of the following endpoints:

- POST at`http://127.0.0.1:5000/data/<customer_id>/<dialog_id>` with a json request body, e.g. `{"text": "my text", "language": "EN"}`
- POST at `http://127.0.0.1:5000/consents/<dialog_id>` with a json request body, e.g. `{"consent": true}`
- GET at `http://127.0.0.1:5000/data`. This one also supports query parameters, e.g. `http://127.0.0.1:5000/data?language=EN&text=my text`

