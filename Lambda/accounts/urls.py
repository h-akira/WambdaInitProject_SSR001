from wambda.urls import Path
from .views import login_view, signup_view, verify_view, logout_view, change_password_view, forgot_password_view, reset_password_view, user_profile_view

urlpatterns = [
    Path("login", login_view, name="login"),
    Path("signup", signup_view, name="signup"),
    Path("verify", verify_view, name="verify"),
    Path("logout", logout_view, name="logout"),
    Path("profile", user_profile_view, name="profile"),
    Path("change-password", change_password_view, name="change_password"),
    Path("forgot-password", forgot_password_view, name="forgot_password"),
    Path("reset-password", reset_password_view, name="reset_password"),
]