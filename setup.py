import os
from setuptools import setup, find_packages
PACKAGES = find_packages()

VERSION_INFO = {}
CWD = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(CWD, "mvison_edr_activity_feed", "_version.py")) as f:
    exec(f.read(), VERSION_INFO)

reqs = [
    'dxlstreamingclient==',
    'requests==2.22.0',
    'jmespath==0.9.4',
    'furl==2.0.0'
]

test_reqs = [
    'mock==3.0.5',
    'pytest==4.5.0',
    'coverage==4.5.3',
    'coveralls==1.7.0',
    'pytest-cov==2.7.1',
    'numpy==1.16.3'
]

opts = dict(
            name="mvisionedractivityfeed",
            maintainer="Camila Stock & Pablo Aguerre",
            install_requires=reqs,
            tests_require = test_reqs + reqs,
            maintainer_email="Camila_Stock@McAfee.com",
            description="Open Source ActivityFeed integrated with OpenDXL streaming clien",
            long_description="Open Source ActivityFeed integrated with OpenDXL streaming client (https://github.com/opendxl/opendxl-streaming-client-python). It includes Client samples that shares thread-data between MVISION EDR and SIEM OnPrem.",
            url="https://github.com/mcafee/mvision-edr-activity-feed",
            download_url="https://github.com/mcafee/mvision-edr-activity-feed",
            license="Apache License 2.0",
            packages=PACKAGES)


if __name__ == '__main__':
    setup(**opts)
