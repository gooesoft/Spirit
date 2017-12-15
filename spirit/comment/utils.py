# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from ..topic.notification.models import TopicNotification, UNDEFINED
from ..topic.unread.models import TopicUnread
from .history.models import CommentHistory
from .poll.utils.render_static import post_render_static_polls
from ..topic.notification import signals

def comment_posted(comment, mentions):
    TopicNotification.create_maybe(user=comment.user, comment=comment, action=UNDEFINED)
    TopicNotification.notify_new_comment(comment=comment)
    TopicNotification.notify_new_mentions(comment=comment, mentions=mentions)
    TopicUnread.unread_new_comment(comment=comment)
    comment.topic.increase_comment_count()

    # only need to notify for mentions
    if mentions:
        signals.notify_new_mentions.send(sender=None, topic=comment.topic, user=comment.user, comment=comment)

    # if not mentions, notify new comment as usual
    signals.notify_new_comment.send(sender=None, topic=comment.topic, user=comment.user, comment=comment)


def pre_comment_update(comment):
    comment.comment_html = post_render_static_polls(comment)
    CommentHistory.create_maybe(comment)


def post_comment_update(comment):
    comment.increase_modified_count()

    comment.comment_html = post_render_static_polls(comment)
    CommentHistory.create(comment)
