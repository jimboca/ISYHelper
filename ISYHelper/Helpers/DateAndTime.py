"""
DateAndTime Monitor
"""

# TODO: Add init to set update_interval for seconds, minutes, hours, days
# TODO: Need isy object defined when start is called...

from datetime import datetime
from .Helper import Helper

class DateAndTime(Helper):

    def __init__(self,parent,hconfig):
        self.optional = { 'interval' : { 'default' : 'minute', 'valid' : ['day', 'hour', 'minute', 'second'] } }
        super(DateAndTime, self).__init__(parent,hconfig)
        self.parent.logger.info("Datetime: interval=" + self.interval)
        # Index of the interval, 0=day, ... 3=second
        self.interval_index = self.optional['interval']['valid'].index(self.interval)

    def second_function(self):
        dt = datetime.now()
        self.parent.logger.info('second_function: The minute is: %s' % dt.second)
        self.Second.val = dt.second

    def minute_function(self):
        dt = datetime.now()
        self.parent.logger.info('minute_function: The minute is: %s' % dt.minute)
        self.Minute.val = dt.minute

    def hour_function(self):
        dt = datetime.now()
        self.parent.logger.info('hour_function: The hour is: %s' % dt.hour)
        self.Hour.val = dt.hour

    def day_function(self):
        dt = datetime.now()
        self.parent.logger.info('day_function: It is a new day!  The time is: %s' % dt)
        self.Day.val = dt.day
        self.Month.val = dt.month
        self.Year.val = dt.year

    # Initialize all on startup
    def start(self):
        # Build our hash of variables
        self.isy_variables = ['Day', 'Month', 'Year']
        if self.interval_index > 0:
            self.isy_variables.append('Hour')
        if self.interval_index > 1:
            self.isy_variables.append('Minute')
        if self.interval_index > 2:
            self.isy_variables.append('Second')
        super(DateAndTime, self).start()
        if self.interval_index > 2:
            self.second_function()
        if self.interval_index > 1:
            self.minute_function()
        if self.interval_index > 0:
            self.hour_function()
        self.day_function()

    def sched(self):
        super(DateAndTime, self).sched()
        # Schedules second_function to be run at the change of each second.
        if self.interval_index > 2:
            self.parent.sched.add_job(self.second_function, 'cron', second='0-59')
        # Schedules minute_function to be run at the change of each minute.
        if self.interval_index > 1:
            self.parent.sched.add_job(self.minute_function, 'cron', second='0')
        # Schedules hour_function to be run at the change of each hour.
        if self.interval_index > 0:
            self.parent.sched.add_job(self.hour_function, 'cron', minute='0', second='0')
        # Schedules day_function to be run at the start of each day.
        self.parent.sched.add_job(self.day_function, 'cron', minute='0', second='0', hour='0')
