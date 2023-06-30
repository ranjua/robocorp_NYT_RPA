class Locators_NYT():

    #page load
    ICON_PAGE_LOADED = '//*[@data-testid="todays-date"]'
    GDPR_REJECT = '//*[@data-testid="GDPR-reject"]'
    
    #Basic Search
    ICON_BASIC_SEARCH = '//*[@data-test-id="search-button"]'
    ICON_BASIC_SEARCH_MOBILE = '//*[@data-testid="nav-button"]'
    TXT_BASIC_SEARCH = '//input[@data-testid="search-input"]'
    TXT_BASIC_SEARCH_MOBILE = TXT_BASIC_SEARCH
    BTN_BASIC_SEARCH = '//*[@data-test-id="search-submit"]'
    BTN_BASIC_SEARCH_MOBILE = BTN_BASIC_SEARCH

    #Advanced Search
    #Dates
    BTN_ADV_DATE = '//button[@data-testid="search-date-dropdown-a"]'
    BTN_ADV_SPFC_DATE = '//button[@value="Specific Dates"]'
    TXT_ADV_START_DATE = '//*[@id="startDate"]'
    TXT_ADV_END_DATE = '//*[@id="endDate"]'

    #Sections
    BTN_ADV_SECTION = '//div[@data-testid="section"]/button[@data-testid="search-multiselect-button"]'
    LIST_ADV_SECTION = '//div[@data-testid="section"]/div/ul[@data-testid="multi-select-dropdown-list"]'
    CHKBOX_ADV_SECTION = '//div[@data-testid="section"]/div/ul[@data-testid="multi-select-dropdown-list"]/li/label/span[text()="$$Q$$"]/../input[@type="checkbox"]'
    
    #Types
    BTN_ADV_TYPE = '//div[@data-testid="type"]/button[@data-testid="search-multiselect-button"]'
    LIST_ADV_TYPE = '//div[@data-testid="type"]/div/ul[@data-testid="multi-select-dropdown-list"]'
    CHKBOX_ADV_TYPE = '//div[@data-testid="type"]/div/ul[@data-testid="multi-select-dropdown-list"]/li/label/span[text()="$$Q$$"]/../input[@type="checkbox"]'
    
    #Sort
    SLC_ADV_SORT = '//select[@data-testid="SearchForm-sortBy"]'
    
    #Results
    LBL_RESULTS = '//p[@data-testid="SearchForm-status"]'

    #Expand
    BTN_EXP_RSLT = '//button[@data-testid="search-show-more-button"]'
#//*[@id="site-content"]/div/div[2]/div[2]/ol/li[1]/div/div/div/a/h4
    #news
    LIST_NEWS_CONTAINER = '//ol[@data-testid="search-results"]/li[@data-testid="search-bodega-result"]'
    DATE_NEWS = 'css:div > span'
    TITLE_NEWS = 'css:div > div > div > a > h4'
    DESCRIPTION_NEWS = 'css:div > div > div > a > p:first-of-type'
    PICTURE_NEWS = 'css:div > div > figure > div > img'
    
    
    def __init__(self):
        pass