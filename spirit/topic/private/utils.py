# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from ..notification.models import TopicNotification
from ..notification import signals

def notify_access(user, topic_private):
    a,b =TopicNotification.create_maybe(
        user=user,
        comment=topic_private.topic.comment_set.last(),
        is_read=False
    )

    print(b)

    signals.notify_invite.send(sender=None, topic=topic_private.topic.comment_set.last().topic, user=user)
