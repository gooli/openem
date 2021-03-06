# coding=utf8

from django import forms

class FormBase(forms.Form):
    def add_field_error(self, field, error):
        errors = self._errors.setdefault(field, forms.util.ErrorList())
        errors.append(error)

    def add_error(self, error):
        self.add_field_error(forms.forms.NON_FIELD_ERRORS, error)

    def get_status(self):
        return 400 if self._errors else 200

    def __getattr__(self, name):
        if hasattr(self, 'cleaned_data') and name in (self.cleaned_data or {}):
            return self.cleaned_data[name]
        else:
            raise AttributeError(name)

class LoginForm(FormBase):
    username = forms.CharField(
        label=u'שם בדוי', 
        max_length=30,
        error_messages= {'required':u'איך אפשר בלי שם?'}
    )
    password = forms.CharField(
        label=u'סיסמא', 
        max_length=30,
        widget=forms.PasswordInput(),
        error_messages= {'required':u'איך אפשר בלי סיסמא?'}
    )

    def clean_username(self):
        return self.cleaned_data['username'].strip()

class RegisterForm(FormBase):
    username = forms.CharField(
        label=u'שם בדוי', 
        max_length=30,
        error_messages= {'required':u'איך אפשר בלי שם?'}
    )
    password = forms.CharField(
        label=u'סיסמא', 
        max_length=30,
        widget=forms.PasswordInput(),
        error_messages= {'required':u'איך אפשר בלי סיסמא?'}
    )
    password2 = forms.CharField(
        label=u'שוב סיסמא', 
        max_length=30,
        widget=forms.PasswordInput(),
        error_messages= {'required':u'סורי, אבל צריך להזין אית אותה הסיסמא פעמיים.'}
    )
    email = forms.EmailField(
        label=u'אימייל (רק אם רוצים)', 
        max_length=60,
        required=False
    )

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        if cleaned_data.get('password') != cleaned_data.get('password2'):
            raise forms.ValidationError(u'שתי הסיסמאות שונות, נסו שנית.')
        return cleaned_data

    def clean_username(self):
        return self.cleaned_data['username'].strip()

class NewConversationForm(FormBase):
    title = forms.CharField(
        label=u'נושא',
        max_length=200,
        error_messages= {'required':u'על מה תרצו לדבר?'},
        widget=forms.TextInput(attrs={'placeholder': u'נושא'})
    )
    message = forms.CharField(
        label=u'הודעה',
        error_messages= {'required':u'מה תרצו לשתף?'},
        widget=forms.Textarea(attrs={'placeholder': u'אני רוצה לשתף ש...'})
    )
