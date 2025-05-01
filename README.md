# Python API CLI App

A Python project that includes:
- A [FastAPI](https://fastapi.tiangolo.com/) API app to interact with the data (located at the `backend` package).
- A command-line interface (CLI) utility `file-client` for retrieving metadata and contents of files from an API (build from the `cli_app` package).

## Libraries Used
- FastAPI for the backend part.
- Argparse and requests for `file-client`.
- Pytest and requests_mock for testing.

## Getting Started

You need Python 3.10+. Create a venv and install all necessary libraries with `pip install -r requirements.txt`.

To install the `file-client` command, run `pip install -e ./cli_app`.

## API Routes
To run the REST API app, run `uvicorn backend.rest_api:app --reload`.

The API includes the following routes:
- POST: `/file/` -- upload a file to the dict.
- GET: `/file/{file_id}/stat/` -- get the metadata about a file (file_id is its UUID)
- GET: `/file/{file_id}/read/` -- get the content of a file (file_id is its UUID)

## file-client
This is the output of `file-client -h`:

```
usage: file-client [-h] [-b {grpc,rest}] [-g GRPC_SERVER] [-u BASE_URL] [-o OUTPUT] {stat,read} ...

A simple CLI application which retrieves and prints data from a REST API.

options:
  -h, --help            show this help message and exit
  -b {grpc,rest}, --backend {grpc,rest}
                        Set a backend to be used, choices are grpc and rest. Default is grpc.
  -g GRPC_SERVER, --grpc-server GRPC_SERVER
                        Set a host and port of the gRPC server. Default is localhost:50051.
  -u BASE_URL, --base-url BASE_URL
                        Set a base URL for a REST server. Default is http://localhost/.
  -o OUTPUT, --output OUTPUT
                        Set the file where to store the output. Default is -, i.e. the stdout.

subcommands:
  {stat,read}           File operations
    stat                Prints the file metadata in a human-readable manner.
    read                Outputs the file content.
```

Warning: Only REST is implemented.

## Testing
All test can be run with the `pytest` command.
