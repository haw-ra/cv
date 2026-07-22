from django.db import models
from django.conf import settings

class Profile(models.Model):
    # --- ربط البروفايل بالمستخدم ---
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    
    # --- خيارات التصميم (CV Themes) ---
    STYLE_CHOICES = [
        ('classic', 'كلاسيك أبيض - Classic White'),
        ('modern-dark', 'مودرن غامق - Modern Dark'),
        ('creative-blue', 'إبداعي أزرق - Creative Blue'),
        ('elegant', 'أنيق ومقسم - Elegant Minimal'),
    ]

    name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    email = models.EmailField()
    
    # --- الحقول الجديدة ---
    phone_number = models.CharField(max_length=20, blank=True, null=True) # رقم الموبايل
    website = models.URLField(blank=True, null=True) # رابط الموقع الخاص بالزبون
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True) # الصورة الشخصية
    
    # حقل الستايل (مدمج ومصحح)
    cv_style = models.CharField(
        max_length=30,
        choices=STYLE_CHOICES,
        default='classic',
        verbose_name='نمط السيرة الذاتية'
    )
    # ----------------------
    
    bio = models.TextField()
    social_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

# 1. جدول التعليم
class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    university = models.CharField(max_length=150)
    degree = models.CharField(max_length=100)
    graduation_year = models.CharField(max_length=4)

    def __str__(self):
        return f"{self.degree} - {self.university}"

# 2. جدول الخبرات والمشاريع
class Experience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    company_or_project = models.CharField(max_length=150)
    job_role = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.job_role

# 3. جدول المهارات
class Skill(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=50)

    def __str__(self):
        return self.skill_name