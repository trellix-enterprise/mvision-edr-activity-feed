
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
