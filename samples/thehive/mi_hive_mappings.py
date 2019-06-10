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

case_priority_mappings = {'unspecified': 0, 'low': 1, 'medium': 2, 'high': 3}

case_status_mappings = {'new': 'Open',
                        'in_progress': 'Open',
                        'inProgress': 'Open',
                        'inconclusive': 'Resolved',
                        'dismissed': 'Resolved',
                        'incident declared': 'Resolved',
                        'incident_declared': 'Resolved'}

case_resolution_mappings = {'inconclusive': 'Indeterminate',
                            'dismissed': 'FalsePositive',
                            'incident declared': 'TruePositive',
                            'incident_declared': 'TruePositive'}
