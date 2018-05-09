import dbtools
import dictionaries
import helpers


def define_types():
    items = dbtools.get_text_for_type_definition()

    text_list = helpers.get_list_by_list_object_key(items, 'text')
    ids = helpers.get_list_by_list_object_key(items, 'id')

    types = dictionaries.keywords_in_type[0]
    types_keywords = dictionaries.keywords_in_type[1]

    for text in text_list:
        areas = []
        for words in types_keywords:
            for word in words:
                if word in text:
                    print(word)
                    areas.append(types[types_keywords.index(words)])
                    break
        dbtools.set_areas_for_document(ids[text_list.index(text)], areas)
