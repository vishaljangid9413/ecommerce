from django.db import models

# Create your models here.
class OTPLog(models.Model):
    STATUS = [
        ('generated', 'Generated'),
        ('expired', 'Expired'),
        ('verified', 'Verified'),
    ]
    otp = models.CharField(max_length=6)
    email = models.CharField(max_length=30)
    status = models.CharField(max_length=10, choices=STATUS, default = "generated")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'OTP Log'
        verbose_name_plural = 'OTP Logs'
    
    def __str__(self):
        return f"{self.email} - ({self.otp})"

    def save(self, *args, **kwargs):
        OTPLog.objects.filter(email=self.email, status='generated').update(status='expired')
        super().save(*args, **kwargs)



