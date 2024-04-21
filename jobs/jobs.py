from apscheduler.schedulers.background import BackgroundScheduler

from config import settings


# from app.models import Buyer
#
#
# def myfunc():
#     # write whatever task you want to perform
#     print("HEY")
#
#
# def schedule():
#     scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
#     scheduler.add_job(myfunc, 'interval', seconds=1)
#     scheduler.start()

with open("../mailing.log") as f:
    for line in f:
        print(line.strip().split(" - "))
