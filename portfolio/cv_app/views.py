from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Profile, Education, Experience, Skill
from .forms import ProfileForm, EducationForm, ExperienceForm, SkillForm

# دالة إنشاء حساب جديد
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # تسجيل الدخول تلقائياً بعد إنشاء الحساب
            return redirect('landing_page')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# دالة الصفحة الرئيسية (الواجهة الترحيبية للموقع) - عامة ولا تحتاج تسجيل دخول
def landing_page(request):
    return render(request, 'landing_page.html')

# دالة عرض السيرة الذاتية (الذكية)
@login_required
def home(request):
    profile = Profile.objects.filter(user=request.user).last()
    
    # إذا لم يكن هناك بيانات، نعرض القالب الكلاسيكي فارغاً
    if not profile:
        return render(request, 'classic_cv.html', {'profile': None})

    # --- هنا نضع كود اختيار القوالب ---
    if profile.cv_style == 'modern-dark':
        template_name = 'modern_dark_cv.html'
    elif profile.cv_style == 'creative-blue':
        template_name = 'creative_blue_cv.html'
    elif profile.cv_style == 'elegant': # السطر الجديد الخاص بالقالب الأنيق
        template_name = 'elegant_cv.html'
    else:
        # القالب الافتراضي إذا كان الاختيار غير محدد
        template_name = 'classic_cv.html' 
    # ----------------------------------

    # نعرض الملف الذي تم اختياره
    return render(request, template_name, {'profile': profile})


# الخطوة 1: البيانات الأساسية
@login_required
def cv_builder(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.cv_style = 'classic'
            profile.save()
            return redirect('add_education', profile_id=profile.id) 
    else:
        form = ProfileForm()
    return render(request, 'cv_builder.html', {'form': form})

# الخطوة 2: إضافة التعليم
@login_required
def add_education(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id, user=request.user)
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.profile = profile
            education.save()
            return redirect('add_experience', profile_id=profile.id) 
    else:
        form = EducationForm()
    return render(request, 'add_education.html', {'form': form, 'profile': profile})

# الخطوة 3: إضافة الخبرات والمشاريع
@login_required
def add_experience(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id, user=request.user)
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.profile = profile
            experience.save()
            return redirect('add_skill', profile_id=profile.id) 
    else:
        form = ExperienceForm()
    return render(request, 'add_experience.html', {'form': form, 'profile': profile})

# الخطوة 4: إضافة المهارات المتعددة
@login_required
def add_skill(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id, user=request.user)
    
    if request.method == 'POST':
        skills_list = request.POST.getlist('skills[]') 
        
        for skill_name in skills_list:
            if skill_name.strip(): 
                Skill.objects.create(profile=profile, skill_name=skill_name.strip())
                
        return redirect('choose_template')
        
    return render(request, 'add_skill.html', {'profile': profile})

# دالة لوحة التحكم (Dashboard)
@login_required
def dashboard(request):
    profile = Profile.objects.filter(user=request.user).last()
    return render(request, 'dashboard.html', {'profile': profile})

# دالة تعديل البيانات الأساسية
@login_required
def edit_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id, user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard') 
    else:
        form = ProfileForm(instance=profile)
        
    return render(request, 'cv_builder.html', {'form': form})

# --- دوال الحذف ---
@login_required
def delete_education(request, edu_id):
    education = get_object_or_404(Education, id=edu_id)
    education.delete()
    return redirect('dashboard')

@login_required
def delete_experience(request, exp_id):
    experience = get_object_or_404(Experience, id=exp_id)
    experience.delete()
    return redirect('dashboard')

@login_required
def delete_skill(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    skill.delete()
    return redirect('dashboard')

# --- دالة اختيار القالب ---
@login_required
def choose_template(request):
    profile = Profile.objects.filter(user=request.user).last() # تم التوحيد إلى filter(user=request.user).last() لضمان خصوصية البيانات
    
    if request.method == 'POST':
        selected_style = request.POST.get('cv_style') 
        if profile:
            profile.cv_style = selected_style
            profile.save() 
        return redirect('home') 
        
    return render(request, 'choose_template.html')