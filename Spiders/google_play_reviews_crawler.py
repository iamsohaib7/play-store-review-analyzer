import json

from PlayStoreScraper import play_store_scraper
from PlayStoreScraper.constants import date_serializer

def main():
    app_details = play_store_scraper.PlayStoreReviews()
    result, _ = app_details.reviews("com.chess")
    with open("SampleScraperOutputs/parsed_app_reviews.json", "w") as f:
        json.dump(result, f, default=date_serializer.json_serial)


if __name__ == '__main__':
    main()

