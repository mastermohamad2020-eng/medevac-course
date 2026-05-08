# 🤖 دليل إعداد GitHub Actions — توليد الأصوات تلقائياً

# ============================================================
# MEDEVAC AT SEA — Auto Voice Generation via GitHub Actions
# ============================================================

دليل شامل لتفعيل توليد الأصوات تلقائياً على GitHub بدون الحاجة لتشغيل أي شيء على جهازك.

---

## 🎯 ما الذي سيحدث؟

1. ترفع الملفات (index.html + course_data.json + generate_voices.py + workflow)
2. ترفع API key كـ "Secret" آمن
3. GitHub Actions يشتغل تلقائياً ويولّد كل ملفات MP3
4. الـ Action يحفظ الملفات في مجلد `audio/` ويعمل commit
5. الكورس يشتغل بالأصوات على GitHub Pages فوراً

---

## 📋 المتطلبات

- ✅ حساب GitHub مجاني
- ✅ Repository موجود (الكورس مرفوع عليه — كما عملت قبل)
- ✅ ElevenLabs API key (لديك بالفعل)

---

# 🚀 الخطوات بالتفصيل

## الخطوة 1: تنزيل الملفات الجديدة

من الـ ZIP الذي تنزله الآن، ستجد:

```
medevac_github_actions_v1.3.zip
├── index.html              ← محدّث (EN-only mode)
├── course_data.json        ← بيانات الكورس
├── generate_voices.py      ← السكريبت المحدّث
├── generate-voices.yml     ← ⭐ ملف GitHub Actions الجديد
└── GITHUB_ACTIONS_SETUP.md ← هذا الدليل
```

---

## الخطوة 2: رفع الملفات على GitHub

### A. ارفع الملفات الأساسية (مثل قبل):

اذهب إلى الـ repository → **Add file → Upload files**

ارفع هذه الملفات في **الجذر** (root):
- ✅ `index.html`
- ✅ `course_data.json`  
- ✅ `generate_voices.py`

اضغط **Commit changes**.

### B. رفع ملف الـ Workflow (مهم جداً):

ملف YAML لازم يكون في مجلد بالاسم `.github/workflows/`. الطريقة الأسهل:

1. في صفحة الـ repository، اضغط **Add file → Create new file**

2. في خانة اسم الملف، اكتب:
   ```
   .github/workflows/generate-voices.yml
   ```
   ⚠ **مهم:** اكتب `.github/workflows/` بالضبط — GitHub سيُنشئ المجلدات تلقائياً.

3. **انسخ كل محتوى ملف `generate-voices.yml`** من الـ ZIP والصقه هنا.

4. اضغط **Commit changes** في الأسفل.

✅ بعد هذه الخطوة، الـ Workflow متاح لكنه **لن يشتغل** بعد لأن الـ Secret لم يُضف.

---

## الخطوة 3: إضافة API Key كـ Secret (الأهم!)

⚠ **لا تضع الـ API key مباشرة في الكود** — استخدم Secrets.

### الخطوات:

1. في صفحة الـ repository، اضغط على تبويب **"Settings"** (أعلى يمين)

2. في القائمة الجانبية اليسرى، اضغط على:
   - **Secrets and variables** (تحت قسم Security)
   - ثم **Actions**

3. اضغط زر **"New repository secret"** الأخضر

4. املأ الحقول:
   - **Name:** `ELEVEN_API_KEY` (بالضبط هذا الاسم — حساس لحالة الأحرف)
   - **Secret:** الصق الـ API key الخاص بك (`sk-...`)

5. اضغط **Add secret**

🔒 **الآن الـ key محمي:** GitHub لن يعرضه لأي شخص حتى لك.

---

## الخطوة 4: تشغيل الـ Workflow أول مرة

### الخيار A — تلقائياً (الأسهل):

1. اذهب إلى ملف `course_data.json` في الـ repository
2. اضغط على ✏ **Edit** 
3. أضف مسافة في أي مكان واحذفها (لإجبار commit)
4. اضغط **Commit changes**

✨ **الـ Workflow سيشتغل تلقائياً!** 

### الخيار B — يدوياً (Manual):

1. اضغط على تبويب **"Actions"** (أعلى الـ repository)

2. في القائمة الجانبية، اضغط على **"🎙 Generate Voice Files"**

3. اضغط زر **"Run workflow"** (الأزرق على اليمين)

4. اختر:
   - **Branch:** `main`
   - **Regenerate ALL files:** `false` (لأول مرة، اتركها false)
   - **Language:** `en`

5. اضغط **Run workflow**

---

## الخطوة 5: متابعة التقدم

1. في تبويب **Actions**، ستجد الـ run الجاري بـ ⏱ icon

