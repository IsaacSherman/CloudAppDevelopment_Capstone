
"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import requests
import sys
d = {
     "COUCH_URL": "https://apikey-v2-xuso6iwsvgf8lrstj2rdk4sqten31eg8x2fge5erjgj:1f20061c1971f7212c14cc02a90db4c4@506718bd-b1ce-4e22-b680-50edf9440bca-bluemix.cloudantnosqldb.appdomain.cloud",
    "IAM_API_KEY": "tcsOCvIqxa6jZ-8r-PFzYDwAWCrJ1EbH4-1twofiPipo",
    "COUCH_USERNAME": "apikey-v2-xuso6iwsvgf8lrstj2rdk4sqten31eg8x2fge5erjgj"
}
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

    return {"dbs": service.get_all_dbs().get_result()}