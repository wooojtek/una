from django import forms

from models import Entry


class WideTextArea(forms.Textarea):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {}).update({'rows': '10', 'cols': '50'})
        super(WideTextArea, self).__init__(*args, **kwargs)


class EntryForm(forms.ModelForm):
    title = forms.CharField(max_length=100,
                            required=False,
                            widget=forms.TextInput(attrs={'size': '50'}))
    body = forms.CharField(widget=WideTextArea(attrs={'class': 'resizable'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        print self.request
        super(EntryForm, self).__init__(*args, **kwargs)
        self.fields['owner'].widget = forms.HiddenInput()
        try:
            self.fields['owner'].initial = self.request.user.pk
        except:
            pass


    class Meta:
        model = Entry
        fields = ('title', 'body', 'owner')