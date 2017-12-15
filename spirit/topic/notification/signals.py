from django.dispatch import Signal

notify_new_comment = Signal(providing_args=["topic", "user", "comment"])

notify_new_mentions = Signal(providing_args=["topic", "user", "comment"])

notify_invite = Signal(providing_args=["topic", "user"])
