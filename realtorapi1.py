import json
import requests
import pandas as pd
from tabulate import tabulate
from pprint import pprint


class RealtorScraper:
    def __init__(self, locations: list) -> None:
        self.locations = locations
        self.all = []
        self.df = None

    def send_request(self, state_code: str, asPath: str, limit, offset) -> dict:
        url = "https://www.realtor.com/api/v1/rdc_search_srp?client_id=rdc-search-rentals&schema=vesta"
        headers = {"content-type": "application/json"}
        body = r'{"query":"\nquery ConsumerSearchQuery($query: HomeSearchCriteria!, $limit: Int, $offset: Int, $sort: [SearchAPISort], $bucket: SearchAPIBucket) {\n  home_search(query: $query, sort: $sort, limit: $limit, offset: $offset, bucket: $bucket) {\n    costar_counts {\n      costar_total\n      non_costar_total\n    }\n    total\n    count\n    properties: results {\n      property_id\n      listing_id\n      list_price\n      list_price_max\n      list_price_min\n      permalink\n      price_reduced_amount\n      matterport\n      has_specials\n      virtual_tours {\n        href\n      }\n      status\n      list_date\n      lead_attributes {\n        lead_type\n      }\n      pet_policy {\n        cats\n        dogs\n        dogs_small\n        dogs_large\n      }\n      other_listings {\n        rdc{\n          listing_id,\n          status\n        }\n      }\n      flags {\n        is_pending\n      }\n      photos(limit: 2, https: true) {\n        href\n      }\n      primary_photo(https: true) {\n          href\n      }\n      advertisers {\n        office {\n          name\n          phones {\n            number\n            type\n            primary\n            trackable\n            ext\n          }\n        }\n        phones {\n          number\n          type\n          primary\n          trackable\n          ext\n        }\n      }\n      flags {\n        is_new_listing\n      }\n      location {\n        address {\n          line\n          city\n          coordinate {\n            lat\n            lon\n          }\n          country\n          state_code\n          postal_code\n        }\n        county {\n          name\n          fips_code\n        }\n      }\n      description {\n        beds\n        beds_max\n        beds_min\n        baths\n        baths_min\n        baths_max\n        baths_full\n        baths_full_calc\n        baths_half\n        baths_3qtr\n        baths_1qtr\n        garage\n        garage_min\n        garage_max\n        sqft\n        sqft_max\n        sqft_min\n        name\n        sub_type\n        type\n        year_built\n      }\n      units {\n        availability {\n          date\n        }\n        description {\n          baths\n          beds\n          sqft\n        }\n        list_price\n      }\n      branding {\n        type\n        photo\n        name\n      }\n      source {\n        id\n        community_id\n        type\n        feed_type\n      }\n      products {\n        products\n      }\n    }\n  }\n}\n",' \
               r'"variables":{"geoSupportedSlug":"","query":{"unique":true,"status":["for_rent"],"state_code":"TX","type":["apartment"],"pending":false},"limit":200,"offset":0,"bucket":{"sort":"rentalModelV2_1","sort_options":{"costar_total":0,"non_costar_total":0,"variation":"costar_basic"}}},' \
               r'"seoPayload":{"asPath":"/apartments/Texas","pageType":{"silo":"search_result_page","status":"for_rent"},"county_needed_for_uniq":false}}'
        json_body = json.loads(body)

        # json_body["variables"]["page_index"] = page_number
        json_body["seoPayload"]['asPath'] = asPath
        json_body["variables"]['limit'] = limit
        json_body["variables"]['offset'] = offset
        json_body["variables"]["query"]["state_code"] = state_code
        # pprint(json_body)

        r = requests.post(url=url, json=json_body, headers=headers)
        pprint(r.json())
        # r.json()
        json_data = r.json()
        return json_data

    def extract_features(self, entry: dict) -> dict:
        pict = [i['href'] for i in entry["photos"]]

        feature_dict = {
            # "id": entry["property_id"],
            "price": entry["list_price"],
            "min_price": entry["list_price_min"],
            "max_price": entry["list_price_max"],

            # 'pet_policy_text': entry["pet_policy"].get('text'),
            "beds": entry["description"]["beds"],
            "min_beds": entry["description"]["beds_min"],
            "max_beds": entry["description"]["beds_max"],
            "baths": entry["description"]["baths"],
            "min_baths": entry["description"]["baths_min"],
            "max_baths": entry["description"]["baths_max"],
            # "garage": entry["description"]["garage"],
            # "stories": entry["description"]["stories"],
            "house_type": entry["description"]["type"],
            # "lot_sqft": entry["description"]["lot_sqft"],
            # "sqft": entry["description"]["sqft"],
            # "year_built": entry["description"]["year_built"],
            "address": entry["location"]["address"]["line"],
            "postal_code": entry["location"]["address"]["postal_code"],
            "state": entry["location"]["address"]["state_code"],
            "city": entry["location"]["address"]["city"],
            # "tags": entry["tags"],
            "pictures": pict[0].replace('s.jpg', 'od-w480_h360_x2.webp'),
            "pictures1": pict[1].replace('s.jpg', 'od-w480_h360_x2.webp'),
            'permalink': entry["permalink"],
        }
        if isinstance(entry["pet_policy"], dict):
            feature_dict.update({'cats': bool(entry["pet_policy"].get('cats')),
                                 'dogs': bool(entry["pet_policy"].get('dogs')), })
        else:
            feature_dict.update({'cats': None,
                                 'dogs': None})
        # if entry["location"]["address"]["coordinate"]:
        #     feature_dict.update({"lat": entry["location"]["address"]["coordinate"]["lat"]})
        #     feature_dict.update({"lon": entry["location"]["address"]["coordinate"]["lon"]})

        # if entry["location"]["county"]:
        #     feature_dict.update({"county": entry["location"]["county"]["name"]})
        # pprint(feature_dict)
        return feature_dict

    def parse_json_data(self) -> list:
        limit = 42
        offset = 0

        feature_dict_list = []

        for state_code, asPath in self.locations:
            print(state_code, asPath, len(self.all))
            for x in range(9):
                if not x:
                    offset += limit
                    asPath += f'/pg-{x + 1}'
                else:
                    offset = 0
                json_data = self.send_request(state_code, asPath, limit, offset)
                # print(json_data["data"]["home_search"]["properties"])
                try:
                    for entry in json_data["data"]["home_search"]["properties"]:
                        feature_dict = self.extract_features(entry)
                        # if len(feature_dict_list) > 100:
                        #     break
                        # if feature_dict['price'] or feature_dict['min_price'] or feature_dict['max_price']:
                        # feature_dict_list.append(feature_dict)
                        self.all.append(feature_dict)
                        # else:
                        #     continue
                except Exception as e:
                    # print(e)
                    pass

        return self.all

    def create_dataframe(self) -> pd.DataFrame:
        feature_dict_list = self.parse_json_data()
        print(len(feature_dict_list))

        self.df = pd.DataFrame(feature_dict_list)
        # dummy_df = pd.get_dummies(df['tags'].explode()).groupby(level=0).sum()
        #
        # merged_df = pd.merge(df, dummy_df, left_index=True, right_index=True)
        return self.save_to_csv()

    def save_to_csv(self):
        self.df.to_csv('Total_new.csv', index=False)
        print(tabulate(self.df.head(10), headers=self.df.columns))
        return self.df


if __name__ == "__main__":
    asPath = lambda x: f"/apartments/{x}"
    all_cities = [('TX', asPath('Texas')), ('NY', asPath('Manhattan')), ('NY', asPath('New-York')),
                  ('CO', asPath('Colorado')), ('OH', asPath('Ohio')), ('WY', asPath('Wyoming')),
                  ('FL', asPath('Florida'))]
    # all_cities = [('FL', asPath('Florida'))]
    r = RealtorScraper(all_cities)
    r.create_dataframe()
