from rest_framework import serializers
from .models import DashboardLink

class DashboardLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardLink
        fields = ['id', 'title', 'description', 'url', 'icon', 'order', 'open_in_new_tab']