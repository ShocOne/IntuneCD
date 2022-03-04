#!/usr/bin/env python3

"""
This module backs up all Management Partners in Intune.

Parameters
----------
path : str
    The path to save the backup to
output : str
    The format the backup will be saved as
token : str
    The token to use for authenticating the request
"""

import json
import os
import yaml

from .clean_filename import clean_filename
from .graph_request import makeapirequest

## Set MS Graph endpoint
endpoint = "https://graph.microsoft.com/beta/deviceManagement/deviceManagementPartners"

## Get all Management Partners and save them in specified path
def savebackup(path, output, token):
    configpath = path+"/"+"Partner Connections/Management/"
    data = makeapirequest(endpoint, token)

    for partner in data['value']:
        if partner['isConfigured'] is False:
            continue
        else:
            print("Backing up Management Partner: " + partner['displayName'])
            
            remove_keys = {'id', 'createdDateTime', 'version', 'lastModifiedDateTime'}
            for k in remove_keys:
                partner.pop(k, None)

            if os.path.exists(configpath) == False:
                os.makedirs(configpath)

            ## Get filename without illegal characters
            fname = clean_filename(partner['displayName'])
            ## Save Compliance policy as JSON or YAML depending on configured value in "-o"
            if output != "json":
                with open(configpath+fname+".yaml", 'w') as yamlFile:
                    yaml.dump(partner, yamlFile, sort_keys=False,
                            default_flow_style=False)
            else:
                with open(configpath+fname+".json", 'w') as jsonFile:
                    json.dump(partner, jsonFile, indent=10)