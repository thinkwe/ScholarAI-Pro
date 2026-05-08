import streamlit as st
import google.generativeai as genai
import datetime

# --- 配置页面 ---
st.set_page_config(
    page_title="ScholarAI | 初中生智能全能学习站",
    page_icon="🎓",
    layout="wide"
)

# --- 侧边栏：配置与导航 ---
st.sidebar.title("⚙️ 控制面板")

# 优先从 Streamlit Secrets 获取 API KEY，如果没有则提示输入
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("请输入 Gemini API Key:", type="password")

if not api_key:
    st.warning("⚠️ 请在侧边栏配置 API Key 以启用 AI 自动化功能。")
    st.stop()

# 初始化 AI 引擎
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

subject = st.sidebar.selectbox(
    "选择学习科目",
    ["语文", "英语", "数学", "社会", "科学"]
)

# --- 核心逻辑：自动化内容生成 ---
def get_automated_lesson(subject):
    today = datetime.date.today()
    # 构造针对性极强的 Prompt，确保知识点符合初中水平并具有深度
    prompt = f"""
    你是一名经验丰富的初中全科名师。今天是 {today}。
    请为学生生成一个关于【{subject}】的深度学习专题。
    
    具体要求：
    1. **专题深度**：不要只列出基础知识，要包含解题思路、思维方法或背景深度。
    2. **模块化内容**：
       - 【今日目标】：明确今天要掌握的 1 个核心能力。
       - 【知识精讲】：深入浅出的讲解。如果是数学/科学，请包含典型公式或原理。
       - 【案例拆解】：一个具体的例题或现象分析。
       - 【随堂挑战】：出一道启发性的题目，要求学生回答。
    3. **格式**：使用 Markdown 格式，多用粗体、列表和引用，使其易于阅读。
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"内容生成失败，请检查网络或 API 额度：{str(e)}"

def get_ai_feedback(content, student_answer):
    feedback_prompt = f"""
    作为老师，请根据以下教学内容和学生的回答进行批改：
    ---
    教学专题内容：{content}
    学生的回答：{student_answer}
    ---
    要求：
    1. 给予鼓励性评价。
    2. 指出回答中的亮点和不足。
    3. 如果有错，请提供详细的解析和正确答案。
    """
    try:
        response = model.generate_content(feedback_prompt)
        return response.text
    except Exception as e:
        return f"批改失败：{str(e)}"

# --- 主界面 UI ---
st.title(f"🚀 {subject} 专题：自动深度学习平台")
st.caption(f"📅 学习进度更新日期：{datetime.date.today()} | 状态：AI 实时赋能")

# 利用 Session State 缓存今日内容，防止页面刷新导致 API 重复调用（节省额度）
cache_key = f"lesson_{subject}_{datetime.date.today()}"
if cache_key not in st.session_state:
    with st.spinner(f"AI 老师正在撰写【{subject}】专题内容..."):
        st.session_state[cache_key] = get_automated_lesson(subject)

# 显示内容
st.markdown("---")
st.markdown(st.session_state[cache_key])

# --- 互动区 ---
st.divider()
st.subheader("📝 互动练习与思考")
answer = st.text_area("请在此处输入你的回答、解题步骤或实验心得：", height=200, placeholder="写下你的想法，AI 老师会实时批改...")

col1, col2 = st.columns([1, 4])
with col1:
    submit_btn = st.button("提交批改", type="primary")

if submit_btn:
    if answer.strip():
        with st.spinner("正在分析你的回答..."):
            feedback = get_ai_feedback(st.session_state[cache_key], answer)
            st.success("✅ 批改已完成！")
            st.markdown("### 👨‍🏫 老师反馈")
            st.info(feedback)
    else:
        st.warning("内容不能为空，请输入你的思考。")

# --- 底部装饰 ---
st.sidebar.markdown("---")
st.sidebar.write("✨ **学习小贴士**：")
st.sidebar.caption("每天换一个科目，保持大脑的交叉记忆活性。科学证明这种方式比单科突击更高效。")
