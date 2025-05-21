from service import translation_service_holder_bean
from util.contant import Constant
from util.message_util import MessageUtil
from util.timezone_util import generate_timezones

timezone_list = generate_timezones()
constant_bean = Constant(translation_holder=translation_service_holder_bean)
message_util_bean = MessageUtil()
