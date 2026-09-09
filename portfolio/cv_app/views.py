from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Profile, Education, Experience, Skill
from .forms import ProfileForm, EducationForm, ExperienceForm, SkillForm
from django.conf import settings

# try to import weasyprint (يساعد على توليد PDF)
try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except Exception:
    # ImportError أو OSError (مثل غياب مكتبات GTK على ويندوز)
    WEASYPRINT_AVAILABLE = False

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
    elif profile.cv_style == 'english': # 👈 إضافة السطر الخاص بالقالب الإنجليزي
        template_name = 'english_cv.html'    
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
            
            # --- السحر هنا: فحص الزر المضغوط ---
            if request.POST.get('save_action') == 'next':
                # إذا ضغط "التالي"، نوديه لصفحة إضافة التعليم
                return redirect('add_education', profile_id=profile.id) 
            else:
                # إذا ضغط "حفظ والعودة"، نرجعه للوحة التحكم
                return redirect('dashboard') 
            # -----------------------------------
    else:
        form = ProfileForm(instance=profile)
        
    # التعديل الأهم: قمنا بتغيير الملف إلى edit_profile.html
    return render(request, 'edit_profile.html', {'form': form, 'profile': profile})

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


# --- دالة تحميل السيرة الذاتية كـ PDF (WeasyPrint) ---
@login_required
def download_cv_pdf(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id, user=request.user)

    # --- اختيار القالب المناسب حسب النمط المحدد ---
    if profile.cv_style == 'modern-dark':
        template_name = 'modern_dark_cv.html'
    elif profile.cv_style == 'creative-blue':
        template_name = 'creative_blue_cv.html'
    elif profile.cv_style == 'elegant':
        template_name = 'elegant_cv.html'
    elif profile.cv_style == 'english': # 👈 إضافة السطر الخاص بالقالب الإنجليزي هنا أيضاً
        template_name = 'english_cv.html'    
    else:
        template_name = 'classic_cv.html'

    html_string = render_to_string(template_name, {'profile': profile, 'request': request})

    # --- التعديل السحري الخاص بـ PythonAnywhere ---
    # 1. استبدال مسار مجلد media (المكان اللي تنحفظ بي صورة المستخدم)
    local_media_path = f"file://{settings.BASE_DIR}/media/"
    html_string = html_string.replace('/media/', local_media_path)
    
    # 2. استبدال مسار مجلد static (اذا عندج صور ثابتة او ملفات CSS)
    local_static_path = f"file://{settings.BASE_DIR}/static/"
    html_string = html_string.replace('/static/', local_static_path)
    # ----------------------------------------------

    # إنشاء استجابة PDF
    if WEASYPRINT_AVAILABLE:
        # مسحنا الـ base_url لأن صار عندنا مسارات محلية بداخل الـ html_string
        pdf_file = HTML(string=html_string).write_pdf()
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="CV_{profile.user.username}.pdf"'
        return response
    else:
        # إذا لم تكن weasyprint مثبتة، نعرض خطأ واضحاً
        return HttpResponse(
            "WeasyPrint غير مثبت. قم بتشغيل: pip install weasyprint",
            status=500,
        )