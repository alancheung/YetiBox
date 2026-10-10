import argparse
import json
from pathlib import Path
import sys


argParser = argparse.ArgumentParser()
argParser.add_argument("--output-file", type=str, default="yetibox-openapi.json", help="The name of the output file")

args = argParser.parse_args()

if __name__ == "__main__":   
    """ 
    Export the OpenAPI schema for the application 
    so it can be used by external dependencies like
    Orval for automatic React hook generation
    """

    try:
        from main import app
    except ModuleNotFoundError as error:
        print(
            f"Could not load the API application because Python module "
            f"'{error.name}' is unavailable. Activate the YetiBox.API Python "
            "environment and install its dependencies with "
            "'python -m pip install -r requirements.txt'.",
            file=sys.stderr,
        )
        raise SystemExit(1) from error

    # Call once to generate (twice returns the URL)
    openapi = app.openapi()

    output_path = Path(args.output_file)
    output_path.write_text(json.dumps(openapi, indent=4, sort_keys=True))