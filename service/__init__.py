from persistence import user_repository_bean
from service.translation_service import TranslationService
from service.translation_service_holder import TranslationServiceHolder
from service.user_service import UserService

user_service_bean = UserService(user_repository=user_repository_bean)

it_translation_service_bean = TranslationService(language="it",
                                                 flag="🇮🇹")
en_translation_service_bean = TranslationService(language="en",
                                                 flag="🇬🇧")
es_translation_service_bean = TranslationService(language="es",
                                                 flag="🇪🇸")
fr_translation_service_bean = TranslationService(language="fr",
                                                 flag="🇫🇷")
de_translation_service_bean = TranslationService(language="de",
                                                 flag="🇩🇪")

translation_service_holder_bean = TranslationServiceHolder(translators=[
    it_translation_service_bean,
    en_translation_service_bean,
    es_translation_service_bean,
    fr_translation_service_bean,
    de_translation_service_bean
])
