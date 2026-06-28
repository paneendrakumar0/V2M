from setuptools import setup, find_packages

setup(
    name="v2m",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "fastapi>=0.100.0",
        "uvicorn>=0.23.0",
        "python-multipart>=0.0.6",
        "tqdm>=4.65.0",
        "coloredlogs>=15.0.1",
    ],
)
