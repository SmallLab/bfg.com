from mainbfg.models import (Categories, TypeSentence, Regions)

"""
    Return data for TypeSentence, Categories, Regions
"""
def get_tcr_data():
    return TypeSentence.objects.get_active_types(), \
           Categories.objects.get_active_categories(), \
           Regions.objects.get_all_regions()
