from django.db import models


class ModelConfig(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', null=False, max_length=255)
    description = models.CharField(db_column='description', null=True, max_length=510)
    params = models.TextField(db_column='params', null=False)
    version = models.CharField(db_column='version', null=False, max_length=20)

    class Meta:
        managed = True
        db_table = 'model_config'

    def __str__(self):
        return self.name + " - " + self.version


class Model(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    model_config = models.ForeignKey('ModelConfig', models.DO_NOTHING, db_column='model_config_id')
    created_date = models.DateTimeField(db_column='created_date', null=True)
    last_seen_date = models.DateTimeField(db_column='last_seen_date', null=False)
    last_trained_date = models.DateTimeField(db_column='last_trained_date', null=False)
    last_tested_date = models.DateTimeField(db_column='last_tested_date', null=False)
    file_path = models.CharField(db_column='file_path', null=False, max_length=10000)
    keras_json = models.TextField(db_column='keras_json', null=True)

    class Meta:
        managed = True
        db_table = 'model'

    def __str__(self):
        return "%s - %s" % (self.id, self.created_date)


class DataframeManager(models.Manager):

    @staticmethod
    def tickers(dataframe, relation='in'):
        return [
            x.ticker.id for x in
            DataframeTicker.objects.filter(dataframe=dataframe, relation=relation)
        ]

    @staticmethod
    def tick_types(dataframe, relation='in'):
        return [
            x.tick_type.id for x in
            DataframeTickType.objects.filter(dataframe=dataframe, relation=relation)
        ]


class Dataframe(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', null=False, max_length=255)
    description = models.CharField(db_column='description', null=True, max_length=510)
    params = models.TextField(db_column='params', null=False)
    objects = DataframeManager()

    class Meta:
        managed = True
        db_table = 'dataframe'

    def __str__(self):
        return self.name


class ModelConfigDataframe(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    model_config = models.ForeignKey('ModelConfig', on_delete=models.DO_NOTHING, db_column='model_config_id')
    dataframe = models.ForeignKey('Dataframe', on_delete=models.DO_NOTHING, db_column='dataframe_id')

    class Meta:
        managed = True
        db_table = 'model_config_dataframe'
        unique_together = (('model_config', 'dataframe'),)

    def __str__(self):
        return str(self.id)


class ModelDataframe(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    model = models.ForeignKey('Model', on_delete=models.DO_NOTHING, db_column='model_id')
    dataframe = models.ForeignKey('Dataframe', on_delete=models.DO_NOTHING, db_column='dataframe_id')

    class Meta:
        managed = True
        db_table = 'model_dataframe'
        unique_together = (('model', 'dataframe'),)

    def __str__(self):
        return str(self.id)


class DataframeTicker(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    ticker = models.ForeignKey('Ticker', on_delete=models.DO_NOTHING, db_column='entity_id')
    dataframe = models.ForeignKey('Dataframe', on_delete=models.DO_NOTHING, db_column='dataframe_id')
    relation = models.CharField(db_column='relation', max_length=32, null=False)

    class Meta:
        managed = True
        db_table = 'dataframe_ticker'
        unique_together = (('ticker', 'dataframe'),)

    def __str__(self):
        return str(self.id)


class DataframeTickType(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    tick_type = models.ForeignKey('TickType', on_delete=models.DO_NOTHING, db_column='tick_type_id')
    dataframe = models.ForeignKey('Dataframe', on_delete=models.DO_NOTHING, db_column='dataframe_id')
    relation = models.CharField(db_column='relation', max_length=32, null=False)

    class Meta:
        managed = True
        db_table = 'dataframe_tick_type'
        unique_together = (('tick_type', 'dataframe'),)

    def __str__(self):
        return str(self.id)


class ErrorType(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', null=False, max_length=255)
    description = models.CharField(db_column='description', null=True, max_length=510)

    class Meta:
        managed = True
        db_table = 'error_type'

    def __str__(self):
        return self.name


class PredictionSet(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    date_created = models.DateTimeField(db_column='date_created', null=True)
    error = models.FloatField(db_column='error', null=False)
    model = models.ForeignKey('Model', on_delete=models.DO_NOTHING, db_column='model_id')
    # errortypeid = models.ForeignKey('ErrorType', models.DO_NOTHING, db_column='ErrorType_id')
    entity = models.ForeignKey('Entity', on_delete=models.DO_NOTHING, db_column='entity_id')

    class Meta:
        managed = True
        db_table = 'prediction_set'

    def __str__(self):
        return str(self.id)


class Prediction(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    value = models.FloatField(db_column='value', null=False)
    tick_type = models.ForeignKey('TickType', on_delete=models.DO_NOTHING, db_column='tick_type_id')
    prediction_set = models.ForeignKey('PredictionSet',
                                       on_delete=models.DO_NOTHING,
                                       db_column='prediction_set_id',
                                       related_name='predictions'
                                       )

    class Meta:
        managed = True
        db_table = 'prediction'

    def __str__(self):
        return str(self.id)


class Metric(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name',  null=False, max_length=255)
    description = models.CharField(db_column='description',  null=False, max_length=510)
    metrics = models.ManyToManyField("self",
                                     through='MetricMetric',
                                     through_fields=('parent_metric_id', 'child_metric_id'),
                                     symmetrical=False
                                     )

    class Meta:
        managed = True
        db_table = 'metric'

    def __str__(self):
        return str(self.name)


class Score(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    value = models.FloatField(db_column='value', null=False)
    prediction_set = models.ForeignKey(PredictionSet, on_delete=models.DO_NOTHING, db_column='prediction_set_id')
    metric = models.ForeignKey(Metric, on_delete=models.DO_NOTHING, db_column='metric_id')

    class Meta:
        managed = True
        db_table = 'score'

    def __str__(self):
        return str(self.id)


class MetricMetric(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    parent_metric = models.ForeignKey(Metric,
                                      on_delete=models.DO_NOTHING,
                                      db_column='parent_metric_id',
                                      related_name='parent_metric_id'
                                      )
    child_metric = models.ForeignKey(Metric,
                                     on_delete=models.DO_NOTHING,
                                     db_column='child_metric_id',
                                     related_name='child_metric_id'
                                     )

    class Meta:
        managed = True
        db_table = 'metric_metric'

    def __str__(self):
        return str(self.id)
