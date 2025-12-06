from django import forms
from django.contrib.auth.models import Group, User

class SendNotificationForm(forms.Form):
    RECIPIENT_CHOICES = [
        ('group', 'Group'),
        ('user', 'Specific User'),
    ]
    TYPE_CHOICES = [
        ('info', 'Info'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('danger', 'Alert/Error'),
    ]

    recipient_type = forms.ChoiceField(
        choices=RECIPIENT_CHOICES, 
        widget=forms.RadioSelect(attrs={'class': 'btn-check', 'autocomplete': 'off'}), 
        initial='group'
    )
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(), 
        required=False, 
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Select Group..."
    )
    user = forms.ModelChoiceField(
        queryset=User.objects.all(), 
        required=False, 
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Select User..."
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter notification message...'}), 
        max_length=255
    )
    notification_type = forms.ChoiceField(
        choices=TYPE_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-select'}), 
        initial='info'
    )
    link = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '/dashboard/'}),
        help_text="Optional: Target URL when clicked"
    )
    
    def clean(self):
        cleaned_data = super().clean()
        recipient_type = cleaned_data.get('recipient_type')
        group = cleaned_data.get('group')
        user = cleaned_data.get('user')

        if recipient_type == 'group' and not group:
            self.add_error('group', 'Please select a target group.')
        if recipient_type == 'user' and not user:
            self.add_error('user', 'Please select a target user.')