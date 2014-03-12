import datetime

from django import forms
from django.forms import widgets
from django.core import validators

from django.contrib.auth.models import User, AnonymousUser

class SignupForm(forms.Form):
  """
  Player signup form

  For the 'username-less' version of the form, see 'SignupFormNoUsername'.
  """
  username            = forms.CharField(max_length=75, widget=forms.TextInput(attrs={'size':'30'}) )
  first_name          = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'size':'30'}) )
  last_name           = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'size':'30'}) )
  password            = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'size':'12'}) )
  password_verify     = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'size':'12'}))
  email               = forms.EmailField(help_text="you@domain.com", widget=forms.TextInput(attrs={'size':'30'}))
  terms               = forms.BooleanField(widget=widgets.CheckboxInput, initial=False, required=True,
                                           error_messages={'required': "You must agree to the terms of use."})
  honey               = forms.CharField(max_length=128, required=False)

  def __init__(self, *args, **kws):
    if 'prefix' not in kws: kws['prefix'] = 'signup'
    super(SignupForm, self).__init__(*args, **kws)

  def clean_username(self):
    username = self.cleaned_data['username'].strip().lower()

    if not re.match("^[a-z0-9_-]+$", username):
      raise forms.ValidationError('You can only use letters, numbers and _ or -')

    if User.objects.filter(username__iexact=username, is_active=True).exists():
      raise forms.ValidationError( 'This one is chosen, please pick another name')

    return username

  def clean_email(self):
    bad_domains = ['21cn.com', '163.com', 'eyou.com', 'sohu.com', 'qq.com']
    email = self.cleaned_data.get('email','').lower().strip()

    email_domain = email.split('@')[1]
    if email_domain in bad_domains:
      raise forms.ValidationError("Registration from this domain is prohibited. Please supply a different email address.")

    if User.objects.filter(email__iexact=email).exists():
      raise forms.ValidationError( 'This email is already registered!')

    return email

  def clean(self):
    """
    Validate fields to make sure everything's as expected.
    """
    cd = self.cleaned_data

    if 'honey' in cd and cd['honey'] != '': # is it a robot?
      raise forms.ValidationError( 'Detected a robot!')

    if 'password' in cd and 'password_verify' in cd:
      if self.cleaned_data['password'] != self.cleaned_data['password_verify']:
        self._errors['password'] = forms.util.ErrorList(["Passwords don't match!"])

    else:
      self._errors['password'] = forms.util.ErrorList(["Please enter and confirm your password"])

    return cd

  def create_user(self, request=None, random_password=False):
    """
    Given a validated form, return a new User.
    Takes care of referrals too (if an HttpRequest object is passed).
    """
    cd = self.cleaned_data

    # Create user
    user = User()
    user.username = cd['username']
    user.first_name = cd['first_name']
    user.last_name = cd['last_name']
    user.email = cd['email']
    user.save()

    if random_password:
      user.random_password = "".join(random.sample(string.lowercase, 8))
      user.set_password(user.random_password)
    else:
      user.set_password(cd['password'])
    user.save()

    if request is not None:
      # If we have a referral code, set the profile's 'referral' field to it.
      # Note: there *should* be a profile here, as a signal will have created it automatically.
      name = request.session.get('referral', '').strip()
      if name:
        referral, _ = enginemodels.Referral.objects.get_or_create(name__iexact=name)
        profile = user.get_profile()
        profile.referral = referral
        profile.save()

    return user