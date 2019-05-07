from setuptools import setup, find_packages
PACKAGES = find_packages()

opts = dict(name="activityfeed",
            maintainer="Camila Stock & Pablo Aguerre",
            maintainer_email="Pablo_Aguerre@McAfee.com",
            description="Open Source ActivityFeed integrated with OpenDXL streaming clien",
            long_description="Open Source ActivityFeed integrated with OpenDXL streaming client (https://github.com/opendxl/opendxl-streaming-client-python). It includes Client samples that shares thread-data between MVISION EDR and SIEM OnPrem.",
            url="https://github.com/mcafee/mvision-edr-activity-feed",
            download_url="https://github.com/mcafee/mvision-edr-activity-feed",
            license="MIT",
            packages=PACKAGES)


if __name__ == '__main__':
    setup(**opts)
