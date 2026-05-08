import streamlit as st
from openai import OpenAI
import datetime

# --- 1. 页面配置 ---
st.set_page_config(
    page_title="ScholarAI Pro | MiniMax M2.7 驱动", 
    page_icon="🎓", 
    layout="wide"
)

# --- 2. 侧边栏：安全配置 ---
st.sidebar.title("🛠️ 教师端配置")
# 建议在 Streamlit Secrets 中配置，此处为本地调试入口
# --- 修改后的强制读取代码 ---
try:
    # 尝试从 Secrets 字典中直接获取
    minimax_api_key = st.secrets["MINIMAX_API_KEY"]
    minimax_group_id = st.secrets["MINIMAX_GROUP_ID"]
except Exception:
    # 如果后台没找到，才显示输入框
    st.sidebar.warning("🔑 后台 Secrets 配置未生效")
    minimax_api_key = st.sidebar.text_input("MiniMax API Key:", type="password")
    minimax_group_id = st.sidebar.text_input("MiniMax Group ID:")

if not minimax_api_key or not minimax_group_id:
    st.info("💡 请先在 Streamlit 后台配置 Secrets 或手动输入。")
    st.stop()
# 初始化 OpenAI 兼容客户端
client = OpenAI(
    api_key=minimax_api_key,
    base_url="https://api.minimax.chat/v1",
)

subject = st.sidebar.selectbox(
    "选择今日研究专题", 
    ["语文", "英语", "数学", "社会", "科学"]
)

# --- 3. 自动化专题引擎 ---
def generate_m27_content(subject):
    today = datetime.date.today()
    
    # 针对 M2.7 模型优化的深度 Prompt
    # M2.7 擅长处理复杂逻辑，所以我们可以要求它输出更具深度的内容
    prompts = {
        "语文": f"今天是{today}。作为语文名师，请针对初中生生成一个‘深度文学素养’专题。要求：包含一篇经典散文/古文的文本细读、3个高阶修辞手法解析、以及一个联想写作练习。",
        "英语": f"今天是{today}。请生成‘完形填空逻辑拆解’专题。通过一段150词左右的语篇，讲解上下文线索（Clues）的寻找方法，并标注3个核心短语的变式用法。",
        "数学": f"今天是{today}。请讲解一个初中数学压轴题模型（如：中点模型、路径最值问题）。要求：用 LaTeX 格式书写公式，包含‘模型构造-例题示范-解析思维导图’。",
        "社会": f"今天是{today}。请结合历史与地理，分析一个‘文明交汇点’（如丝绸之路或大航海时代）。要求：用逻辑链条串联因果关系，并提供一个辅助记忆的结构化框架。",
        "科学": f"今天是{today}。请设计一个‘探索性实验’专题（如：探究影响电磁铁磁性强弱的因素）。要求：包含假设、变量控制、实验步骤及原理的深度推导。"
    }

    try:
        response = client.chat.completions.create(
            model="MiniMax-M2.7", # 这是 M2.7 系列在 API 中的标准 ID
            messages=[
                {"role": "system", "content": "你是一名基于 MiniMax M2.7 技术的全科特级教师。你的教学特点是：逻辑缜密、善于启发、注重知识的底层逻辑而非死记硬背。"},
                {"role": "user", "content": prompts[subject]}
            ],
            extra_headers={"GroupId": minimax_group_id}
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ M2.7 引擎调度错误: {str(e)}"

# --- 4. 主界面布局 ---
st.title(f"🚀 ScholarAI Pro：{subject}自动深化学习")
st.caption(f"Powered by MiniMax M2.7 | 知识体系每天自动更新")

# 缓存机制：确保一天内同一科目只消耗一次 API 额度
cache_key = f"m27_{subject}_{datetime.date.today()}"
if cache_key not in st.session_state:
    with st.spinner("M2.7 正在构思今日深度专题..."):
        st.session_state[cache_key] = generate_m27_content(subject)

# 展示生成的教学内容
st.markdown("---")
st.markdown(st.session_state[cache_key])

# --- 5. 交互式反馈（AI 批改） ---
st.divider()
st.subheader("📝 学生反馈与在线作业")
user_submission = st.text_area("请在此输入你的解题步骤、练习答案或对今日专题的疑问：", height=200)

if st.button("提交给 M2.7 老师点睛"):
    if user_submission:
        with st.spinner("M2.7 正在进行深度逻辑评估..."):
            correction_prompt = f"针对专题：{st.session_state[cache_key]}\n学生的反馈是：{user_submission}\n请进行精细化批改。如果是疑问，请给出引导性回答而非直接给答案。"
            
            feedback = client.chat.completions.create(
                model="minimax-text-01",
                messages=[
                    {"role": "system", "content": "你负责对学生的作业进行‘点睛式’批改。"},
                    {"role": "user", "content": correction_prompt}
                ],
                extra_headers={"GroupId": minimax_group_id}
            )
            st.success("✅ 批改完成！")
            st.markdown("### 👨‍🏫 老师点评")
            st.info(feedback.choices[0].message.content)
    else:
        st.warning("请先填写你的学习反馈。")
