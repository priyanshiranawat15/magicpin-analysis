from Extractor.extractor import Extractor

with Extractor() as e:
    e.landing_page()
    e.click_dropdowns()
    e.extract_soup_object()



