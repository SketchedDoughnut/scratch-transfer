"""
__main__.py

Orchastrates unpacking, converting assets, parsing
the project, and copying files based on configuration.
"""

import logging

from . import config, packer, parser, unpacker


def main():
    """
    Converts the project using the settings saved in config
    """
    # Setup the logger
    logging.basicConfig(
        format="[%(levelname)s] %(message)s", level=config.LOG_LEVEL)

    # Download the project from the internet
    if config.PROJECT_URL:
        project = unpacker.download_project(
            config.PROJECT_URL, config.OUTPUT_FOLDER)

    # Extract the project from an sb3
    elif config.PROJECT_PATH:
        project = unpacker.extract_project(
            config.PROJECT_PATH, config.OUTPUT_FOLDER)

    else:
        logging.error("A project url/path was not provided.")
        project = None

    # Verify the project was unpacked
    if project is None:
        logging.critical("Failed to unpack project.")
        return False

    # Save a debug json
    if config.DEBUG_JSON:
        project.save_json(config.FORMAT_JSON)

    # Convert project assets
    if config.CONVERT_ASSETS:
        unpacker.convert_assets(project)

    # Parse the project
    code = parser.parse_project(project)

    # Save the project's code
    packer.save_code(project, code)

    # Copy engine files
    packer.copy_engine(project)

    while True:
        input(project.output_dir)


if __name__ == '__main__':
    main()
