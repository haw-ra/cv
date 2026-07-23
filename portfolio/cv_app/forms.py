from django import forms
from .models import Profile, Education, Experience, Skill

# 1. فورمة البيانات الأساسية
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'job_title', 'email', 'phone_number', 'address', 'profile_picture', 'bio', 'social_link']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'الاسم الكامل'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'المسمى الوظيفي (مثلاً: مطور برمجيات)'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'البريد الإلكتروني'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'اكتب نبذة مختصرة عن مهاراتك وشغفك...'}),
            'social_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'رابط حسابك على LinkedIn أو GitHub'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم الموبايل (اختياري)'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'عنوان السكن (اختياري)'}),
            'cv_style': forms.Select(attrs={'class': 'form-control'}),
        }

# 2. فورمة التعليم
class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['university', 'degree', 'graduation_year']
        widgets = {
            'university': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم الجامعة أو المعهد'}),
            'degree': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'الشهادة التخصصية (مثلاً: بكالوريوس علوم حاسوب)'}),
            'graduation_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'سنة التخرج (مثلاً: 2026)'}),
        }

# 3. فورمة الخبرات
class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['company_or_project', 'job_role', 'description']
        widgets = {
            'company_or_project': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم الشركة أو المشروع (مثلاً: مشروع تخرج)'}),
            'job_role': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'دورك في المشروع (مثلاً: مطور Backend)'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'اشرح باختصار التقنيات التي استخدمتها والإنجازات...'}),
        }

# 4. فورمة المهارات
class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['skill_name']
        widgets = {
            'skill_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم المهارة (مثلاً: Python)'}),
        }