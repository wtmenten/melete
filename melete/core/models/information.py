from django.db import models
from encrypted_model_fields.fields import EncryptedCharField


class Article(models.Model):
    id = models.AutoField(db_column='id', primary_key=True),
    title = models.CharField(db_column='title', max_length=510)
    contents = models.TextField(db_column='contents')
    sentiment = models.FloatField(db_column='sentiment', blank=True, null=True)
    polarity = models.FloatField(db_column='polarity', blank=True, null=True)
    subjectivity = models.FloatField(db_column='subjectivity', blank=True, null=True)
    source = models.ForeignKey('Source', on_delete=models.DO_NOTHING, db_column='source_id')
    date = models.DateTimeField(db_column='date')
    date_processed = models.DateTimeField(db_column='date_processed')

    class Meta:
        managed = True
        db_table = 'article'

    def __str__(self):
        return self.title


class ThreadSeries(models.Model):
    id = models.AutoField(db_column='id', primary_key=True),
    source = models.ForeignKey('Source', on_delete=models.DO_NOTHING, db_column='source_id')

    class Meta:
        managed = True
        db_table = 'thread_series'

    def __str__(self):
        return str(self.id)


class Thread(models.Model):
    id = models.AutoField(db_column='id', primary_key=True),
    thread_series = models.ForeignKey('ThreadSeries', on_delete=models.DO_NOTHING, db_column='thread_series_id')
    source = models.ForeignKey('Source', on_delete=models.DO_NOTHING, db_column='source_id')
    date = models.DateTimeField(db_column='date')
    date_processed = models.DateTimeField(db_column='date_processed')

    class Meta:
        managed = True
        db_table = 'thread'

    def __str__(self):
        return str(self.id)


class CommentCollection(models.Model):
    id = models.AutoField(db_column='id', primary_key=True),
    thread = models.ForeignKey('Thread', on_delete=models.DO_NOTHING, db_column='thread_id')
    source = models.ForeignKey('Source', on_delete=models.DO_NOTHING, db_column='source_id')
    date_processed = models.DateTimeField(db_column='date_processed')

    class Meta:
        managed = True
        db_table = 'comment_collection'

    def __str__(self):
        return str(self.id)


