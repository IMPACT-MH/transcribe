# setup.py

from setuptools import setup, find_packages

# Helper function to read requirements from `requirements.txt`
def read_requirements():
    with open("requirements.txt") as f:
        return f.read().splitlines()

setup(
    name="transcribe",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=read_requirements(),  # Read requirements.txt
    entry_points={
        'console_scripts': [
            'transcribe=transcribe.__main__:main',
        ],
    },
    description="A tool for transcribing audio files using Whisper.",
    author="Josh Kenney",
    author_email="joshua.kenney@yale.edu",
    url="https://github.com/IMPACT-MH/transcribe",
)
