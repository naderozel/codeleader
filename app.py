import streamlit as st
from groq import Groq
import tempfile
import os

ACADEMY_INFO="""

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
- Scratch Jr & Code.org: خوارزميات، تتابع، حلقات، شروط عبر مكعبات بصرية بدون كتابة أكواد
- PictoBlox AI Junior: مقدمة للذكاء الاصطناعي والروبوتات بلغة البلوكات

[مسار اليافعين - سن 9 إلى 13 سنة]
- Scratch 3.0 المتقدم: ألعاب متعددة المستويات، متغيرات، منصات ألعاب
- Python: برمجة نصية حقيقية، قواعد بيانات، هياكل بيانات، دوال، مكتبات
- تطوير المواقع (Web Development): HTML5, CSS3, JavaScript, Bootstrap (Front-End) + PHP & MySQL (Back-End)
- تطوير الألعاب (Game Development): محركات ألعاب، ألعاب 2D و3D، فيزياء، ذكاء اصطناعي للأعداء
- تطبيقات الموبايل: MIT App Inventor، تطبيقات أندرويد وآيفون، ربط بحساسات الهاتف (GPS، كاميرا)

[مسار الشباب - سن 14 إلى 18 سنة]
- الذكاء الاصطناعي وتعلم الآلة (AI & Machine Learning): Python، OpenCV، تحليل بيانات، التعرف على الوجوه
- الجرافيك والموشن جرافيك والمونتاج: Adobe Photoshop، Illustrator، Premiere، After Effects

=== الأسعار والدفع ===
- الأسعار تختلف حسب المسار وسن الطالب، وتتوفر عروض وخصومات للأخوة
- للاستفسار عن الأسعار: التواصل مباشرة عبر واتساب
- طرق الدفع: فودافون كاش، إنستا باي، تحويل بنكي

=== المواعيد ===
- مجموعات مسائية متاحة أيام الأسبوع
- مجموعات الجمعة والسبت لمن لديهم تعارض مع المدرسة
- إيقاف مؤقت تلقائي في فترات الامتحانات المدرسية

=== خدمات مجانية ===
- جلسة استشارية مجانية لتحديد المسار المناسب للطفل حسب سنه وشغفه

=== التواصل ===
- الموقع: https://codeleadereg.com
- واتساب 1: https://wa.me/201284447141  (01284447141)
- واتساب 2: https://wa.me/201030115464  (01030115464)
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
"""


Groq_model = "openai/gpt-oss-120b"
@st.cache_resource
def get_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

client = get_client()


st.set_page_config(
    page_title="🎓CODELEADER", 
    page_icon="🎓", 
    layout="centered"
    )


st.title("🎓CODELEADER")
audio_input = st.audio_input("Record your message...")
user_input = st.chat_input("Type your message here...") 

if "message_history" not in st.session_state:
    st.session_state.message_history = []


if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.message_history = []
    st.rerun()

for message in st.session_state.message_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if user_input:
    st.session_state.message_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model=Groq_model,
                    messages= [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.message_history,
                    max_tokens=512,
                
                )
                reply = response.choices[0].message.content
            except Exception as e:
                    reply = ("""
                        : ليس لدي معلومه حول هذا الموضوع، يُرجى التواصل معنا مباشرة عبر واتساب
    
                    📲 https://wa.me/201284447141
                    📲 https://wa.me/201030115464"""
                
                    )
        st.write(reply)                 
                 
    st.session_state.message_history.append({"role": "assistant", "content": reply})\
 


if audio_input:
    if st.button("send audio"):
        with st.spinner("converting audio to text..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(audio_input.read())
                tmp_file_path = tmp_file.name
            try:
                with open(tmp_file_path, "rb") as audio_file:
                     transcript = client.audio.transcriptions.create(
                        model="whisper-large-v3-turbo",
                        file=open(tmp_file_path, "rb"),  # open the file in binary mode
                        response_format="text"
)

            finally:
                os.unlink(tmp_file_path)
        if not transcript or len(transcript.strip()) < 2:
            st.session_state.message_history.append({"role": "assistant", "content":transcript})
            with st.chat_message("user"):
                st.write(f"{transcript}")
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        messages = [{"role": "system", "content": "your are a helpful assistant"}]
                        for msg in st.session_state.message_history:
                            messages.append({"role": msg['role'], "content": msg["content"]})
                        response = client.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=messages,
                            max_tokens=500,
                            temperature=0.7
                        )
                        answer = response.choices[0].message.content
                    except Exception as e:
                        answer = e
