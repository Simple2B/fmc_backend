from .reset_password import UserResetPasswordIn


class ProfileChangePasswordIn(UserResetPasswordIn):
    old_password: str
