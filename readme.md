# Prisma Cloud OpsGenie Alert Integration

This repository is to facilitate the sending of Prisma Cloud alerts to OpsGenie.

Direct Webhook integration isn't possible because of limitations of the OpsGenie API. Some notes:
* Alert API 'message' field is mandatory.
* API Integration on OpsGenie does NOT support dynamic fields. This is unfortunate because this would allow the 'translation' of any field in the JSON payload to the field(s) required by OpsGenie. This means there is zero flexibility in the sending of payloads to OpsGenie.

## Code Information

This repo is specifically for running on Azure Functions. Runtime is Python 3.8 but the code should work on other 3.x versions.

## Connecting to the OpsGenie API

The Azure function code should have a file named "local.settings.json". Here you set environment variables. In Azure itself you go to your function > Settings > Configuration > Application Settings. Key "GENIE_KEY", value format below.

The OpsGenie API key should exist as an env variable named "GENIE_KEY" with the value set to "GenieKey <your-api-key>".

## How the function works

Prisma Cloud sends alert information as a JSON object. Sometimes this is a single object, but oftentimes alerts are grouped into a JSON Array. The code checks if this is a single object, and if so places into an Array (Python List). This is to make the for loop always valid, even if just a single iteration.

The code grabs specific JSON key/values from the payload. This is completely customisable. Full reference of the Alert Payload is here: https://docs.paloaltonetworks.com/prisma/prisma-cloud/prisma-cloud-admin/manage-prisma-cloud-alerts/alert-payload.html

It then builds a message (OpsGenie mandatory) and optional description (which is of course recommended to populate the alert with more meaningful imformation). Priority is set to P2 but this can be changed.

For each alert we then call the OpsGenie API with the built message and description. 

**Please note** this would generate an alert for every Prisma alert. So if we have a grouped alert this could generate a lot. One potential change should you wish to just call OpsGenie once, would be not to iterate through the Python List, but rather just access the first list item:

    request_json_body[0]["<json-key>"]