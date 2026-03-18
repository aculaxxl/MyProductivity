from allauth.account.adapter import DefaultAccountAdapter
from allauth.utils import generate_unique_username

class UsernameMaxAdapter(DefaultAccountAdapter):
    def populate_username(self, request, user):
        # generate username frm email
        if not user.username:
            user.username = generate_unique_username([
                user.email,
                "user"
            ])
        return super().populate_username(request, user)