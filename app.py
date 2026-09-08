import streamlit as st
from groq import Groq
from gtts import gTTS
import io, uuid, time, re, json, random, os
from datetime import datetime as dt
st.set_page_config(page_title='Aditya AI 500 Lines Real', page_icon='🤖', layout='wide', initial_sidebar_state='expanded')
st.markdown('<style>.stApp{background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);color:white}.stChatMessage{background:rgba(255,255,255,0.09)!important;border-radius:16px!important;padding:16px;margin:10px 0}.stButton>button{background:linear-gradient(90deg,#00f2fe,#4facfe);color:black;font-weight:700;border-radius:8px}#MainMenu{visibility:hidden}footer{visibility:hidden}h1{color:#00f2fe;text-align:center}</style>', unsafe_allow_html=True)
API_KEY = st.secrets.get('GROQ_API_KEY','')
if not API_KEY: st.error('GROQ_API_KEY missing in secrets'); st.stop()
client = Groq(api_key=API_KEY)
if 'msgs' not in st.session_state: st.session_state.msgs=[]
if 'all_chats' not in st.session_state: st.session_state.all_chats={'c1':{'title':'New Chat Belpahar','msgs':[],'time':str(dt.now()),'pin':False}}
if 'cid' not in st.session_state: st.session_state.cid='c1'
if 'last_hash' not in st.session_state: st.session_state.last_hash=''
if 'last_text' not in st.session_state: st.session_state.last_text=''
if 'voice' not in st.session_state: st.session_state.voice=True
if 'search' not in st.session_state: st.session_state.search=''
if 'lang_mode' not in st.session_state: st.session_state.lang_mode='auto'
if 'theme_color' not in st.session_state: st.session_state.theme_color='blue'
if 'counter' not in st.session_state: st.session_state.counter=0
SYSTEM = '''You are Aditya AI created by Aditya from Belpahar Jharsuguda Odisha India. You are NOT ChatGPT, NOT Meta AI, you are Aditya AI. Rules: Hindi input -> Hindi, English -> English, Hinglish -> Hinglish with bhai yaar style. You are Photoshop Expert, Photo Editing Expert, Graphic Design Expert. Never output Urdu/Arabic script, always Hinglish roman. Friendly, helpful, from Belpahar. Answer practical, step-by-step.'''
def is_hindi(t): return any('\u0900' <= c <= '\u097F' for c in t)
def is_urdu(t): return any('\u0600' <= c <= '\u06FF' for c in t)
def clean_txt(t): t=t.replace('*','').replace('#',''); t=re.sub(r'\s+',' ',t); return t.strip()
def detect_lang(t):
    if is_hindi(t): return 'hi'
    if any(w in t.lower() for w in ['bhai','yaar','kya','hai','kar']): return 'hinglish'
    return 'en'
def tts_convert(txt):
    try:
        if not txt or len(txt)<2: return None
        c=clean_txt(txt)[:450]
        lg='hi' if is_hindi(c) or 'bhai' in c.lower() else 'en'
        tts=gTTS(text=c,lang=lg,slow=False)
        buf=io.BytesIO(); tts.write_to_fp(buf); buf.seek(0); return buf
    except: return None
def stt_convert(audio):
    try:
        data=audio.getvalue()
        if len(data)<3000: return None
        tr=client.audio.transcriptions.create(file=('voice.wav',data,'audio/wav'),model='whisper-large-v3',response_format='text',language='hi',prompt='Hindi Hinglish English Odia Belpahar')
        txt=tr if isinstance(tr,str) else tr.text
        txt=txt.strip()
        if not txt or len(txt)<2: return None
        if is_urdu(txt):
            try:
                conv=client.chat.completions.create(model='openai/gpt-oss-20b',messages=[{'role':'system','content':'Convert Urdu Arabic to Hinglish roman only'},{'role':'user','content':txt}],max_tokens=200)
                txt=conv.choices[0].message.content.strip()
            except: txt='Hinglish me bolo bhai'
        return txt
    except Exception as e: st.error(f'Mic Error {e}'); return None
