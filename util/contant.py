from service import TranslationServiceHolder


class Constant:
    def __init__(self, translation_holder: TranslationServiceHolder):
        self.__translation_holder: TranslationServiceHolder = translation_holder

    @staticmethod
    def parser():
        return "Markdown"

    def select_language(self, lang: str = None) -> str:
        if lang is None:
            response = ""
            for translator in self.__translation_holder.get_translators():
                response += f"{translator.flag} {translator.find_translation(i18n_key='response.selectLanguage')}\n\n"
            return response
        else:
            return self.__translation_holder.find_translation(lang=lang,
                                                              i18n_key="response.selectLanguage")

    def welcome_message(self, lang: str):
        return self.__translation_holder.find_translation(lang=lang,
                                                          i18n_key="response.welcome")

    def fallback(self, lang: str):
        return self.__translation_holder.find_translation(lang=lang,
                                                          i18n_key="response.fallback")

    def unknown_option(self, lang: str):
        return self.__translation_holder.find_translation(lang=lang,
                                                          i18n_key="response.unknownOption")

    def language_settled(self, lang: str):
        return self.__translation_holder.find_translation(lang=lang,
                                                          i18n_key="response.languageSettled")

    def service_unavailable(self, lang: str):
        return self.__translation_holder.find_translation(lang=lang,
                                                          i18n_key="response.serviceUnavailable")

    def service_not_implemented(self, lang: str):
        return self.__translation_holder.find_translation(lang=lang,
                                                          i18n_key="response.notImplemented")

    def help_commands(self, lang: str):
        return self.__translation_holder.find_translation(lang=lang,
                                                          i18n_key="response.help")