class Comment(models.Model):
    id = models.AutoField(db_column='id', primary_key=True),
    text = models.TextField(db_column='contents')
    sentiment = models.FloatField(db_column='sentiment', blank=True, null=True)
    polarity = models.FloatField(db_column='polarity', blank=True, null=True)
    subjectivity = models.FloatField(db_column='subjectivity', blank=True, null=True)
    source = models.ForeignKey('Source', on_delete=models.DO_NOTHING, db_column='source_id')
    date = models.DateTimeField(db_column='date')
    date_processed = models.DateTimeField(db_column='date_processed')
    collection = models.ForeignKey('CommentCollection', on_delete=models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'comment'

    def __str__(self):
        return str(self.id)


class Report(models.Model):
    id = models.AutoField(db_column='id', primary_key=True),
    name = models.CharField(db_column='name', max_length=510)
    description = models.CharField(db_column='description', max_length=1020, blank=True, null=True)
    path = models.CharField(db_column='path', max_length=1020, blank=True, null=True)
    sentiment = models.FloatField(db_column='sentiment', blank=True, null=True)
    polarity = models.FloatField(db_column='polarity', blank=True, null=True)
    subjectivity = models.FloatField(db_column='subjectivity', blank=True, null=True)
    date = models.DateTimeField(db_column='date')
    source = models.ForeignKey('Source', on_delete=models.DO_NOTHING, db_column='source_id')

    class Meta:
        managed = True
        db_table = 'Report'

    def __str__(self):
        return self.name


class Series(models.Model):
    id = models.AutoField(db_column='id', primary_key=True),
    tick_type = models.ForeignKey('TickType', on_delete=models.DO_NOTHING, db_column='tick_type_id')

    class Meta:
        managed = True
        db_table = 'series'

    def __str__(self):
        return "Series %s: %s" % (self.tick_type.name, self.id)


class Tick(models.Model):
    id = models.AutoField(db_column='id', primary_key=True),
    value = models.FloatField(db_column='value')
    tick_type = models.ForeignKey('TickType', on_delete=models.DO_NOTHING, db_column='tick_type_id')
    date = models.DateTimeField(db_column='date')

    class Meta:
        managed = True
        db_table = 'tick'

    def __str__(self):
        return "Tick %s: %s" % (self.tick_type.name, self.id)


class Source(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    type = models.CharField(db_column='type', max_length=255)
    name = models.CharField(db_column='name', max_length=255)
    description = models.CharField(db_column='description', max_length=1020, blank=True, null=True)
    url = models.CharField(db_column='url', max_length=2040)
    website = models.ForeignKey('Website', models.DO_NOTHING, db_column='website_id')

    class Meta:
        managed = True
        db_table = 'source'

    def __str__(self):
        return self.name


class Website(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=255)
    description = models.CharField(db_column='description', max_length=1020, blank=True, null=True)
    url = models.CharField(db_column='url', max_length=2040)
    login_script = models.TextField(db_column='login_script', blank=True, null=True)
    credentials = models.ForeignKey('Credentials',
                                    on_delete=models.DO_NOTHING, db_column='credentials_id', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'website'

    def __str__(self):
        return self.name


class Credentials(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    email = models.CharField(db_column='email', max_length=510)
    username = models.CharField(db_column='username', max_length=255)
    password = EncryptedCharField(db_column='password', max_length=255)

    class Meta:
        managed = True
        db_table = 'credentials'

    def __str__(self):
        return "Credentials: %s" % self.id


class TickType(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=510)
    description = models.CharField(db_column='description', max_length=1020, blank=True, null=True)
    params = models.CharField(db_column='params', max_length=5000, blank=True, null=True)
    fill = models.ForeignKey('Fill', models.DO_NOTHING, db_column="fill_id")
    frequency = models.ForeignKey('Frequency', models.DO_NOTHING, db_column="frequency_id")
    function = models.ForeignKey('Function', models.DO_NOTHING, db_column="function_id")

    class Meta:
        managed = True
        db_table = 'tick_type'

    def __str__(self):
        return self.name


class Fill(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=255)
    description = models.CharField(db_column='description', max_length=255, null=True)

    class Meta:
        managed = True
        db_table = 'fill'

    def __str__(self):
        return self.name


class Frequency(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=255)
    description = models.CharField(db_column='description', max_length=255, null=True)

    class Meta:
        managed = True
        db_table = 'frequency'

    def __str__(self):
        return self.name


class Function(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=255)
    description = models.CharField(db_column='description', max_length=255, null=True)

    class Meta:
        managed = True
        db_table = 'function'

    def __str__(self):
        return self.name


# Associative Entities


class SeriesEntity(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    series = models.ForeignKey('Series',
                               on_delete=models.DO_NOTHING,
                               db_column='series_id',
                               related_name='entity_series'
                               )
    entity = models.ForeignKey('Entity',
                               on_delete=models.DO_NOTHING,
                               db_column='entity_id',
                               related_name='series_entity'
                               )

    class Meta:
        managed = True
        db_table = 'series_entity'
        unique_together = (('series', 'entity'),)

    def __str__(self):
        return str(self.id)


class TickEntity(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    tick = models.ForeignKey('Tick', on_delete=models.DO_NOTHING, db_column='tick_id', related_name='entity_tick')
    entity = models.ForeignKey('Entity', on_delete=models.DO_NOTHING, db_column='entity_id', related_name='tick_entity')

    class Meta:
        managed = True
        db_table = 'tick_entity'
        unique_together = (('tick', 'entity'),)

    def __str__(self):
        return str(self.id)


class ArticleEntity(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    article = models.ForeignKey('Series',
                                on_delete=models.DO_NOTHING,
                                db_column='article_id',
                                related_name='entity_article'
                                )
    entity = models.ForeignKey('Entity',
                               on_delete=models.DO_NOTHING,
                               db_column='entity_id',
                               related_name='article_entity'
                               )

    class Meta:
        managed = True
        db_table = 'article_entity'
        unique_together = (('article', 'entity'),)

    def __str__(self):
        return str(self.id)


class ReportEntity(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    report = models.ForeignKey('Report',
                               on_delete=models.DO_NOTHING,
                               db_column='report_id',
                               related_name='entity_report'
                               )
    entity = models.ForeignKey('Entity',
                               on_delete=models.DO_NOTHING,
                               db_column='entity_id',
                               related_name='report_entity'
                               )

    class Meta:
        managed = True
        db_table = 'report_entity'
        unique_together = (('report', 'entity'),)

    def __str__(self):
        return str(self.id)


class CommentEntity(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    comment = models.ForeignKey('Comment',
                                on_delete=models.DO_NOTHING,
                                db_column='comment_id',
                                related_name='entity_comment'
                                )
    entity = models.ForeignKey('Entity',
                               on_delete=models.DO_NOTHING,
                               db_column='entity_id',
                               related_name='comment_entity'
                               )

    class Meta:
        managed = True
        db_table = 'comment_entity'
        unique_together = (('comment', 'entity'),)

    def __str__(self):
        return str(self.id)


class CommentCollectionEntity(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    comment_collection = models.ForeignKey('CommentCollection',
                                           on_delete=models.DO_NOTHING,
                                           db_column='comment_collection_id',
                                           related_name='entity_comment_collection'
                                           )
    entity = models.ForeignKey('Entity',
                               on_delete=models.DO_NOTHING,
                               db_column='entity_id',
                               related_name='comment_collection_entity'
                               )

    class Meta:
        managed = True
        db_table = 'comment_collection_entity'
        unique_together = (('comment_collection', 'entity'),)

    def __str__(self):
        return str(self.id)
