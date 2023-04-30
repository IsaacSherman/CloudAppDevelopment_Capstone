
"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
import json
import sys
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import requests

#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
def main(param_dict, query=None):
    """Main Function

    Args:
        param_dict (Dict): json containing COUCH_URL, IAM_API_KEY, and COUCH_USERNAME
            query: object defining the query.  Must contain:
                selector: a dictonary containing fields to select and  a dictionary for selecting on that field  {"_id":{"$gt":0}}
                sort(optional): a list containing the dictionary objects defining a sort.  [{"_id": "desc"}, ...]. No sort is applied if none is specified 
                fields(optional): a list containing the fields to select.  ["_id", "state"].  All fields are selected if none are specified
    Returns:
        json of database names
    """
    if not query:
        query = param_dict["query"]
        param_dict = param_dict["param_dict"]
    if "selector" not in query:
        raise Exception("Invalid query", "A query must have a selector")
    if "fields" not in query:
        fields = list()
    else:
        fields = list(query["fields"])
    if "sort" not in query:
        sort = list()
    else:
        sort = list(query["sort"])
    selector = dict(query["selector"])
    authenticator = IAMAuthenticator(param_dict["IAM_API_KEY"])
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(param_dict["COUCH_URL"])
    resp = service.post_dbs_info(['dealerships'])
    response = service.post_find(
        db="dealerships",
        selector=selector,
        sort = sort,
        fields = fields,
        ).get_result()

    print(response)
    return {"info": resp.result,
        "result": response
    }

with open("../../creds.json", encoding='UTF8') as fin:
    params = json.load(fin)
query = {
    "selector":{
        "_id":{
            "$gt": "0"
        }
    },
    "sort":[
        {
            "_id":"desc"
        }
    ]
}
butts = main(params, query)
print(butts)
