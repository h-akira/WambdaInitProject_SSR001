from wambda.urls import Path
from .views import login_view, signup_view, verify_view, logout_view, change_password_view

urlpatterns = [
    Path("login", login_view, name="login"),
    Path("signup", signup_view, name="signup"),
    Path("verify", verify_view, name="verify"),
    Path("logout", logout_view, name="logout"),
    Path("change-password", change_password_view, name="change_password"),
]