import json

from PlayStoreScraper import play_store_scraper

def main():
    app_scraper = play_store_scraper.PlayStoreAppDetails()
    result = app_scraper.app("com.chess")
    with open("SampleScraperOutputs/parsed_app_details.json", "w") as f:
        json.dump(result, f)


if __name__ == '__main__':
    main()