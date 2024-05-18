from enum import Enum

from common.models.fcm import FCMToken
from common.models.user import User
from firebase_admin.exceptions import FirebaseError
from firebase_admin.messaging import AndroidConfig, Message, Notification, send


class PushController:
    tokens = FCMToken.objects

    class FCMPriority(Enum):
        HIGH = "high"
        NORMAL = "normal"

    def notifyTo(
        self, user: User, title: str, body: str, priority: FCMPriority = FCMPriority.NORMAL
    ):
        """
        - user: The user to send the push notification
        - title: The title of the notification
        - body: The body of the notification
        - priority: The priority of the notification either high or normal
        """
        t = self.tokens.filter(user=user)
        try:
            send(
                Message(
                    token=t,
                    notification=Notification(title=title, body=body),
                    android=AndroidConfig(priority="high"),
                ),
            )
        except FirebaseError | ValueError as e:
            assert False, f"Error sending notification: {e}"
