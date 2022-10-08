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
# pprint(json_data)
for entry in json_data["data"]["home_search"]["properties"]:
    pprint(entry)
    pprint(entry['description'])
    print(entry['description']['baths'])

