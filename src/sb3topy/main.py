"""
main.py

Orchastrates unpacking, converting assets, parsing
the project, and copying files based on configuration.

To allow simple configuration from the command line, the
path to a configuration json can be passed as an argument.
"""


import logging

from . import config, gui, packer, parser, unpacker


def main():
    """
    Converts the project using the settings saved in config
    """
    # Load configuration from the command line
    config.parse_args()

    # Setup the logger
    logging.basicConfig(
        format="[%(levelname)s] %(message)s", level=config.LOG_LEVEL)

    # Run the gui if it is enabled
    if config.USE_GUI:
        gui.run_app()
        return True

    # Download the project from the internet
    if config.PROJECT_URL:
        project = unpacker.download_project(
            config.PROJECT_URL, config.OUTPUT_PATH)

    # Extract the project from an sb3
    elif config.PROJECT_PATH:
        project = unpacker.extract_project(
            config.PROJECT_PATH, config.OUTPUT_PATH)

    else:
        logging.error("A project url/path was not provided.")
        project = None

    # Verify the project was unpacked
    if project is None:
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

    logging.info("Finished converting project. Saved in '%s'",
                 project.output_dir)

    if config.AUTORUN:
        packer.run_project(project.output_dir)

    return True