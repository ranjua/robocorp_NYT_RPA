from core.nyt_rpa import NYT_RPA
from core.excel_rpa import Excel_RPA
from RPA.Robocorp.WorkItems import WorkItems
import utils.helpers as helpers
import os
import datetime


def main():
    try:
        # Config
        wi = WorkItems()
        wi.get_input_work_item()
        search_phrase = wi.get_work_item_variable("search_phrase")
        helpers.logger.info(search_phrase)
        months_back = wi.get_work_item_variable("months_back")
        helpers.logger.info(months_back)
        sections = wi.get_work_item_variable("sections")
        helpers.logger.info(sections)

        limit = 100
        if len(search_phrase) > limit:
            search_phrase = search_phrase[:limit]

        types = None  # ["Article","Audio"]
        sortBy = "newest"
        start_date, end_date = helpers.get_daterange_str(months_back)
        config = {
            "start_date": start_date,
            "end_date": end_date,
            "sections": sections,
            "types": types,
            "sortBy": sortBy,
            "init_url": "http://www.nytimes.com/"
        }

        # RPA NYT To collect news
        nyt_rpa = NYT_RPA(
            timeout=60, speed=3, auto_close=True, screenshot_directory="output", **config
        )
        collected_news, success = nyt_rpa.get_news_from(search_phrase, max_retries=3)
        #success = True
        #collected_news = helpers.get_test_data()
        if success:
            #If success, news can be empty or a list of news.
            if collected_news:
                # RPA to write collections in Excel file
                excel_rpa = Excel_RPA()
                filename = helpers.clean_string_for_filename(
                    start_date
                    + " "
                    + end_date
                    + " "
                    + search_phrase
                    + " "
                    + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                )
                folder_path = "output"
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                excel_rpa.save_collection(
                    name=folder_path + "/" + filename + ".xlsx", collection=collected_news
                )
            else:
                helpers.logger.info("Empty search, with the current parameters.")
        else:
            #If not success, means something was wrong.
            helpers.logger.error("Exit with error.")
    except Exception as e:
        # Other errors.
        helpers.logger.critical(e)


# Call the main() function, checking that we are running as a stand-alone script:
if __name__ == "__main__":
    main()
