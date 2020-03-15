from django.db import models


class Tag(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=510)
    description = models.CharField(db_column='description', max_length=1020, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tag'

    def __str__(self):
        return self.name


class TagGroup(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=510)
    description = models.CharField(db_column='description', max_length=1020, blank=True, null=True)
    tags = models.ManyToManyField(Tag, through='TagTagGroup')
    tag_groups = models.ManyToManyField("self",
                                        through='TagGroupTagGroup',
                                        through_fields=('tag_group1', 'tag_group2'),
                                        symmetrical=False
                                        )

    class Meta:
        managed = True
        db_table = 'tag_group'

    def __str__(self):
        return self.name


class TagTagGroup(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    tag = models.ForeignKey(Tag, on_delete=models.DO_NOTHING, db_column='tag_id')
    tag_group = models.ForeignKey(TagGroup, on_delete=models.DO_NOTHING, db_column='tag_group_id')

    class Meta:
        managed = True
        db_table = 'tag_tag_group'

    def __str__(self):
        return str(self.id)


class TagGroupTagGroup(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    tag_group1 = models.ForeignKey(TagGroup,
                                   on_delete=models.DO_NOTHING,
                                   db_column='tag_group_id1',
                                   related_name="tag_group_id1"
                                   )
    tag_group2 = models.ForeignKey(TagGroup,
                                   on_delete=models.DO_NOTHING,
                                   db_column='tag_group_id2',
                                   related_name="tag_group_id2"
                                   )

    class Meta:
        managed = True
        db_table = 'tag_group_tag_group'

    def __str__(self):
        return str(self.id)
