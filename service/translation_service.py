import javaproperties

from configuration import base_directory


class TranslationService:
    def __init__(self, language: str,
                 flag: str):
        self.language = language
        self.flag = flag
        self.properties = {}
        with open(f'{base_directory}/resources/translation-{language}.properties', 'r', encoding="iso-8859-1") as file:
            self.properties = javaproperties.load(file)

    def find_translation(self, i18n_key: str):
        return self.properties.get(i18n_key, None)

    def get_flag(self):
        return self.flag
