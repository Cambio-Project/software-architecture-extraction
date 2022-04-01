import random
from util.log import warning
from util.text.languages import LanguageConfig, TEXT


def text(text_id: int):
    if LanguageConfig.LANGUAGE not in TEXT:
        LanguageConfig.LANGUAGE = 'en'
        warning('Fallback to default language "en" since {} does not exist.'.format(LanguageConfig.LANGUAGE))

    if text_id in TEXT[LanguageConfig.LANGUAGE]:
        return TEXT[LanguageConfig.LANGUAGE][text_id]
    else:
        return 'NO TEXT ID "{}"'.format(text_id)


def random_text(text_id: int) -> str:
    result = text(text_id)
    return random_selection(result)


def random_selection(selection) -> str:
    if len(selection) > 0:
        return selection[random.randint(0, max(0, len(selection) - 1))]
    return ''
