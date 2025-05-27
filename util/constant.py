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

    def select_configuration_option(self, lang: str) -> str:
        return self.__translation_holder.find_translation(lang=lang,
                                                          i18n_key="response.selectConfigurationOption")

    def welcome_message(self, lang: str):
        return self.__translation_holder.find_translation(lang=lang,
                                                          i18n_key="response.welcome")

    def date_not_available(self, lang: str):
        return self.__translation_holder.find_translation(lang=lang,
                                                          i18n_key="response.dateNotAvailable")

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

    def ring_placeholder(self, lang: str):
        return self.__translation_holder.find_translation(lang=lang,
                                                          i18n_key="placeholder.ring")

    def user_placeholder(self, lang: str):
        return self.__translation_holder.find_translation(lang=lang,
                                                          i18n_key="placeholder.user")

    def insertion_date(self, lang: str):
        return self.__translation_holder.find_translation(lang=lang,
                                                          i18n_key="response.insertionDate")

    def insertion_date_time_placeholder(self, lang: str):
        return self.__translation_holder.find_translation(lang=lang,
                                                          i18n_key="placeholder.insertion.dateTime")

    def location_for_timezone_placeholder(self, lang: str):
        return self.__translation_holder.find_translation(lang=lang,
                                                          i18n_key="placeholder.locationForTimeZone")

    def timezone_correctly_settled(self, lang: str):
        return self.__translation_holder.find_translation(lang=lang,
                                                          i18n_key="response.timezoneSet")

    def timezone_set_error(self, lang: str):
        return self.__translation_holder.find_translation(lang=lang,
                                                          i18n_key="response.timezoneSetError")

    def insertion_time(self, lang: str):
        return self.__translation_holder.find_translation(lang=lang,
                                                          i18n_key="response.insertionTime")

    def choose_option(self, lang: str):
        return self.__translation_holder.find_translation(lang=lang,
                                                          i18n_key="response.chooseOption")

    def invalid_date(self, lang: str):
        return self.__translation_holder.find_translation(lang=lang,
                                                          i18n_key="response.invalidDate")

    def invalid_time(self, lang: str):
        return self.__translation_holder.find_translation(lang=lang,
                                                          i18n_key="response.invalidTime")

    def ring_date_accepted(self, lang: str):
        return self.__translation_holder.find_translation(lang=lang,
                                                          i18n_key="response.acceptDate")

    def ring_time_accepted(self, lang: str):
        return self.__translation_holder.find_translation(lang=lang,
                                                          i18n_key="response.acceptTime")

    def ring_insert(self, lang: str):
        return self.__translation_holder.find_translation(lang=lang,
                                                          i18n_key="enum.ring.inserted")

    def ring_remove(self, lang: str):
        return self.__translation_holder.find_translation(lang=lang,
                                                          i18n_key="enum.ring.removed")

    def time_to_insert_ring(self, lang: str):
        return self.__translation_holder.find_translation(lang=lang,
                                                          i18n_key="response.timeToInsertRing")

    def tomorrow_ring_insertion(self, lang: str):
        return self.__translation_holder.find_translation(lang=lang,
                                                          i18n_key="response.timeToInsertRing.tomorrow")

    def time_to_remove_ring(self, lang: str):
        return self.__translation_holder.find_translation(lang=lang,
                                                          i18n_key="response.timeToRemoveRing")

    def tomorrow_ring_removal(self, lang: str):
        return self.__translation_holder.find_translation(lang=lang,
                                                          i18n_key="response.timeToRemoveRing.tomorrow")

    def happy_birthday(self, lang: str):
        return self.__translation_holder.find_translation(lang=lang,
                                                          i18n_key="response.happyBirthday")
