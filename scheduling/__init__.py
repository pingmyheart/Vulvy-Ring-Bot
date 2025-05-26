from zoneinfo import ZoneInfo

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from configuration import bot
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

scheduler = BackgroundScheduler(timezone=ZoneInfo("UTC"))
cron_expr = CronTrigger.from_crontab("* * * * *")
scheduler.add_job(ring_notification_scheduler_bean.schedule, cron_expr)
scheduler.add_job(ring_reminder_notification_scheduler_bean.schedule, cron_expr)
scheduler.start()
