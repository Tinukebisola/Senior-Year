import json
import requests
from pprint import pprint

url = "https://www.realtor.com/api/v1/rdc_search_srp?client_id=rdc-search-rentals&schema=vesta"
headers = {"content-type": "application/json"}

# RENT
body = r'{"query":"\nquery ConsumerSearchQuery($query: HomeSearchCriteria!, $limit: Int, $offset: Int, $sort: [SearchAPISort], $bucket: SearchAPIBucket) {\n  home_search(query: $query, sort: $sort, limit: $limit, offset: $offset, bucket: $bucket) {\n    costar_counts {\n      costar_total\n      non_costar_total\n    }\n    total\n    count\n    properties: results {\n      property_id\n      listing_id\n      list_price\n      list_price_max\n      list_price_min\n      permalink\n      price_reduced_amount\n      matterport\n      virtual_tours {\n        href\n      }\n      status\n      list_date\n      lead_attributes {\n        lead_type\n      }\n      pet_policy {\n        cats\n        dogs\n        dogs_small\n        dogs_large\n      }\n      other_listings {\n        rdc{\n          listing_id,\n          status\n        }\n      }\n      flags {\n        is_pending\n      }\n      photos(limit: 2, https: true) {\n        href\n      }\n      primary_photo(https: true) {\n          href\n      }\n      advertisers {\n        office {\n          name\n          phones {\n            number\n            type\n            primary\n            trackable\n            ext\n          }\n        }\n        phones {\n          number\n          type\n          primary\n          trackable\n          ext\n        }\n      }\n      flags {\n        is_new_listing\n      }\n      location {\n        address {\n          line\n          city\n          coordinate {\n            lat\n            lon\n          }\n          country\n          state_code\n          postal_code\n        }\n        county {\n          name\n          fips_code\n        }\n      }\n      description {\n        beds\n        beds_max\n        beds_min\n        baths\n        baths_min\n        baths_max\n        baths_full\n        baths_full_calc\n        baths_half\n        baths_3qtr\n        baths_1qtr\n        garage\n        garage_min\n        garage_max\n        sqft\n        sqft_max\n        sqft_min\n        lot_sqft\n        name\n        sub_type\n        type\n        year_built\n      }\n      units {\n        availability {\n          date\n        }\n        description {\n          baths\n          beds\n          sqft\n        }\n        list_price\n      }\n      branding {\n        type\n        photo\n        name\n      }\n      source {\n        id\n        type\n      }\n    }\n  }\n}\n","variables":{"geoSupportedSlug":"","query":{"primary":true,"status":["for_rent"],"state_code":"CO","pending":false},"limit":42,"offset":42,"bucket":{"sort":"rentalModelV2_1","sort_options":{"costar_total":1311,"non_costar_total":5992,"variation":"costar_basic"}}},"seoPayload":{"asPath":"/apartments/Colorado/","pageType":{"silo":"search_result_page","status":"for_rent"},"county_needed_for_uniq":false}}'
json_body = json.loads(body)


r = requests.post(url=url, json=json_body, headers=headers)
json_data = r.json()
all_properties = []
for entry in json_data["data"]["home_search"]["properties"]:
    try:
        pict = [i['href'] for i in entry["photos"]]
        feature_dict = {
            "id": entry["property_id"],
            "price": entry["list_price"],
            "min_price": entry["list_price_min"],
            "max_price": entry["list_price_max"],
            'cats': entry["pet_policy"].get('cats'),
            'dogs': entry["pet_policy"].get('dogs'),
            'pet_policy_text': entry["pet_policy"].get('text'),
            "beds": entry["description"]["beds"],
            "min_beds": entry["description"]["beds_min"],
            "max_beds": entry["description"]["beds_max"],
            "baths": entry["description"]["baths"],
            "min_baths": entry["description"]["baths_min"],
            "max_baths": entry["description"]["baths_max"],
            "garage": entry["description"]["garage"],
            "house_type": entry["description"]["type"],
            "sqft": entry["description"]["sqft"],
            "year_built": entry["description"]["year_built"],
            "address": entry["location"]["address"]["line"],
            "postal_code": entry["location"]["address"]["postal_code"],
            "state": entry["location"]["address"]["state_code"],
            "city": entry["location"]["address"]["city"],
            "pictures": pict[0],
            "pictures1": pict[1]
        }

        if entry["location"]["address"]["coordinate"]:
            feature_dict.update({"lat": entry["location"]["address"]["coordinate"]["lat"]})
            feature_dict.update({"lon": entry["location"]["address"]["coordinate"]["lon"]})

        if entry["location"]["county"]:
            feature_dict.update({"county": entry["location"]["county"]["name"]})


        all_properties.append(feature_dict)
    except:
        pass

print(all_properties)