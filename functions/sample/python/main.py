
"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import requests
import json
import sys
#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
def main(param_dict):
    """Main Function

    Args:
        param_dict (Dict): json containing COUCH_URL, IAM_API_KEY, and COUCH_USERNAME

    Returns:
        json of database names
    """

    authenticator = IAMAuthenticator(param_dict["IAM_API_KEY"])
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(param_dict["COUCH_URL"])
    resp = service.post_dbs_info(['dealerships'])
    response = service.post_find(
        db="dealerships",
        selector={"id":{'$eq':7}}
        ).get_result()

    print(response)
    return {"info": resp.result}

with open("../../creds.json") as fin:
    param_dict = json.load(fin)
butts = main(param_dict)
print(butts)
