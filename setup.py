"""
MCAFEE CONFIDENTIAL
Copyright (c) 2019 McAfee, LLC
The source code contained or described herein and all documents related
to the source code ("Material") are owned by McAfee or its
suppliers or licensors. Title to the Material remains with McAfee
or its suppliers and licensors. The Material contains trade
secrets and proprietary and confidential information of McAfee or its
suppliers and licensors. The Material is protected by worldwide copyright
and trade secret laws and treaty provisions. No part of the Material may
be used, copied, reproduced, modified, published, uploaded, posted,
transmitted, distributed, or disclosed in any way without McAfee's prior
express written permission.
No license under any patent, copyright, trade secret or other intellectual
property right is granted to or conferred upon you by disclosure or
delivery of the Materials, either expressly, by implication, inducement,
estoppel or otherwise. Any license under such intellectual property rights
must be express and approved by McAfee in writing.
"""

import os
import ast
from setuptools import setup

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
            name="mvision_edr_activity_feed",
            version=get_version(),
            maintainer="Camila Stock & Pablo Aguerre",
            maintainer_email="Pablo_Aguerre@McAfee.com",
            install_requires=reqs,
            tests_require = test_reqs + reqs,
            description="Open Source ActivityFeed integrated with OpenDXL streaming clien",
            long_description="Open Source ActivityFeed integrated with OpenDXL streaming client (https://github.com/opendxl/opendxl-streaming-client-python).",
            url="https://github.com/mcafee/mvision-edr-activity-feed",
            download_url="https://github.com/mcafee/mvision-edr-activity-feed",
            license="Apache License 2.0",
            packages=['mvision_edr_activity_feed', 'samples', 'samples.esm', 'samples.slack', 'samples.thehive'],
            package_dir={'mvision_edr_activity_feed': 'mvision_edr_activity_feed', 'samples': 'samples'},
            include_package_data=True,
            entry_points={
               'console_scripts': [
                    'mvision-edr-activity-feed = mvision_edr_activity_feed.__main__:main'
               ]
            }
            )

if __name__ == '__main__':
    try:
        setup(**opts)
        print "mvedr-activity-feed setup successfully"
    except Exception as e:
        print e
        raise Exception("Unable to setup mvedr-activity-feed")
