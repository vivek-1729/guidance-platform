from django import forms
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

class ResourceForm(forms.Form):
    """
    Admin form to add resources
    """
    title = forms.CharField(label='Title', max_length=1000)
    link = forms.CharField(label='Link', max_length=1000)
    topic = forms.CharField(label='Topic', max_length=500)

class VideoForm(forms.Form):
    """
    Admin form to add videos
    """
    name = forms.CharField(label='Name', max_length=1000)
    link = forms.CharField(label='Link', max_length=1000)

class addBucket(forms.Form):
    """
    Admin form to create a class of resources
    """
    bucket = forms.CharField(label="Name", max_length=1000)

class addScholarship(forms.Form):
    """
    Admin form to create a scholarship
    """
    name = forms.CharField(label="Name", max_length=1000)
    link = forms.CharField(label='Link', max_length=1000)
    description = forms.CharField(label='Description', max_length=5000, widget=forms.Textarea)

class CustomAuthenticate(forms.Form):
    """
    Login form
    """
    username = forms.CharField(max_length=254)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)



grade_choices =( #TODO: Have a blank choice and don't submit if that's selected
    ("NA", "---"),
    ("6", "6"),
    ("7", "7"),
    ("8", "8"),
    ("9", "9"),
    ("10", "10"),
    ("11", "11"),
    ("2", "12"),
    ("Alum", "Alumni"),
    ("Mentor", "Mentor"),
)

class CustomCreate(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))
    grade = forms.ChoiceField(choices=grade_choices)
    nk_id = forms.CharField(label=_("Nanhi Kali / Mentor Id (if applicable)"), required=False)

    class Meta:
        model = User
        fields = ("username",)
        help_texts = {
            'username' : None,
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(CustomCreate, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user