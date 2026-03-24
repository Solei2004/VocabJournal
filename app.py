import streamlit as st
import json
import os
from datetime import datetime

# --- 1. 样式与移动端全屏优化 ---
st.set_page_config(page_title="Encounter Vocab", page_icon="📓", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC; }
    .stButton>button { 
        width: 100% !important; 
        height: 50px !important; 
        border-radius: 12px !important;
        font-weight: 600 !important;
    }
    /* 教学引导框：深度逻辑还原 */
    .teaching-box {
        background: #FFFFFF; padding: 20px; border-radius: 10px;
        border: 1px solid #E2E8F0; border-top: 5px solid #2563EB; margin: 15px 0;
    }
    .example-text {
        background: #F0F7FF; padding: 12px; border-radius: 6px;
        border-left: 4px solid #2563EB; font-style: italic; font-size: 15px; margin: 10px 0;
    }
    .logic-list { font-size: 14px; line-height: 1.6; color: #4B5563; }
    .pos-pill {
        background: #EDF2F7; color: #2D3748; padding: 2px 8px;
        border-radius: 6px; font-size: 12px; font-weight: bold; margin-right: 5px; border: 1px solid #CBD5E0;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. 数据引擎 ---
DATA_FILE = 'journal.json'
IMG_DIR = 'my_photos'
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)

if 'means_list' not in st.session_state: st.session_state.means_list = [{"pos": "adj.", "def": ""}]
if 'is_saved' not in st.session_state: st.session_state.is_saved = False
if 'form_iteration' not in st.session_state: st.session_state.form_iteration = 0
if 'editing_id' not in st.session_state: st.session_state.editing_id = None

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try: return json.load(f)
            except: return []
    return []

def save_data(entries):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=4)

POS_OPTIONS = ["n.", "v.", "adj.", "adv.", "prep.", "conj.", "phrase", "interj."]

# --- 3. 页面构建 (Tab 模式) ---
tab_rec, tab_his, tab_set = st.tabs(["✍️ 记录遇见", "📖 翻阅时光", "⚙️ 数据设置"])

