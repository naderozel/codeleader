import os
import tempfile
import streamlit as st
from groq import Groq

st.set_page_config(page_title="CODEleader Academy", page_icon="🎓", layout="centered")

ACADEMY_INFO = """
اسم الأكاديمية: أكاديمية كود ليدر - CODEleader Academy
الشعار: أكثر من مجرد برمجة، نحن نبني قادة المستقبل

=== الاعتمادات والفلسفة ===
- معتمدة دولياً من منظمة STEM.org الأمريكية
- التعلم القائم على المشاريع (Project-Based Learning)
- مشروع حقيقي في كل حصة
- تنمية التفكير النقدي، حل المشكلات، الإبداع، ومهارات العرض والتقديم

=== نظام الدراسة ===
- أونلاين مباشر عبر Zoom وليس فيديوهات مسجلة
- مجموعات من 3 إلى 5 طلاب
- حصة أسبوعياً مدتها 90 دقيقة
- تسجيل الحصة وإرسالها للطالب
- جروب واتساب خاص لكل مجموعة
- تقرير أداء أسبوعي لولي الأمر
- مشروع نهائي في نهاية كل مستوى
- المستوى = 8 محاضرات، نحو شهرين

=== المسارات ===
[الصغار - 6 إلى 8 سنوات]
- Scratch Jr & Code.org
- الخوارزميات، التتابع، الحلقات، الشروط
- PictoBlox AI Junior
- مقدمة للذكاء الاصطناعي والروبوتات

[اليافعين - 9 إلى 13 سنة]
- Scratch 3.0 المتقدم
- Python
- قواعد البيانات وهياكل البيانات والدوال والمكتبات
- Web Development: HTML5, CSS3, JavaScript, Bootstrap, PHP, MySQL
- Game Development: ألعاب 2D و3D، الفيزياء، ذكاء اصطناعي للأعداء
- Mobile Apps: MIT App Inventor، Android وiPhone، GPS والكاميرا

[الشباب - 14 إلى 18 سنة]
- AI & Machine Learning
- Python، OpenCV، تحليل البيانات، التعرف على الوجوه
- Photoshop، Illustrator، Premiere، After Effects

=== الأسعار ===
- الأسعار تختلف حسب المسار وسن الطالب
- عروض وخصومات للأخوة
- للاستفسار عن الأسعار: التواصل عبر واتساب
- الدفع: فودافون كاش، إنستا باي، تحويل بنكي

=== المواعيد ===
- مجموعات مسائية خلال الأسبوع
- الجمعة والسبت
- إيقاف مؤقت أثناء الامتحانات المدرسية

=== خدمة مجانية ===
- جلسة استشارية مجانية لتحديد المسار المناسب حسب سن الطفل وشغفه

=== التواصل ===
- الموقع: https://codeleadereg.com
- واتساب 1: https://wa.me/201284447141
- واتساب 2: https://wa.me/201030115464
- البريد: info@codeleadereg.com
- Facebook: facebook.com/CodeLeaderAcademy
"""

SYSTEM_PROMPT = f"""
أنت المساعد الرسمي لأكاديمية CODEleader لتعليم البرمجة للأطفال واليافعين.

- تحدث بالعربية الفصحى المبسطة وبأسلوب رسمي وودود.
- ابدأ الرد بترحيب مثل: "أهلاً بكم في أكاديمية CODEleader 🎓".
- أجب فقط بناءً على معلومات الأكاديمية.
- لا تخترع أسعاراً أو مواعيد أو خدمات غير موجودة.
- عند السؤال عن الأسعار: وضح أن الأسعار تختلف حسب المسار وسن الطالب، وتوجد عروض وخصومات للأخوة، ثم وجه المستخدم إلى واتساب.
- عند السؤال عن المواعيد الحالية أو جدول المجموعات استخدم حرفياً:

لتحديد الموعد الأنسب لطفلكم ومعرفة المجموعات المتاحة حالياً، يُرجى التواصل مباشرةً مع فريق خدمة العملاء عبر واتساب على الأرقام التالية:
📲 واتساب 1: https://wa.me/201284447141
📲 واتساب 2: https://wa.me/201030115464
وسيتواصل معكم فريقنا في أقرب وقت ممكن.

- إذا كان السؤال خارج معلومات الأكاديمية استخدم:

للمزيد من التفاصيل، يُرجى التواصل معنا مباشرةً عبر واتساب:
📲 https://wa.me/201284447141
📲 https://wa.me/201030115464

- عند ذكر واتساب اذكر الرابطين دائماً.
- اختم الردود المناسبة بعبارة:
"نحن في أكاديمية CODEleader على أتم الاستعداد للإجابة عن أي استفسار آخر. 🎓"

=== معلومات الأكاديمية ===
{ACADEMY_INFO}
"""

CHAT_MODEL = "openai/gpt-oss-120b"
WHISPER_MODEL = "whisper-large-v3-turbo"

@st.cache_resource
def get_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

try:
    client = get_client()
except Exception:
    st.error("تعذر تشغيل خدمة الذكاء الاصطناعي. تأكد من GROQ_API_KEY.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

def ask_ai(messages):
    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages,
        max_tokens=600,
        temperature=0.2
    )
    return response.choices[0].message.content.strip()

def transcribe_audio(audio):
    temp_path = None
    try:
        suffix = os.path.splitext(audio.name)[1] if hasattr(audio, "name") else ".wav"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(audio.getvalue())
            temp_path = tmp.name
        with open(temp_path, "rb") as file:
            result = client.audio.transcriptions.create(
                model=WHISPER_MODEL,
                file=file,
                response_format="text"
            )
        return str(result).strip()
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

def generate_answer(text):
    st.session_state.messages.append({"role": "user", "content": text})
    try:
        answer = ask_ai(st.session_state.messages)
    except Exception:
        st.session_state.messages.pop()
        answer = """نعتذر، حدث خطأ مؤقت أثناء معالجة طلبكم.

للمزيد من التفاصيل، يُرجى التواصل معنا مباشرةً عبر واتساب:
📲 https://wa.me/201284447141
📲 https://wa.me/201030115464"""
    st.session_state.messages.append({"role": "assistant", "content": answer})
    return answer

st.title("🎓 CODEleader")
st.caption("أكثر من مجرد برمجة، نحن نبني قادة المستقبل")

with st.sidebar:
    st.header("CODEleader Academy")
    if st.button("🗑️ مسح المحادثة", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("اكتب استفسارك هنا...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        with st.spinner("جاري إعداد الرد..."):
            answer = generate_answer(user_input)
        st.markdown(answer)

st.divider()
st.subheader("🎙️ إرسال رسالة صوتية")
audio = st.audio_input("اضغط هنا لتسجيل رسالتك")

if audio and st.button("📤 إرسال التسجيل", use_container_width=True):
    with st.spinner("🎙️ جاري تحويل التسجيل إلى نص..."):
        try:
            transcript = transcribe_audio(audio)
        except Exception:
            transcript = ""
            st.error("حدث خطأ أثناء تحويل التسجيل الصوتي.")

    if len(transcript) < 2:
        st.warning("لم نتمكن من التعرف على الكلام في التسجيل. يرجى المحاولة مرة أخرى.")
    else:
        with st.chat_message("user"):
            st.markdown(f"🎙️ **رسالتكم:**\n\n{transcript}")
        with st.chat_message("assistant"):
            with st.spinner("جاري إعداد الرد..."):
                answer = generate_answer(transcript)
            st.markdown(answer)
