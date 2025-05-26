from command_handler.calendar_command_handler import CalendarCommandHandler
from command_handler.configure_command_handler import ConfigureCommandHandler
from command_handler.help_command_handler import HelpCommandHandler
from command_handler.language_command_handler import LanguageCommandHandler
from command_handler.location_command_handler import LocationCommandHandler
from command_handler.start_command_handler import StartCommandHandler
from configuration import bot
from service import ring_service_bean, user_service_bean
from util import constant_bean, message_util_bean

calendar_command_handler_bean = CalendarCommandHandler(tg_bot=bot,
                                                       constant_bean=constant_bean,
                                                       ring_service_bean=ring_service_bean,
                                                       user_service_bean=user_service_bean)

configure_command_handler_bean = ConfigureCommandHandler(tg_bot=bot,
                                                         constant_bean=constant_bean,
                                                         ring_service_bean=ring_service_bean,
                                                         user_service_bean=user_service_bean)

help_command_handler_bean = HelpCommandHandler(tg_bot=bot,
                                               constant_bean=constant_bean,
                                               ring_service_bean=ring_service_bean,
                                               user_service_bean=user_service_bean)

start_command_handler_bean = StartCommandHandler(tg_bot=bot,
                                                 constant_bean=constant_bean,
                                                 ring_service_bean=ring_service_bean,
                                                 user_service_bean=user_service_bean,
                                                 message_util_bean=message_util_bean)

language_command_handler_bean = LanguageCommandHandler(tg_bot=bot,
                                                       constant_bean=constant_bean,
                                                       ring_service_bean=ring_service_bean,
                                                       user_service_bean=user_service_bean,
                                                       message_util_bean=message_util_bean)

location_command_handler_bean = LocationCommandHandler(tg_bot=bot,
                                                       constant_bean=constant_bean,
                                                       ring_service_bean=ring_service_bean,
                                                       user_service_bean=user_service_bean)
