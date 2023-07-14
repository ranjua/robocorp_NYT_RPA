from RPA.HTTP import HTTP

from utils.logger import logger

from dateutil.relativedelta import relativedelta
import calendar, re
from datetime import datetime

def get_daterange_str(months_back=1, format="%m/%d/%Y"):
    if not isinstance(months_back, int) or months_back < 0:
        months_back = 0
    
    current_date = datetime.now()
    _, last_day = calendar.monthrange(current_date.year, current_date.month)
    first_day_date = current_date.replace(day=1)
    end_date = current_date.replace(day=last_day)

    if months_back > 1:
        first_day_date = current_date - relativedelta(months=months_back-1, day=1)

    return first_day_date.strftime(format), end_date.strftime(format)
    

def contains_money(text):
    pattern = r'\$\d+(?:,\d+)?(?:\.\d+)?|\d+(?:,\d+)?\s?(?:dollars|USD)'
    if re.search(pattern, text):
        return True
    else:
        return False

def count_search_phrase(search_phrase, text):
    return text.lower().count(search_phrase.lower())

def download_image(url, file_path, max_retries=3):
    http = HTTP()
    retry_count = 0
    while retry_count < max_retries:
        try:
            http.download(url, target_file=file_path, overwrite=True)
            # Download successful, exit the loop
            break
        except Exception as e:
            logger.info(f"Error downloading image: {str(e)}")
            logger.info(f"Retrying: ({retry_count}/{max_retries})")
            retry_count += 1
    
    if retry_count >= max_retries:
        logger.error("Max retries exceeded. Unable to download the image.")

def clean_string_for_filename(input_string):
    # Remove non-alphanumeric characters
    alphanumeric_string = re.sub(r'[^a-zA-Z0-9\s]', '', input_string)
    # Replace spaces
    cleaned_string = alphanumeric_string.replace(' ', '_')
    return cleaned_string


def get_test_data():
    return [
        {'title': 'Taking a Late-in-Life Victory Lap, Thanks to His Novels Lunatic Energy', 'date': 'June 16', 'description': "Robert Plunket's 1983 novel, My Search for Warren Harding, was out of print for decades  but remained stealthily influential. Its reissue has catapulted him out of retirement.", 'picture_filename': 'https://static01.nyt.com/images/2023/06/16/multimedia/16Plunket2-mcgp/16Plunket2-mcgp-threeByTwoSmallAt2X.jpg?quality=75&auto=webp&disable=upscale', 'count_search_phrase': 0, 'contains_money': True},
        {'title': 'In the Search for Latin Americas Disappeared, Memories and Evidence Entwine', 'date': 'March 14', 'description': 'In Still Life With Bones, the anthropologist Alexa Hagerty describes how she learned to see the dead with a forensic eye  and to listen to the living.', 'picture_filename': 'output/images/IntheSearchforLatinAmericasDisappearedMemoriesandEvidenceEntwine.png', 'count_search_phrase': 0, 'contains_money': False},
        {'title': 'Learning to Hear What the Dead Have to Say', 'date': 'March 16', 'description': 'In Still Life With Bones, Alexa Hagerty recounts her training in the science of forensic exhumation at mass grave sites in Guatemala and Argentina  and what such work means for the families of victims.', 'picture_filename': 'output/images/LearningtoHearWhattheDeadHavetoSay.png', 'count_search_phrase': 1, 'contains_money': False}
    ]