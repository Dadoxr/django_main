from django import forms

from mailing.models import Message, Recipient, Setting


class SettingForm(forms.ModelForm):

    new_recipients = forms.CharField(
        max_length=150, 
        label='Новые получатели', 
        widget=forms.TextInput(attrs={
            'class': 'text-secondary', 
            'placeholder': 'Через запятую (пример first@mail.ru, second@gmail.com, third@yandex.ru,...)'
            }),
        required=False,
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
                
        queryset = Recipient.objects.filter(owner=user)
        if len(queryset) != 0:
            self.fields['old_recipients'] = forms.ModelMultipleChoiceField(
                queryset=queryset,
                label='Выберите получателей',
                widget=forms.CheckboxSelectMultiple,
                required=False,
            )

    class Meta:
        
        model = Setting
        fields = ('start_time', 'period', 'new_recipients', 'message' )
        widgets = {'start_time': forms.TimeInput(attrs={'type': 'time'})}


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ('subject', 'body', )
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = 'Можно оставить пустым'