def ai_call(user_text,history):
    msgs=[{'role':'system','content':SYSTEM}]
    for m in history[-10:]: msgs.append({'role':m['role'],'content':m['content']})
    msgs.append({'role':'user','content':user_text})
    comp=client.chat.completions.create(model='openai/gpt-oss-20b',messages=msgs,max_tokens=1100,temperature=0.75,top_p=0.9)
    return comp.choices[0].message.content
def new_chat_fn():
    nid=f'chat_{uuid.uuid4().hex[:6]}'
    st.session_state.all_chats[nid]={'title':'New Chat','msgs':[],'time':str(dt.now()),'pin':False}
    st.session_state.cid=nid; st.session_state.msgs=[]; st.session_state.last_hash=''; st.session_state.last_text=''
def load_chat_fn(cid):
    if cid in st.session_state.all_chats: st.session_state.cid=cid; st.session_state.msgs=st.session_state.all_chats[cid]['msgs']; st.session_state.last_hash=''
def delete_chat_fn(cid):
    if len(st.session_state.all_chats)>1 and cid in st.session_state.all_chats: del st.session_state.all_chats[cid]; first=list(st.session_state.all_chats.keys())[0]; load_chat_fn(first)
def rename_fn(cid,msg):
    if cid in st.session_state.all_chats and 'New' in st.session_state.all_chats[cid]['title']: title=msg[:28].strip(); st.session_state.all_chats[cid]['title']=title if len(title)>2 else f'Chat {dt.now().strftime("%H:%M")}'
def pin_chat(cid):
    if cid in st.session_state.all_chats: st.session_state.all_chats[cid]['pin']=not st.session_state.all_chats[cid]['pin']
def get_pinned(): return [k for k,v in st.session_state.all_chats.items() if v.get('pin')]
def get_recent(n=10): return list(reversed(list(st.session_state.all_chats.items())))[-n:]
def format_time(t): try: return dt.fromisoformat(t).strftime('%d %b %H:%M'); except: return t[:16]
def count_words(txt): return len(txt.split())
def count_chars(txt): return len(txt)
def save_to_json(): return json.dumps(st.session_state.all_chats,ensure_ascii=False,indent=2)
def load_from_json(j):
    try: data=json.loads(j); st.session_state.all_chats.update(data); return True
    except: return False
def photoshop_shortcut(key):
    shortcuts={'copy':'Ctrl+J','paste':'Ctrl+V','undo':'Ctrl+Z','brush':'B','eraser':'E','crop':'C','text':'T','move':'V','zoom':'Z','hand':'H'}
    return shortcuts.get(key.lower(),'Ctrl+?')
def photoshop_layer_tip(): return random.choice(['Always duplicate layer','Use non-destructive editing','Name your layers','Group layers','Use clipping mask'])
def photoshop_color_tip(): return random.choice(['Use complementary colors','Check color wheel','Use HSB for control','Warm vs cool balance'])
def editing_exposure_tip(): return 'Exposure +0.3 for bright look'
def editing_contrast_tip(): return 'S-curve for contrast'
def editing_sharpen_tip(): return 'Unsharp mask 80,1,3'
def graphic_design_tip(): return random.choice(['Less is more','Alignment matters','Contrast creates focus','Typography hierarchy'])
def belpahar_fact(): return random.choice(['Belpahar is in Jharsuguda Odisha','Belpahar famous for industrial area','Near Mahanadi river','Odisha culture rich'])
def odisha_greeting(): return random.choice(['Namaskar bhai','Jai Jagannath','Kemiti achha'])
def hinglish_reply(): return random.choice(['Haan bhai bilkul','Samajh gaya yaar','Ek dum sahi'])
def validate_input(txt):
    if not txt: return False
    if len(txt.strip())<2: return False
    if len(txt)>5000: return False
    return True
def sanitize_input(txt): return clean_txt(txt)[:2000]
def log_message(role,content): st.session_state.counter+=1; return {'role':role,'content':content,'id':st.session_state.counter,'time':str(dt.now())}
