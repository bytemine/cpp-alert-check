from setuptools import setup

setup(
    name="cpp_alert_check",
    version="0.0.1",
    description="CrashPlan alert check for Icinga",
    packages=["cpp_alert_check"],
    author="bytemine GmbH",
    author_email="schuller@bytemine.net",
    install_requires=[
        "certifi",
        "chardet",
        "idna",
        "requests",
        "urllib3"
    ],
    entry_points={'console_scripts':['cpp_alert_check=cpp_alert_check.cpp_alert_check:main']}
)
