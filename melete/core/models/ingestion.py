from django.db import models


class TickLoad(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    start_date = models.DateTimeField(db_column='start_date')
    end_date = models.DateTimeField(db_column='end_date')
    tick_type = models.ForeignKey('TickType', on_delete=models.DO_NOTHING, db_column='tick_type_id')
    ticker = models.ForeignKey('Ticker', on_delete=models.DO_NOTHING, db_column='ticker_id')

    class Meta:
        managed = True
        db_table = 'tick_load'

    def __str__(self):
        return "Tick Load: %s(%s) [%s-%s]" % (self.ticker, self.tick_type, self.start_date, self.end_date)


class ThreadLoad(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    start_date = models.DateTimeField(db_column='start_date')
    end_date = models.DateTimeField(db_column='end_date')
    thread = models.ForeignKey('Thread', on_delete=models.DO_NOTHING, db_column='thread_id')

    class Meta:
        managed = True
        db_table = 'thread_load'

    def __str__(self):
        return "Thread Load: %s [%s-%s]" % (self.thread, self.start_date, self.end_date)


class WebsiteLoad(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    start_date = models.DateTimeField(db_column='start_date')
    end_date = models.DateTimeField(db_column='end_date')
    website = models.ForeignKey('Website', on_delete=models.DO_NOTHING, db_column='website_id')

    class Meta:
        managed = True
        db_table = 'website_load'

    def __str__(self):
        return "Website Load: %s [%s-%s]" % (self.website, self.start_date, self.end_date)


class ThreadSeriesLoad(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    start_date = models.DateTimeField(db_column='start_date')
    end_date = models.DateTimeField(db_column='end_date')
    thread_series = models.ForeignKey('ThreadSeries', on_delete=models.DO_NOTHING, db_column='thread_series_id')

    class Meta:
        managed = True
        db_table = 'thread_series_load'

    def __str__(self):
        return "Thread-Series Load: %s [%s-%s]" % (self.thread_series, self.start_date, self.end_date)
