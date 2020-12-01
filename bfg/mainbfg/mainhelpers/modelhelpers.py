from django.core.cache import cache

from mainbfg.models import (TypeSentence, Categories, Regions, Sentence)


class ModelHelpers():
  """
    Get data for TypeSentence, Categories, Regions(CTR) - staticmethod
    """

  def get_data_ctr():
    if cache.get('data_ctr'):
      return cache.get('data_ctr')
    else:
      data = {}
      data['types'] = TypeSentence.objects.get_active_types()
      data['categories'] = Categories.objects.get_active_categories()
      data['categories_list'] = Categories.objects.get_list_categories()
      data['regions'] = Regions.objects.get_all_regions()
      cache.set('data_ctr', data)

      return data

  """
        Get data for top sentences - staticmethod
    """

  def get_top_sentences():
    return Sentence.objects.get_top_sentences_start_page()
