import streamlit as st
import uuid

# إعداد الصفحة
st.set_page_config(page_title="One Piece Chat", page_icon="🏴‍☠️")

# دالة توليد الصور المجانية
def generate_free_image(prompt):
    formatted_prompt = prompt.replace(" ", "%20")
    return f"https://image.pollinations.ai/prompt/{formatted_prompt}?width=1024&height=1024&nologo=true"

# نظام إدارة المحادثات
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

# القائمة الجانبية
with st.sidebar:
    st.title("⚓ طاقم قبعة القش")
    if st.button("➕ محادثة جديدة"):
        new_id = str(uuid.uuid4())
        st.session_state.current_chat_id = new_id
        st.session_state.creating_new = True

    st.write("---")
    for cid, data in st.session_state.all_chats.items():
        if st.button(f"{data['char']} - {data['name']}", key=cid):
            st.session_state.current_chat_id = cid
            st.session_state.creating_new = False

# الشاشة الرئيسية
if st.session_state.get("creating_new"):
    char = st.selectbox("اختر الشخصية:", ["لوفي 🍖", "زورو ⚔️", "نامي 💰", "سانجي 🚬"])
    name = st.text_input("اسم المغامرة:", value="مغامرة جديدة")
    if st.button("بدء"):
        cid = st.session_state.current_chat_id
        st.session_state.all_chats[cid] = {"char": char, "name": name, "messages": []}
        st.session_state.creating_new = False
        st.rerun()

elif st.session_state.current_chat_id:
    cid = st.session_state.current_chat_id
    chat = st.session_state.all_chats[cid]
    st.header(f"دردشة {chat['char']}")

    for msg in chat["messages"]:
        with st.chat_message(msg["role"]):
            if msg["type"] == "text": st.write(msg["content"])
            else: st.image(msg["content"])

    if user_input := st.chat_input("اكتب رسالة أو ابدأ بكلمة 'ارسم'..."):
        chat["messages"].append({"role": "user", "type": "text", "content": user_input})
        
        if user_input.startswith("ارسم"):
            img_url = generate_free_image(user_input.replace("ارسم", ""))
            chat["messages"].append({"role": "assistant", "type": "image", "content": img_url})
        else:
            reply = f"بصفتي {chat['char']}، أنا معك في هذه الرحلة!"
            chat["messages"].append({"role": "assistant", "type": "text", "content": reply})
        st.rerun()