with tab_rec:
    with st.container(key=f"v33_form_{st.session_state.form_iteration}"):
        st.subheader("📍 基础信息")
        word = st.text_input("记录新单词", placeholder="如: hypocritical", key=f"w_{st.session_state.form_iteration}", disabled=st.session_state.is_saved).strip()
        
        for i, m in enumerate(st.session_state.means_list):
            c1, c2 = st.columns([1.2, 2.5])
            m['pos'] = c1.selectbox(f"词性 {i+1}", POS_OPTIONS, key=f"p_{i}_{st.session_state.form_iteration}", disabled=st.session_state.is_saved)
            m['def'] = c2.text_input(f"含义 {i+1}", key=f"d_{i}_{st.session_state.form_iteration}", placeholder="中文定义", disabled=st.session_state.is_saved)
        
        if not st.session_state.is_saved:
            b1, b2 = st.columns(2)
            if b1.button("➕ 增加词义"):
                st.session_state.means_list.append({"pos": "adj.", "def": ""})
                st.rerun()
            if b2.button("➖ 移除末行") and len(st.session_state.means_list) > 1:
                st.session_state.means_list.pop(); st.rerun()

        st.subheader("📷 场景化沉浸")
        pic = st.file_uploader("上传照片", type=['jpg','png','jpeg'], key=f"pic_{st.session_state.form_iteration}", disabled=st.session_state.is_saved)
        scene = st.text_area("🚩 遇见场景", key=f"sc_{st.session_state.form_iteration}", placeholder="当时发生了什么？", disabled=st.session_state.is_saved)
        sentence = st.text_area("✍️ 场景化造句", placeholder="描述一个冲突瞬间...", key=f"sent_{st.session_state.form_iteration}", height=100, disabled=st.session_state.is_saved)
        
        # --- 核心教学逻辑回归 ---
        st.markdown(f"""
            <div class="teaching-box">
                <b>💡 为什么不能用“万能模板”造句？</b><br>
                如果你写：<i>“他真的很 hypocritical。”</i> —— 这句话换成 <i>kind, rich, tall</i> 全都通顺。由于场景<b>缺乏排他性</b>，这种记忆是<b>无效</b>的。<br>
                <br><b>✅ 正确示范：</b>
                <div class="example-text">
                    那个男人嘴上说爱她一辈子，但最后背叛了她，他真的好 <b>hypocritical（虚伪的）</b>。
                </div>
                <b>🧠 为什么要这样写？（底层逻辑）：</b>
                <div class="logic-list">
                    <ul>
                        <li><b>场景排他性：</b>“背叛”情节锁死了词义，只有“虚伪”才贴切，不可替代。</li>
                        <li><b>情感锚点：</b>通过背叛带来的愤怒感刺激大脑，加强长期记忆。</li>
                        <li><b>双语辅助：</b>基础薄弱时，用中文铺垫冲突情景，复刻单词灵魂。</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)

    if not st.session_state.is_saved:
        if st.button("💾 封存记录", type="primary"):
            if word and sentence:
                img_path = ""
                if pic:
                    img_path = f"{IMG_DIR}/{datetime.now().timestamp()}.jpg"
                    with open(img_path, "wb") as f: f.write(pic.getbuffer())
                data = load_data(); data.append({
                    "id": datetime.now().strftime("%Y%m%d%H%M%S%f"), "word": word, "meanings": st.session_state.means_list,
                    "scene": scene, "sentence": sentence, "img": img_path, "date": datetime.now().strftime("%Y-%m-%d")
                })
                save_data(data); st.session_state.is_saved = True; st.rerun()
    else:
        st.success("🎉 已封存")
        if st.button("➕ 再记一个", type="primary"):
            st.session_state.form_iteration += 1; st.session_state.is_saved = False
            st.session_state.means_list = [{"pos": "adj.", "def": ""}]; st.rerun()

with tab_his:
    search = st.text_input("🔍 搜索单词、含义或场景...")
    all_entries = load_data()
    filtered = [e for e in all_entries if search.lower() in e['word'].lower() or search in str(e['meanings']) or (e.get('scene') and search in e['scene'])]
    
    for entry in reversed(filtered):
        if st.session_state.editing_id == entry['id']:
            with st.container(border=True):
                st.subheader("📝 修改记录")
                e_w = st.text_input("单词", value=entry['word'], key=f"e_w_{entry['id']}")
                e_m = []
                for i, m in enumerate(entry['meanings']):
                    c1, c2 = st.columns([1, 2])
                    p = c1.selectbox(f"词性 {i+1}", POS_OPTIONS, index=POS_OPTIONS.index(m['pos']), key=f"e_p_{i}_{entry['id']}")
                    d = c2.text_input(f"含义 {i+1}", value=m['def'], key=f"e_d_{i}_{entry['id']}")
                    e_m.append({"pos": p, "def": d})
                e_sc = st.text_area("场景", value=entry.get('scene', ''), key=f"e_sc_{entry['id']}")
                e_sn = st.text_area("造句", value=entry['sentence'], key=f"e_sn_{entry['id']}")
                if st.button("✅ 保存修改", key=f"sv_{entry['id']}", type="primary"):
                    data = load_data()
                    for item in data:
                        if item['id'] == entry['id']: item.update({"word": e_w, "meanings": e_m, "scene": e_sc, "sentence": e_sn})
                    save_data(data); st.session_state.editing_id = None; st.rerun()
                if st.button("❌ 取消", key=f"cl_{entry['id']}"): st.session_state.editing_id = None; st.rerun()
        else:
            header = f"🔤 {entry['word']} | {entry['meanings'][0]['def']}"
            with st.expander(header):
                if entry.get('img'): st.image(entry['img'])
                st.caption(f"🗓️ {entry['date']}")
                st.write(f"🚩 **场景：** {entry.get('scene', '无')}")
                for m in entry['meanings']:
                    st.markdown(f"<span class='pos-pill'>{m['pos']}</span> {m['def']}", unsafe_allow_html=True)
                st.info(f"✍️ **造句：**\n{entry['sentence']}")
                c1, c2 = st.columns(2)
                if c1.button("✏️ 修改", key=f"ed_{entry['id']}"): st.session_state.editing_id = entry['id']; st.rerun()
                if c2.button("🗑️ 删除", key=f"de_{entry['id']}"):
                    new_data = [item for item in load_data() if item['id'] != entry['id']]
                    save_data(new_data); st.rerun()

with tab_set:
    st.subheader("💾 数据管理")
    st.download_button("📤 导出备份 (journal.json)", data=json.dumps(load_data(), ensure_ascii=False, indent=4), file_name="vocab_backup.json", mime="application/json")
    st.info("💡 提示：在手机浏览器点“添加到主屏幕”即可全屏使用。")