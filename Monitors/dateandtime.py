"""
DateAndTime Monitor
"""

# TODO: Add init to set update_interval for seconds, minutes, hours, days
# TODO: Need isy object defined when start is called...

from .monitor import Monitor
from datetime import datetime

class DateAndTime(Monitor):

    def second_function(self):
        print('second_function: The time is: %s' % datetime.now())

    def minute_function(self):
        self.parent.logger.info('minute_function: The minute is: %s' % datetime.now().minute)
        self.parent.isy.variables[2]['s.PyISY.Minute'].val = datetime.now().minute

    def hour_function(self):
        self.parent.logger.info('hour_function: The hour is: %s' % datetime.now().hour)
        self.parent.isy.variables[2]['s.PyISY.Hour'].val = datetime.now().hour

    def day_function(self):
        dt = datetime.now()
        self.parent.logger.info('day_function: It is a new day!  The time is: %s' % dt)
        self.parent.isy.variables[2]['s.PyISY.Day'].val = dt.day
        self.parent.isy.variables[2]['s.PyISY.Month'].val = dt.month
        self.parent.isy.variables[2]['s.PyISY.Year'].val = dt.year

    def start(self):
        #super(DateAndTime, self).start()
        # Initialize all on startup
        #self.minute_function()
        #self.hour_function()
        #self.day_function()
        # Schedules second_function to be run at the change of each second.
        #self.parent.sched.add_job(second_function, 'cron', second='0-59')
        # Schedules minute_function to be run at the change of each minute.
        self.parent.sched.add_job(self.minute_function, 'cron', second='0')
        # Schedules hour_function to be run at the change of each hour.
        self.parent.sched.add_job(self.hour_function, 'cron', minute='0', second='0')
        # Schedules day_function to be run at the start of each day.
        self.parent.sched.add_job(self.day_function, 'cron', minute='0', second='0', hour='0')
