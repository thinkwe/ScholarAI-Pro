import streamlit as st
import datetime

# 模拟 AI 生成的内容（在实际部署中，这里可以调用 Gemini API）
def get_daily_content(subject):
    # 这里可以接入 API，根据日期自动生成不重复的知识点
    contents = {
        "语文": "【专题：苏轼的豁达人生】今日学习《定风波》，重点掌握‘归去，也无风雨也无晴’的意境。",
        "英语": "【Vocabulary】Root: 'Spect' (to look). Words: Inspect, Spectacle, Retrospect.",
        "数学": "【解题技巧】几何辅助线的‘三步走’战略：找中点、连对角、构造全等。",
        "社会": "【记忆宫殿】用故事线串联‘工业革命’的三个阶段及关键人物。",
        "科学": "【动手实验】利用家里的白醋和白糖，观察晶体析出过程，记录饱和溶液变化。"
    }
    return contents.get(subject, "正在加载...")

# --- 网页 UI 设计 ---
st.set_page_config(page_title="女儿的智慧花园", layout="wide")

st.title("🌟 ScholarAI：初中专题自动化学习平台")
st.caption(f"今天是：{datetime.date.today()} | 知识已自动更新")

# 侧边栏导航
subject_choice = st.sidebar.radio("选择学科领域", ["语文", "英语", "数学", "社会", "科学"])

# 主界面显示
st.header(f"📚 {subject_choice} 专题深度学习")

col1, col2 = st.columns([2, 1])

with col1:
    st.info(get_daily_content(subject_choice))
    st.write("---")
    st.subheader("📝 今日挑战")
    st.text_area("在下方输入你的思考或解题步骤：", placeholder="AI 会根据你的回答提供反馈...")
    if st.button("提交并获取 AI 点评"):
        st.success("提交成功！AI 正在分析你的答案...（此功能可接入 API 实现自动批改）")

with col2:
    st.markdown("### 📈 学习进度")
    st.progress(65) # 这里可以根据学习记录动态变化
    st.write("✅ 已连续学习：15 天")
    st.write("🔥 词汇量预计增长：1200+")
