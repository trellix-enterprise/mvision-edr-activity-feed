import os
import ast
from setuptools import setup, find_packages

PACKAGES = find_packages('mvision_edr_activity_feed')
CWD = os.path.abspath(os.path.dirname(__file__))

def get_version():
    f = open(os.path.join(CWD,'mvision_edr_activity_feed/__init__.py'), 'r')
    code = ast.parse(f.read())

    for item in code.body:
        if type(item) == ast.Assign:
            if item.targets[0].id == '__version__':
                return item.value.s
    raise Exception("Cloud not read version from package")

reqs = [
    'dxlstreamingclient==0.1.1',
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
            version=get_version(),
            maintainer="Camila Stock & Pablo Aguerre",
            maintainer_email="Camila_Stock@McAfee.com",
            install_requires=reqs,
            tests_require = test_reqs + reqs,
            description="Open Source ActivityFeed integrated with OpenDXL streaming clien",
            long_description="Open Source ActivityFeed integrated with OpenDXL streaming client (https://github.com/opendxl/opendxl-streaming-client-python).",
            url="https://github.com/mcafee/mvision-edr-activity-feed",
            download_url="https://github.com/mcafee/mvision-edr-activity-feed",
            license="Apache License 2.0",
            packages=PACKAGES,
            package_dir={'': 'mvision_edr_activity_feed'},
            include_package_data=True,
            entry_points={
                'console_scripts': [
                    'mvision-edr-activity-feed = '
                    'mvision_edr_activity_feed.__main__:main'
                ]
            })


if __name__ == '__main__':
    setup(**opts)
