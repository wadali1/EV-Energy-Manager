import streamlit as st

st.set_page_config(page_title="EV Energy Manager", layout="wide")


st.markdown(
    """
    <style>
    .title-container {
        text-align: center;
        padding-top: 20px;
    }
    .title-container h1 {
        font-size: 36px;
    }
    .title-container h3 {
        font-size: 20px;
        color: #6c757d;
    }
    .main-container {
        text-align: center;
        margin-top: 50px;
    }
    </style>
    <div class="title-container">
        <h1>⚡ EV Energy Manager</h1>
        <h3>A smart dashboard for monitoring EV charging and energy distribution</h3>
    </div>
    """,
    unsafe_allow_html=True,
)


st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to:", ["Home", "Charging Overview", "Energy Analysis"])

st.sidebar.header("⚙️ Configuration")
st.sidebar.markdown("### Select Number of Chargers")

num_level2_chargers = st.sidebar.slider("Level 2 Chargers", 1, 10, 5)
num_level3_chargers = st.sidebar.slider("Level 3 Chargers", 1, 5, 3)

st.markdown('<div class="main-container">', unsafe_allow_html=True)


if page == "Home":
    st.markdown("<h2>🏠 Welcome to the EV Energy Manager Dashboard!</h2>", unsafe_allow_html=True)
    st.markdown("<p>Use the sidebar to navigate different sections and customize filters.</p>", unsafe_allow_html=True)

elif page == "Charging Overview":
    st.markdown("<h2>📊 Charging Overview</h2>", unsafe_allow_html=True)
    st.markdown("<p>This section will display real-time charging statistics and insights.</p>", unsafe_allow_html=True)

elif page == "Energy Analysis":
    st.markdown("<h2>🔍 Energy Analysis</h2>", unsafe_allow_html=True)
    st.markdown("<p>This section will provide detailed energy consumption trends.</p>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
