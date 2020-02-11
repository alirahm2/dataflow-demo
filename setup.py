import setuptools

REQUIRED_PACKAGES = ["kafka-python==1.4.7"]

setuptools.setup(
    name="app",
    version="1.0.0",
    description="DataFlow worker",
    install_requires=REQUIRED_PACKAGES,
    dependency_links=[],
    packages=setuptools.find_packages(),
)
