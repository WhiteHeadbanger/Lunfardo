"""
Lunfardo entry point.
"""
import argparse
import os
import sys
from .lunfardo import Lunfardo

def main() -> None:
    """Main entry point of the Lunfardo interpreter."""
    parser = argparse.ArgumentParser(
        description="Execute Lunfardo code from a file or start the REPL."
    )
    parser.add_argument("file", nargs="?", help="Path to the Lunfardo file to execute.")
    args = parser.parse_args()

    lunfardo = Lunfardo()  # Instance of the Lunfardo class

    if args.file:
        script_path = os.path.abspath(args.file)
        if not os.path.isfile(script_path):
            print(f"Error: File not found: {script_path}")
            sys.exit(1)
        lunfardo.execute_file(script_path)
    else:
        lunfardo.run_repl()

if __name__ == "__main__":
    main()
