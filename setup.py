import os
from setuptools import setup, find_packages
PACKAGES = find_packages()

VERSION_INFO = {}
CWD = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(CWD, "mvisonedractivityfeed", "_version.py")) as f:
    exec(f.read(), VERSION_INFO)

opts = dict(
            name="mvisionedractivityfeed",
            maintainer="Camila Stock & Pablo Aguerre",
            install_requires=[
                "dxlstreamingclient"
            ],
            maintainer_email="Camila_Stock@McAfee.com",
            description="Open Source ActivityFeed integrated with OpenDXL streaming clien",
            long_description="Open Source ActivityFeed integrated with OpenDXL streaming client (https://github.com/opendxl/opendxl-streaming-client-python). It includes Client samples that shares thread-data between MVISION EDR and SIEM OnPrem.",
            url="https://github.com/mcafee/mvision-edr-activity-feed",
            download_url="https://github.com/mcafee/mvision-edr-activity-feed",
            license="MIT",
            packages=PACKAGES)


if __name__ == '__main__':
    setup(**opts)
