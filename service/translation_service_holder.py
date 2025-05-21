from service.translation_service import TranslationService


class TranslationServiceHolder:
    def __init__(self, translators: list[TranslationService]):
        self.__list_translator = translators

    def get_translators(self) -> list[TranslationService]:
        return self.__list_translator

    def find_translation(self, lang: str, i18n_key: str) -> str:
        i18n_service: TranslationService = self.__hold(lang)
        if i18n_service is not None:
            return i18n_service.find_translation(i18n_key=i18n_key)
        return str(None)

    def __hold(self, lang: str) -> TranslationService:
        return next((translator for translator in self.__list_translator if translator.language == lang), None)
