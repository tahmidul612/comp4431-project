from allauth.account.forms import SignupForm, ResetPasswordForm
from hcaptcha.fields import hCaptchaField


class CustomSignupForm(SignupForm):
    hcaptcha = hCaptchaField(theme='dark')
    # if the order of fields isn't as you expected ,then you can use field_order
    field_order = ['username', 'email', 'password1', 'password2', 'hcaptcha']
    # customize this according to your form


class CustomForgetPassword(ResetPasswordForm):
    hcaptcha = hCaptchaField(theme='dark')
