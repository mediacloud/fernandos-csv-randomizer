import sys

import ez_setup
from fernandos_csv_randomizer import APP_TITLE, APP_NAME, APP_VERSION

ez_setup.use_setuptools()

from setuptools import setup

ENTRY_POINT = 'fernandos_csv_randomizer.py'

if sys.platform == 'darwin':
    extra_options = dict(
        setup_requires=['py2app'],
        app=[ENTRY_POINT],
        options=dict(
            py2app={
                # Cross-platform applications generally expect sys.argv to be used for opening files
                'argv_emulation': True,
                'iconfile': 'fernando.icns',
                'plist': {
                    'CFBundleName': APP_NAME,
                    'CFBundleDisplayName': APP_TITLE,
                    'CFBundleGetInfoString': 'Randomizes CSV and outputs a preset number of rows.',
                    'CFBundleVersion': APP_VERSION,
                    'CFBundleShortVersionString': APP_VERSION,
                    'CFBundleIdentifier': 'org.mediacloud.fernandos_csv_randomizer',
                },
            },
        ),
    )

elif sys.platform == 'win32':
    extra_options = dict(
        setup_requires=['py2exe'],
        app=[ENTRY_POINT],
    )
else:
    extra_options = dict(
        # Normally unix-like platforms will use "setup.py install" and install the main script as such
        scripts=[ENTRY_POINT],
    )

setup(
    name=APP_NAME,
    **extra_options
)
