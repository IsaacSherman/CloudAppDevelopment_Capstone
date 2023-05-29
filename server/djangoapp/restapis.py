import requests
import json
from json import JSONDecodeError
from .models import CarDealer, CarMake, CarModel, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
from datetime import datetime

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url, auth=None, **kwargs):
    print (kwargs)
    print (f"GET from {url}")
    try:
        if auth is not None:
            response = requests.get(url, auth=auth,
                headers={"Content-Type":"application/json"},
                params = kwargs)
        else:
            response= requests.get(url, 
                headers={"Content-Type":"application/json"},
                params = kwargs)
    except:
        print (f"Network exception occurred")
    status_code = response.status_code
    print(f"Status: {status_code}")
    print(f"response = {response}")
    if not hasattr(response, "text"):
        return json.loads("{ }")
    try:
        return json.loads(response.text)
    except JSONDecodeError as e:
        print(e)
        return json.loads("{ }")

def get_dealers_from_cf(url, **kwargs):
    results= []
    json_result = get_request(url)["response"]["docs"]
    print(f"here: {json_result}")
    if json_result:
        for dealer_doc in json_result:
            print(dealer_doc)
            dealer_obj = CarDealer(
                address=dealer_doc["address"], 
                city=dealer_doc["city"], 
                full_name=dealer_doc["full_name"],
                id=dealer_doc["id"], 
                latitude=dealer_doc["lat"],
                longitude=dealer_doc["long"],
                short_name=dealer_doc["short_name"],
                st=dealer_doc["st"],
                state=dealer_doc["state"],
                zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url)
    if json_result:
        for review in json_result["results"]:
            if "purchase_date" not in review:
                review["purchase_date"] = datetime.now() 
            if "car_make" not in review:
                review["car_make"] = "Unknown" 
            if "car_model" not in review:
                review["car_model"] = "Unknown"
            if "car_year" not in review:
                review["car_year"] = "Unknown"

            obj = DealerReview(
                dealership=review["dealership"], 
                name=review["name"], 
                review=review["review"],
                purchase=review["purchase"],
                id=review["id"], 
                purchase_date=review["purchase_date"],
                car_make=review["car_make"],
                car_model=review["car_model"],
                car_year=review["car_year"],
                sentiment="positive", 
                )
            obj.sentiment = analyze_review_sentiments(review["review"])
            print(obj.sentiment)
            results.append(obj)
    return results

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    result = requests.post(url, json=json_payload, params=kwargs)
    print(result)
    

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/8215bb78-6279-4f27-ab7d-f4c029305d5e"
    key = "".join(["TV2pCH_","Xhp7xatIQ","e8K7CCPrSf","c0nw7x8dF9","nG34bnRk"])
    auth = HTTPBasicAuth("apikey", key)
    authenticator = IAMAuthenticator(key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2023-05-11',
        authenticator=authenticator
        )
    try:
        response = natural_language_understanding.analyze(
        text=text,
        features=Features(
            entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
            keywords=KeywordsOptions(emotion=True, sentiment=True,
                                    limit=2))).get_result()
    except Exception as e:
        print(e)
        return "neutral"
    print(response)

    return response["keywords"][0]["sentiment"]["label"]
    # natural_language_understanding.set_service_url(url)
    # features = Features(        
    #     entities=EntitiesOptions(emotion=True, sentiment=True),
    #     keywords=KeywordsOptions(emotion=True, sentiment=True,)
    # )
    # result = natural_language_understanding.analyze(text=text, features=Features).get_result()

    # print (result)
    # return result