2. اضغط عليه لرؤية التفاصيل

3. اضغط على **"generate-voices"** job

4. ستجد التقدم سطر سطر:
   ```
   [1/115] M01-L01-S01-d0-en.mp3 | Adam | Officers, every medical emergency...
   [2/115] M01-L01-S01-d1-en.mp3 | Josh | Master, the crew often hesitates...
   ...
   ```

⏱ **الوقت المتوقع:** 15-25 دقيقة لتوليد ~115 ملف EN

---

## الخطوة 6: التحقق من النجاح

عند انتهاء الـ Workflow:

1. ستجد ✅ علامة خضراء بجانب الـ run

2. ادخل صفحة الـ repository — ستجد مجلد جديد **`audio/`** فيه كل ملفات MP3

3. الـ Workflow عمل commit تلقائي بعنوان:
   ```
   🎙 Auto-generate voice files [115 MP3s, 4.2M]
   ```

4. **GitHub Pages تتحدث تلقائياً** خلال 1-2 دقيقة

5. افتح الكورس على:
   ```
   https://YOUR_USERNAME.github.io/medevac-course/
   ```

🎉 **اضغط أي زر ▶ Play EN — الصوت يشتغل!**

---

# 🔄 عمليات لاحقة

## إعادة توليد بعض الأصوات

إذا غيرت نص في `course_data.json`:

1. ارفع التغيير → الـ Workflow يشتغل تلقائياً
2. الملفات الجديدة فقط ستُولَّد (الموجودة تُتخطى)

## إعادة توليد كل الأصوات من الصفر

1. Actions → Generate Voice Files → Run workflow
2. اختر **"Regenerate ALL files: true"**
3. كل الـ MP3 ستُحذف وتُولَّد من جديد

## إضافة العربي لاحقاً

1. Actions → Run workflow → **Language: ar** أو **both**
2. الملفات الجديدة `*-ar.mp3` ستُضاف
3. في `index.html`، احذف هذا السطر من الـ CSS لإظهار أزرار العربي:
   ```css
   .voice-player-btn.lang-ar { display: none; }
   ```

---

# 💰 تتبع التكلفة

كل run يستهلك من رصيدك في ElevenLabs:

| سيناريو | الاستهلاك |
|---|---|
| التوليد الأول (كل EN) | ~22,000 character |
| تعديل نص واحد + run | ~200 character (الجملة الجديدة فقط) |
| Regenerate ALL EN | ~22,000 character (مجدداً) |
| إضافة Arabic | ~22,000 character إضافية |

📊 **راقب رصيدك على:** https://elevenlabs.io/app/usage

---

# 🆘 حل المشاكل

### ❌ "ELEVEN_API_KEY secret is not set"
**الحل:** الـ Secret ما تم إضافته. ارجع للخطوة 3.

### ❌ "INVALID_API_KEY"
**الحل:** الـ Key نفسه خطأ أو منتهي. تحقق من elevenlabs.io.

### ❌ Workflow لا يشتغل تلقائياً
**الأسباب المحتملة:**
- ملف `.github/workflows/generate-voices.yml` ليس في المسار الصحيح
- Branch ليس `main` (قد يكون `master`)

**الحل:** افتح صفحة الـ Actions → إذا الـ workflow غير ظاهر، تحقق من المسار.

### ❌ بعض الأصوات لم تُولَّد
**الحل:** شغل الـ workflow يدوياً مرة أخرى — السكريبت سيتخطى الموجود ويكمل.

### ⚠ "Rate limit / quota exceeded"
**الحل:** انتظر 30 ثانية ثم run مجدداً، أو ارفع رصيدك على ElevenLabs.

### ⚠ الأصوات لا تشتغل على GitHub Pages
**الحل:**
1. تحقق أن مجلد `audio/` موجود في الـ repository
2. افتح Console المتصفح (F12) — اقرأ الأخطاء
3. تحقق أن Pages مفعّلة على branch `main`

---

# 🎯 Checklist نهائي

- [ ] رفعت `index.html` على الـ repo
- [ ] رفعت `course_data.json` على الـ repo
- [ ] رفعت `generate_voices.py` على الـ repo
- [ ] رفعت `.github/workflows/generate-voices.yml`
- [ ] أضفت Secret اسمه `ELEVEN_API_KEY`
- [ ] الـ Workflow اشتغل ووصل لعلامة ✅
- [ ] مجلد `audio/` ظهر في الـ repo
- [ ] الكورس على GitHub Pages الأصوات تشتغل
- [ ] iframe على Thinkific يعرض الكورس بالأصوات

---

🚢 **بالتوفيق Captain — الآن كل شيء مؤتمت بالكامل!** ⚓

أي سؤال — استفسر.
