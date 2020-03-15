import django.utils.timezone
from django.db import models

from melete.users.models import User


class Portfolio(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=255)
    created = models.DateTimeField(db_column='created', default=django.utils.timezone.now, null=True)
    modified = models.DateTimeField(db_column='modified', null=True)
    details = models.TextField(db_column='details', null=True)

    class Meta:
        managed = True
        db_table = 'portfolio'

    def __str__(self):
        return self.name


class PortfolioPermission(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', null=False, max_length=255)
    description = models.CharField(db_column='description', null=True, max_length=255)

    class Meta:
        managed = True
        db_table = 'portfolio_permission'

    def __str__(self):
        return str(self.id)


class UserPortfolio(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_column='user_id')
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, db_column='portfolio_id')
    portfolio_permission = models.ForeignKey(PortfolioPermission,
                                             on_delete=models.DO_NOTHING,
                                             db_column='portfolio_permission_id'
                                             )

    class Meta:
        managed = True
        db_table = 'user_portfolio'
        unique_together = (('user', 'portfolio', 'portfolio_permission'),)

    def __str__(self):
        return str(self.id)


class AssetType(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', null=False, max_length=255)
    description = models.CharField(db_column='description', null=True, max_length=255)

    class Meta:
        managed = True
        db_table = 'asset_type'

    def __str__(self):
        return str(self.id)


class Asset(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    portfolio = models.ForeignKey(Portfolio, related_name='assets', on_delete=models.CASCADE, db_column="portfolio_id")
    entity = models.ForeignKey('Entity', on_delete=models.DO_NOTHING, db_column="entity_id", null=True)
    asset_type = models.ForeignKey(AssetType, on_delete=models.DO_NOTHING, db_column="asset_type_id")
    enter_date = models.DateTimeField(db_column='enter_date', null=False)
    exit_date = models.DateTimeField(db_column='exit_date', null=True)
    expiration_date = models.DateTimeField(db_column='expiration_date', null=True)
    quantity = models.FloatField(db_column='quantity', null=False)
    premium = models.FloatField(db_column='premium', null=True, default=0)
    price = models.FloatField(db_column='price', null=False)

    class Meta:
        managed = True
        db_table = 'asset'

    def __str__(self):
        return str(self.id)


class OrderType(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', null=False, max_length=255)
    description = models.CharField(db_column='description', null=True, max_length=255)

    class Meta:
        managed = True
        db_table = 'order_type'

    def __str__(self):
        return str(self.id)


class AssetOrder(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    asset = models.ForeignKey(Asset, on_delete=models.DO_NOTHING, db_column='asset_id')
    order_type = models.ForeignKey(OrderType, on_delete=models.DO_NOTHING, db_column='order_type_id')
    quantity = models.FloatField(db_column='quantity', null=False)
    target = models.FloatField(db_column='target', null=False)
    expiration_date = models.DateTimeField(db_column='expiration_date', null=True)

    class Meta:
        managed = True
        db_table = 'asset_order'

    def __str__(self):
        return str(self.id)
