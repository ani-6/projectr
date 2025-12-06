from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.common.utils import perform_health_check_and_notify

class Command(BaseCommand):
    help = 'Checks system health (DB, Redis) and sends notifications if services are down.'

    def handle(self, *args, **kwargs):
        self.stdout.write(f"[{timezone.now()}] Starting System Health Check...")
        
        # This function handles checking status AND sending notifications
        metrics = perform_health_check_and_notify()
        
        self.stdout.write("Health Check Results:")
        self.stdout.write(f"- Database: {metrics['db_status']} ({metrics['db_latency']}ms)")
        self.stdout.write(f"- Redis: {metrics['redis_status']} ({metrics['redis_latency']}ms)")
        
        # Check if notifications were actually triggered
        if metrics.get('notifications_sent', False):
            self.stdout.write(self.style.ERROR("Issues detected! Notifications have been sent to Managers."))
        elif metrics['db_status'] != 'Online' or metrics['redis_status'] != 'Online':
            self.stdout.write(self.style.WARNING("Issues detected, but notifications were suppressed (Rate Limit or Empty Groups)."))
        else:
            self.stdout.write(self.style.SUCCESS("All systems operational."))