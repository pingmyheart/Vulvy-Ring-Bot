from zoneinfo import ZoneInfo

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from configuration import bot
from scheduling.birthday_notification_scheduler import BirthdayNotificationScheduler
from scheduling.ring_notification_scheduler import RingNotificationScheduler
from scheduling.ring_reminder_notification_scheduler import RingReminderNotificationScheduler
from service import user_service_bean, ring_service_bean
from util import constant_bean

ring_notification_scheduler_bean = RingNotificationScheduler(user_service_bean=user_service_bean,
                                                             ring_service_bean=ring_service_bean,
                                                             constant_bean=constant_bean,
                                                             tg_bot=bot)

ring_reminder_notification_scheduler_bean = RingReminderNotificationScheduler(user_service_bean=user_service_bean,
                                                                              ring_service_bean=ring_service_bean,
                                                                              constant_bean=constant_bean,
                                                                              tg_bot=bot)
birthday_notification_scheduler_bean = BirthdayNotificationScheduler(user_service_bean=user_service_bean,
                                                                     constant_bean=constant_bean,
                                                                     tg_bot=bot)

# Initialize the scheduler
scheduler = BackgroundScheduler(timezone=ZoneInfo("UTC"))
cron_expr_every_minute = CronTrigger.from_crontab("* * * * *")
cron_expr_every_morning = CronTrigger.from_crontab("* * * * *")
scheduler.add_job(ring_notification_scheduler_bean.schedule, cron_expr_every_minute)
scheduler.add_job(ring_reminder_notification_scheduler_bean.schedule, cron_expr_every_minute)
scheduler.add_job(birthday_notification_scheduler_bean.schedule, cron_expr_every_morning)
scheduler.start()
