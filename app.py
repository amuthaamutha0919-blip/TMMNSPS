import streamlit as st
import pandas as pd
from datetime import datetime, date

# --- 1. டிசைன் மற்றும் ஸ்டைல் ---
st.set_page_config(page_title="சங்க மேலாண்மை", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    [data-testid="stSidebar"] { background-color: #1B4F72; color: white; }
    .complaint-box { background-color: #FDEDEC; padding: 20px; border-radius: 10px; border-left: 5px solid #E74C3C; }
    .id-card { background: linear-gradient(135deg, #1b263b, #0d1b2a); padding: 30px; border-radius: 20px; color: white; text-align: center; border: 3px solid #F1C40F; width: 320px; margin: auto; }
    </style>
    """, unsafe_allow_html=True)

LOGO_URL = "https://i.ibb.co/XwhBx8S/image.png"

# --- 2. டேட்டா மேலாண்மை ---
if 'complaints' not in st.session_state:
    st.session_state.complaints = []
if 'user_db' not in st.session_state:
    st.session_state.user_db = pd.DataFrame(columns=["பெயர்", "மொபைல்", "பிறந்தநாள்", "நிதி"])
if 'locks' not in st.session_state:
    st.session_state.locks = {k: True for k in ["நிதி", "ஐடி கார்டு", "தொடர்புகள்", "புகைப்படம்", "அறிவிப்பு", "உதவி", "புகார்"]}
if 'targets' not in st.session_state:
    st.session_state.targets = {"fest_name": "பொங்கல் விழா", "fest_dt": date(2026, 1, 14)}

# --- 3. விரிவான லாகின் ---
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.image(LOGO_URL, width=150)
    st.title("🔐 சங்க லாகின்")
    with st.form("login"):
        name = st.text_input("பெயர்")
        dob = st.date_input("பிறந்த தேதி", value=date(1995, 1, 1))
        mob = st.text_input("மொபைல்")
        role = st.selectbox("வகை", ["உறுப்பினர்", "தலைவர் (Admin)"])
        pwd = st.text_input("பாஸ்வேர்டு", type="password")
        if st.form_submit_button("Login"):
            if (role == "தலைவர் (Admin)" and pwd == "admin123") or (role == "உறுப்பினர்" and pwd == "member123"):
                st.session_state.logged_in = True
                st.session_state.role = "admin" if role == "தலைவர் (Admin)" else "member"
                st.session_state.u_name, st.session_state.u_dob, st.session_state.u_mob = name, dob, mob
                st.rerun()
            else: st.error("தவறான பாஸ்வேர்டு!")
    st.stop()

# --- 4. மெனு போர்டு (Sidebar) ---
with st.sidebar:
    st.image(LOGO_URL, width=100)
    st.write(f"செல்வம்: **{st.session_state.u_name}**")
    
    # மெனு பட்டியல் (8 + 1 வசதிகள்)
    options = ["🏠 முகப்பு"]
    if st.session_state.locks['நிதி']: options.append("💰 நிதி நிலை")
    if st.session_state.locks['ஐடி கார்டு']: options.append("🪪 ஐடி கார்டு")
    if st.session_state.locks['தொடர்புகள்']: options.append("📞 தொடர்புகள்")
    if st.session_state.locks['புகைப்படம்']: options.append("🖼️ புகைப்படங்கள்")
    if st.session_state.locks['அறிவிப்பு']: options.append("📢 அறிவிப்புகள்")
    if st.session_state.locks['உதவி']: options.append("🆘 உதவி")
    if st.session_state.locks['புகார்']: options.append("📩 புகார் பெட்டி")
    
    if st.session_state.role == "admin": options.append("⚙️ நிர்வாக அறை")
    
    menu = st.radio("மெனு", options)
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# --- 5. பிறந்தநாள் வாழ்த்து ---
if date.today().day == st.session_state.u_dob.day and date.today().month == st.session_state.u_dob.month:
    st.balloons()
    st.success(f"🎂 இனிய பிறந்தநாள் வாழ்த்துக்கள் {st.session_state.u_name}!")

# --- 6. பக்கங்களின் செயல்பாடு ---
if menu == "🏠 முகப்பு":
    st.header(f"🎊 {st.session_state.targets['fest_name']}")
    days = (st.session_state.targets['fest_dt'] - date.today()).days
    st.metric("விழா வர இன்னும்", f"{max(0, days)} நாட்கள்")

elif menu == "📩 புகார் பெட்டி":
    st.header("📩 புகார் பெட்டி")
    if st.session_state.role == "member":
        with st.form("complaint"):
            msg = st.text_area("உங்கள் புகாரை இங்கே எழுதவும் (தலைவருக்கு மட்டுமே தெரியும்)")
            if st.form_submit_button("அனுப்பு"):
                st.session_state.complaints.append({"பெயர்": st.session_state.u_name, "புகார்": msg, "தேதி": date.today()})
                st.success("உங்கள் புகார் தலைவருக்கு அனுப்பப்பட்டது.")
    else:
        st.subheader("வந்த புகார்கள்:")
        for c in st.session_state.complaints:
            st.markdown(f"<div class='complaint-box'><b>{c['பெயர்']}</b> ({c['தேதி']}):<br>{c['புகார்']}</div><br>", unsafe_allow_html=True)

elif menu == "🪪 ஐடி கார்டு":
    st.markdown(f"""<div class="id-card">
        <img src="{LOGO_URL}" width="80"><br>
        <h2>{st.session_state.u_name}</h2>
        <p>மொபைல்: {st.session_state.u_mob}</p>
        <div style="background:#F1C40F; color:black; padding:5px; border-radius:5px;">ID NO: {abs(hash(st.session_state.u_mob))%10000}</div>
    </div>""", unsafe_allow_html=True)

elif menu == "⚙️ நிர்வாக அறை" and st.session_state.role == "admin":
    st.header("⚙️ நிர்வாகக் கட்டுப்பாடு")
    st.session_state.locks['ஐடி கார்டு'] = st.toggle("ஐடி கார்டு பக்கம் திற", value=st.session_state.locks['ஐடி கார்டு'])
    st.session_state.locks['புகார்'] = st.toggle("புகார் பெட்டி திற", value=st.session_state.locks['புகார்'])
    # மற்ற லாக் பட்டன்கள்...
