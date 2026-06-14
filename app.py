import streamlit as st
import psutil
import platform
import socket
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="Cyber Security Dashboard",
    page_icon="🔐",
    layout="wide"
)

st.title("🔐 Cyber Security Dashboard")
st.markdown("### System Monitoring & Security Analysis")

# System Information
st.subheader("💻 System Information")

col1, col2, col3 = st.columns(3)

with col1:
    st.info(f"OS: {platform.system()}")

with col2:
    st.info(f"Release: {platform.release()}")

with col3:
    st.info(f"Machine: {platform.machine()}")

hostname = socket.gethostname()

try:
    ip_address = socket.gethostbyname(hostname)
except:
    ip_address = "Unavailable"

st.write(f"**Hostname:** {hostname}")
st.write(f"**IP Address:** {ip_address}")

st.divider()

# Resource Monitoring
st.subheader("📊 Resource Monitoring")

cpu_usage = psutil.cpu_percent(interval=1)
memory_usage = psutil.virtual_memory().percent
disk_usage = psutil.disk_usage('/').percent

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("CPU Usage", f"{cpu_usage}%")

with col2:
    st.metric("Memory Usage", f"{memory_usage}%")

with col3:
    st.metric("Disk Usage", f"{disk_usage}%")

data = pd.DataFrame({
    "Resource": ["CPU", "Memory", "Disk"],
    "Usage": [cpu_usage, memory_usage, disk_usage]
})

fig = px.bar(
    data,
    x="Resource",
    y="Usage",
    title="System Resource Usage"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Password Strength Checker
st.subheader("🔑 Password Strength Checker")

password = st.text_input(
    "Enter Password",
    type="password"
)

if password:

    score = 0

    if len(password) >= 8:
        score += 1

    if any(c.isupper() for c in password):
        score += 1

    if any(c.islower() for c in password):
        score += 1

    if any(c.isdigit() for c in password):
        score += 1

    if any(not c.isalnum() for c in password):
        score += 1

    if score <= 2:
        st.error("Weak Password ❌")
    elif score <= 4:
        st.warning("Medium Password ⚠️")
    else:
        st.success("Strong Password ✅")

st.divider()

# Running Processes
st.subheader("⚙️ Running Processes")

processes = []

for proc in psutil.process_iter(['pid', 'name']):
    try:
        processes.append(proc.info)
    except:
        pass

df = pd.DataFrame(processes)

st.dataframe(
    df.head(20),
    use_container_width=True
)

st.divider()

# Security Tips
st.subheader("🛡️ Security Tips")

tips = [
    "Use strong and unique passwords.",
    "Enable Two-Factor Authentication (2FA).",
    "Keep software updated.",
    "Avoid suspicious email links.",
    "Regularly back up important files."
]

for tip in tips:
    st.write(f"✔ {tip}")

st.divider()

st.caption(
    f"Dashboard Generated on {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
)
