import streamlit as st
from groq import Groq
import tempfile
import os

ACADEMY_INFO = """

اسم الأكاديمية: أكاديمية كود ليدر - CODEleader Academy
الشعار: أكثر من مجرد برمجة، نحن نبني قادة المستقبل

=== الاعتمادات والفلسفة ===
- معتمدة دولياً من منظمة STEM.org الأمريكية (أعلى اعتماد عالمي في العلوم والتكنولوجيا والهندسة والرياضيات)
- منهجية التعلم القائم على المشاريع (Project-Based Learning): الطالب يصنع مشروعاً حقيقياً في كل حصة
- تُبنى مهارات القرن الحادي والعشرين: التفكير النقدي، حل المشكلات، الإبداع، مهارات العرض والتقديم

=== نظام الدراسة ===
- أونلاين مباشر (Live) عبر Zoom - وليس فيديوهات مسجلة
- مجموعات صغيرة جداً: من 3 إلى 5 طلاب كحد أقصى
- حصة واحدة أسبوعياً مدتها 90 دقيقة
- كل حصة تُسجَّل وترسل للطالب فور انتهائها
- جروب واتساب خاص لكل مجموعة (أولياء الأمور + المهندس + مشرف الدعم)
- تقرير أداء أسبوعي يُرسل لولي الأمر
- مشروع نهائي في نهاية كل مستوى للحصول على الشهادة والانتقال للمستوى الأعلى
- المستوى الواحد = 8 محاضرات (نحو شهرين)

=== المسارات التعليمية ===

[مسار الصغار - سن 6 إلى 8 سنوات]
- Scratch Jr & Code.org
- PictoBlox AI Junior

[مسار اليافعين - سن 9 إلى 13 سنة]
- Scratch 3.0 المتقدم
- Python
- تطوير المواقع
- تطوير الألعاب
- تطبيقات الموبايل

[مسار الشباب - سن 14 إلى 18 سنة]
- الذكاء الاصطناعي وتعلم الآلة
- الجرافيك والموشن جرافيك والمونتاج

=== الأسعار والدفع ===
- الأسعار تختلف حسب المسار والفئة العمرية
- التواصل عبر واتساب

=== المواعيد ===
- مجموعات مسائية + الجمعة والسبت
- إيقاف مؤقت في فترات الامتحانات

=== خدمات مجانية ===
- جلسة استشارية مجانية

=== التواصل ===
- الموقع: https://codeleadereg.com
- واتساب 1: https://wa.me/201284447141
- واتساب 2: https://wa.me/201030115464
- البريد الإلكتروني: info@codeleadereg.com
- فيسبوك: facebook.com/CodeLeaderAcademy
"""

SYSTEM_PROMPT = f"""

أنت مساعد ذكي ومحترف لأكاديمية CODEleader لتعليم البرمجة للأطفال واليافعين.

=== الشخصية والأسلوب ===
- تحدث بأسلوب رسمي ومحترف باللغة العربية الفصحى المبسطة.
- ابدأ ردودك دائماً بترحيب رسمي مثل: "أهلاً بكم في أكاديمية CODEleader 🎓" أو "يسعدنا تلقّي استفساركم."
- استخدم عبارات مثل: "بكل سرور"، "يُسعدنا إعلامكم"، "نودّ الإشارة إلى"، "تفضّلوا بالتواصل معنا".
- اختم ردودك دائماً بعبارة مثل: "نحن في أكاديمية CODEleader على أتم الاستعداد للإجابة عن أي استفسار آخر. 🎓"

=== قواعد الرد ===
- أجب فقط بناءً على المعلومات التالية ولا تُضِف معلومات من خارجها.
- إذا سأل أحد عن السعر: أوضح أن الأسعار تختلف حسب المسار والفئة العمرية وأن هناك عروضاً وخصومات متاحة، وأرشده للتواصل عبر واتساب.
- إذا سأل عن موعد مجموعة محددة أو جدول الحصص الحالي أو الأوقات المتاحة: رد بالنص التالي حرفياً:
  "لتحديد الموعد الأنسب لطفلكم ومعرفة المجموعات المتاحة حالياً، يُرجى التواصل مباشرةً مع فريق خدمة العملاء عبر واتساب على الأرقام التالية:
  📲 واتساب 1: https://wa.me/201284447141
  📲 واتساب 2: https://wa.me/201030115464
  وسيتواصل معكم فريقنا في أقرب وقت ممكن."
- إذا كان السؤال خارج نطاق معلومات الأكاديمية: قل بأدب "للمزيد من التفاصيل، يُرجى التواصل معنا مباشرةً عبر واتساب:
  📲 https://wa.me/201284447141
  📲 https://wa.me/201030115464"
- عند ذكر روابط التواصل اذكر الرابطين معاً دائماً.

معلومات الأكاديمية:
{ACADEMY_INFO}
"""

Groq_model = "openai/gpt-oss-120b"
@st.cache_resource
def get_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])



client = get_client()

st.set_page_config(page_title="🎓CODELEADER", page_icon="🎓", layout="centered")
st.title("🎓CODELEADER")

# Chat history
if "message_history" not in st.session_state:
    st.session_state.message_history = []

# Clear chat
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.message_history = []
    st.rerun()

# Display chat history
for message in st.session_state.message_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Text input
user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.message_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model=Groq_model,
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.message_history,
                    max_tokens=512,
                )
                reply = response.choices[0].message.content
            except Exception as e:
                reply = (
                    "ليس لدي معلومة حول هذا الموضوع، يُرجى التواصل معنا مباشرة عبر واتساب\n\n"
                    "📲 https://wa.me/201284447141\n"
                    "📲 https://wa.me/201030115464"
                )
        st.write(reply)
        st.session_state.message_history.append({"role": "assistant", "content": reply})

# Audio input
audio_input = st.audio_input("Record your message...")

if audio_input and st.button("Send Audio"):
    with st.spinner("Converting audio to text..."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_input.read())
            tmp_file_path = tmp_file.name

        try:
            with open(tmp_file_path, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-large-v3-turbo",
                    file=audio_file,
                    response_format="text"
                )
        finally:
            os.unlink(tmp_file_path)

    # Show transcript
    st.session_state.message_history.append({"role": "user", "content": transcript})
    with st.chat_message("user"):
        st.write(transcript)

    # Generate assistant reply
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                messages = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.message_history
                response = client.chat.completions.create(
                    model=Groq_model,
                    messages=messages,
                    max_tokens=500,
                    temperature=0.7
                )
                answer = response.choices[0].message.content
            except Exception as e:
                answer = f"حدث خطأ أثناء معالجة الصوت: {e}"

        st.write(answer)
        st.session_state.message_history.append({"role": "assistant", "content": answer})
