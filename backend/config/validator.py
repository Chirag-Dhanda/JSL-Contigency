from pydantic import ValidationError
import sys

def validate_config():
    """Validates that all required environment variables are present and correct."""
    try:
        from config.manager import get_config
        _ = get_config()
    except ValidationError as e:
        sys.stderr.write("\n" + "="*60 + "\n")
        sys.stderr.write("CRITICAL CONFIGURATION ERROR\n")
        sys.stderr.write("="*60 + "\n")
        sys.stderr.write("The application failed to start due to missing or invalid environment variables.\n")
        sys.stderr.write("Please check your .env file or environment variables against the required settings.\n\n")
        sys.stderr.write("Detailed Validation Errors:\n")
        for error in e.errors():
            loc = " -> ".join([str(x) for x in error["loc"]])
            sys.stderr.write(f"- {loc}: {error['msg']}\n")
        sys.stderr.write("="*60 + "\n")
        sys.exit(1)
