import graphene

from graphql_auth import mutations
from django.db.models import signals
from graphql_auth.models import UserStatus


def verify_user_status(sender, instance, created, **kwargs):
    if created:
        instance.verified = True
        instance.save(update_fields=["verified"])


signals.post_save.connect(receiver=verify_user_status, sender=UserStatus)


class AccountMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
