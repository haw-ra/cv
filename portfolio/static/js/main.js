// رسالة ترحيبية تظهر في الكونسول للتأكد من عمل السكربت
console.log("تم تحميل ملف الجافاسكربت بنجاح! المنصة جاهزة.");

// إضافة تأثير بسيط عند التمرير (Scroll)
window.addEventListener('scroll', function() {
    let hero = document.querySelector('.hero-section');
    if (window.scrollY > 50 && hero) {
        hero.style.opacity = '0.9';
    } else if (hero) {
        hero.style.opacity = '1';
    }
});