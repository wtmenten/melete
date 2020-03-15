import datetime

from channels.layers import get_channel_layer
from django.conf import settings
from django.core.cache import cache
from django.db import models

channel_layer = get_channel_layer()


class Room(models.Model):
    """
    A room for people/bots to chat in.
    """

    # Room name
    name = models.CharField(max_length=255)

    # If only "staff" users are allowed (is_staff on django's User)
    staff_only = models.BooleanField(default=False)

    historical_period = models.DurationField(null=False, default=datetime.timedelta(days=7))
    historical_count = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    @property
    def group_name(self):
        """
        Returns the Channels Group name that sockets should subscribe to to get sent
        messages as they are generated.
        """
        return "room-%s" % self.id

    @property
    def cache_prefix(self):
        return "status-room-%s" % self.id

    @property
    def history(self):
        history_cache_keys = (cache.keys("%s-*" % self.cache_prefix) or [])
        history_cache_keys.sort(key=lambda x: int(x.split('-')[-1]))
        if self.historical_count is not None:
            remove, history_cache_keys = (
                history_cache_keys[:-self.historical_count],
                history_cache_keys[-self.historical_count:]
            )
            cache.delete_many(remove)
        return cache.get_many(history_cache_keys) or []

    async def join(self, username):

        # reducing next key may overwrite existing history
        # cache.set("%s-next-key" % self.cache_prefix)

        # Send a join message if it's turned on
        if settings.NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
            await self.send({
                    "type": "chat.join",  # used by channel consumer
                    "msg_type": settings.MSG_TYPE_ENTER,
                    "username": username,
                })

    async def leave(self, username):
        # Send a join message if it's turned on
        if settings.NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
            await self.send({
                    "type": "chat.leave",  # used by channel consumer
                    "msg_type": settings.MSG_TYPE_LEAVE,
                    "username": username,
                })

    async def send(self, message):
        message["timestamp"] = message.get("timestamp", datetime.datetime.now().timestamp())
        message["room_id"] = self.id
        try:
            next_cache_postfix = cache.incr("%s_meta_next-key" % self.cache_prefix)
        except ValueError:
            cache.set("%s_meta_next-key" % self.cache_prefix, 0, timeout=None)
            next_cache_postfix = cache.incr("%s_meta_next-key" % self.cache_prefix)

        message["id"] = next_cache_postfix
        cache.set("%s-%s" % (self.cache_prefix, next_cache_postfix), message, self.historical_period.total_seconds())
        await channel_layer.group_send(
            self.group_name,
            message
        )
