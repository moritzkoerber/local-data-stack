from setuptools import find_packages, setup

setup(
    name="local_dagster",
    version="0.0.1",
    packages=find_packages(),
    package_data={
        "local_dagster": [
            "dbt-project/**/*",
        ],
    },
    install_requires=[
        "dagster",
        "dagster-cloud",
        "dagster-dbt",
        "dbt-duckdb<1.10",
    ],
    extras_require={
        "dev": [
            "dagster-webserver",
        ]
    },
)
