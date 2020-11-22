import logging
import json
from datetime import datetime
import urllib3
import os

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    http = urllib3.PoolManager()
    url = "https://api.eu.opsgenie.com/v2/alerts"
    # data = json.loads(req['body'])
    request_json_body = req.get_json()
    now = datetime.now()
    date_time = now.strftime("%Y/%m/%d, %H:%M:%S")

    # Set OpsGenie HTTP request headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': os.environ.get('GENIE_KEY')
    }

    if not isinstance(request_json_body, list):  # Is this a single JSON object (dict)
        request_json_body = [request_json_body]  # Place into a list

        # Gather key pieces of info from Prisma Alert JSON
    try:
        for counter, value in enumerate(request_json_body):
            account_name = request_json_body[counter]["accountName"]
            severity = request_json_body[counter]["severity"]
            rule_name = request_json_body[counter]["alertRuleName"]
            resource_id = request_json_body[counter]["resourceId"]
            policy_desc = request_json_body[counter]["policyDescription"]
            cloud_resource_type = request_json_body[counter]["resourceCloudService"]
            cloud_type = request_json_body[counter]["cloudType"]
            prisma_alert_url = request_json_body[counter]["callbackUrl"]

            # name given to the alert message (title)
            message = 'Prisma Alert: ' + "| " + date_time + \
                " | " + resource_id + " " + rule_name

            # String for the alert body
            description = 'Alert details \n' + "Link to alert: " + prisma_alert_url + "\n" \
                   + "Account name: " + account_name + "\n" \
                   + "Cloud platform: " + cloud_type + "\n" + "Resource type: " + cloud_resource_type + "\n" \
                   + "Policy description: " + policy_desc + "\n"

            # Build the request JSON to be sent to OpsGenie
            req_data = {
                'message': message,  # message is a mandatory field
                'description': description,
                'priority': 'P2'
            }
            encoded_req_data = json.dumps(req_data).encode('utf-8')

            r = http.request(
                'POST',
                url,
                body=encoded_req_data,
                headers=headers)

            print(r.data)

    except:
        # Reflect the request back as a response. This will greatly aid troubleshooting...
        # so one can analyse the JSON structure against what is expected.
        return func.HttpResponse(
                "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
                status_code=200
                )

    return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
             )

    # name = req.params.get('name')
    # if not name:
    #     try:
    #         req_body = req.get_json()
    #     except ValueError:
    #         pass
    #     else:
    #         name = req_body.get('name')

    # if name:
    #     return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    # else:
    #     return func.HttpResponse(
    #         "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
    #         status_code=200
    #     )
