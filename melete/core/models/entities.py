from django.db import models
from polymorphic.models import PolymorphicModel


class Entity(PolymorphicModel):
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=510)
    description = models.CharField(db_column='description', max_length=1020, blank=True, null=True)
    related = models.ManyToManyField('Entity', through='EntityEntity', related_name="entity_entities")
    tags = models.ManyToManyField('Tag', through='TagEntity', related_name="entity_tags")
    # information = models.ManyToManyField(Information, through='InformationEntity')
    # ticks = models.ManyToManyField(Tick, through='InformationEntity', related_name="ticks")
    # reports = models.ManyToManyField(Report, through='InformationEntity', related_name="reports")
    # articles = models.ManyToManyField(Article, through='InformationEntity', related_name="articles")

    class Meta:
        managed = True
        db_table = 'entity'

    def __str__(self):
        return self.name


class Language(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=255)
    description = models.CharField(db_column='description', max_length=1020)

    class Meta:
        managed = True
        db_table = 'language'

    def __str__(self):
        return self.name


class Alias(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    alias = models.CharField(db_column='alias', max_length=510)
    entity = models.ForeignKey(Entity, on_delete=models.DO_NOTHING, db_column='entity_id')
    language = models.ForeignKey(Language, on_delete=models.DO_NOTHING, db_column='Language_id')

    class Meta:
        managed = True
        db_table = 'alias'

    def __str__(self):
        return self.alias


class Exchange(Entity):
    # entity = models.OneToOneField('Entity', on_delete=models.DO_NOTHING, db_column='entity_id', parent_link=True)
    symbol = models.CharField(db_column='symbol', max_length=10)

    class Meta:
        managed = True
        db_table = 'exchange'

    def __str__(self):
        return str(self.id)


class Company(Entity):
    # entity = models.OneToOneField('Entity', on_delete=models.DO_NOTHING, db_column='entity_id', parent_link=True)
    sector = models.CharField(db_column='sector', null=True, max_length=255)
    industry = models.CharField(db_column='industry', null=True, max_length=255)
    ipo_year = models.IntegerField(db_column='ipo_year', null=True)

    class Meta:
        managed = True
        db_table = 'company'

    def __str__(self):
        return str(self.id)


class Ticker(Entity):
    # entity = models.OneToOneField('Entity', on_delete=models.DO_NOTHING, db_column='entity_id', parent_link=True)
    symbol = models.CharField(db_column='symbol', max_length=20)
    ticker_company = models.ForeignKey('Company',
                                       on_delete=models.DO_NOTHING,
                                       db_column='company_id',
                                       related_name='tickers'
                                       )
    ticker_exchange = models.ForeignKey('Exchange',
                                        on_delete=models.DO_NOTHING,
                                        db_column='exchange_id',
                                        related_name='tickers'
                                        )

    lookup_field = 'symbol'

    class Meta:
        managed = True
        db_table = 'ticker'
        unique_together = (('ticker_exchange', 'symbol'),)

    def __str__(self):
        return self.symbol


class Index(Entity):
    # entity = models.OneToOneField('Entity', on_delete=models.DO_NOTHING, db_column='entity_id', parent_link=True)
    tickers = models.ManyToManyField(Ticker, through='IndexTicker')

    class Meta:
        managed = True
        db_table = 'index'

    def __str__(self):
        return self.name


class Country(Entity):
    # entity = models.OneToOneField('Entity', on_delete=models.DO_NOTHING, db_column='entity_id', parent_link=True)

    class Meta:
        managed = True
        db_table = 'country'

    def __str__(self):
        return str(self.id)


class Person(Entity):
    # entity = models.OneToOneField('Entity', on_delete=models.DO_NOTHING, db_column='entity_id', parent_link=True)
    first_name = models.CharField(db_column='first_name', max_length=500)
    last_name = models.CharField(db_column='last_name', max_length=500)

    class Meta:
        managed = True
        db_table = 'person'

    def __str__(self):
        return str(self.id)


class Product(Entity):
    # entity = models.OneToOneField('Entity', on_delete=models.DO_NOTHING, db_column='entity_id', parent_link=True)

    class Meta:
        managed = True
        db_table = 'product'

    def __str__(self):
        return str(self.id)


class Currency(Entity):
    # entity = models.OneToOneField('Entity', on_delete=models.DO_NOTHING, db_column='entity_id', parent_link=True)
    symbol = models.CharField(db_column='symbol', max_length=25, null=False)

    class Meta:
        managed = True
        db_table = 'currency'

    def __str__(self):
        return str(self.id)


# Associative Entities


class EntityEntity(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    entity1 = models.ForeignKey('Entity', on_delete=models.DO_NOTHING, db_column='entity_id1', related_name='entity1')
    entity2 = models.ForeignKey('Entity', on_delete=models.DO_NOTHING, db_column='entity_id2', related_name='entity2')

    class Meta:
        managed = True
        db_table = 'entity_entity'

    def __str__(self):
        return str(self.id)


class TagEntity(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    tag = models.ForeignKey('Tag', on_delete=models.DO_NOTHING, db_column='tag_id', related_name='tag')
    entity = models.ForeignKey(Entity, on_delete=models.DO_NOTHING, db_column='entity_id', related_name='entity')

    class Meta:
        managed = True
        db_table = 'tag_entity'

    def __str__(self):
        return str(self.id)


class IndexTicker(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    index = models.ForeignKey(Index, on_delete=models.DO_NOTHING, db_column='index_id')
    ticker = models.ForeignKey(Ticker, on_delete=models.DO_NOTHING, db_column='ticker_id')

    class Meta:
        managed = True
        db_table = 'index_company'
        unique_together = (('index', 'ticker'),)

    def __str__(self):
        return "%s - %s" % (self.index, self.ticker)


class PersonEntity(models.Model):
    person_entity = models.AutoField(db_column='id', primary_key=True)
    person = models.ForeignKey(Person,
                               on_delete=models.DO_NOTHING, db_column='person_id', related_name="entities_people")
    entity = models.ForeignKey(Entity,
                               on_delete=models.DO_NOTHING, db_column='entity_id', related_name="peoples_entities")

    class Meta:
        managed = True
        db_table = 'person_entity'
        unique_together = (('person', 'entity'),)

    def __str__(self):
        return "%s - %s" % (self.person, self.entity)


class ProductEntity(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    product = models.ForeignKey(Product,
                                on_delete=models.DO_NOTHING, db_column='product_id', related_name="entities_products")
    entity = models.ForeignKey(Entity,
                               on_delete=models.DO_NOTHING, db_column='entity_id', related_name="products_entities")

    class Meta:
        managed = True
        db_table = 'product_entity'
        unique_together = (('product', 'entity'),)

    def __str__(self):
        return "%s - %s" % (self.product, self.entity)
