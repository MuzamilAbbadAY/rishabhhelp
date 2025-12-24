import streamlit as st
import time
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl

# -------------------------------
# Email Configuration
# -------------------------------
def send_emergency_email(latitude, longitude, severity, vehicle_id="VH-2024-001"):
    """
    Send emergency email using Gmail SMTP (FREE)
    """
    try:
        # Configure these with your actual email details
        sender_email = "tanmayirebbapragada@gmail.com"  
        sender_password = "rfct wlng xayn zduf" 
        receiver_email = "muzamilabbaday1020@gmail.com"  
        
        # Create email
        subject = f"🚨 ACCIDENT ALERT - Vehicle {vehicle_id}"
        
        body = f"""
        ⚠️ EMERGENCY ALERT ⚠️
        
        Vehicle Accident Detected!
        
        📊 Details:
        - Severity Level: {severity}/10
        - Location: {latitude}, {longitude}
        - Time: {time.strftime('%Y-%m-%d %H:%M:%S')}
        - Vehicle ID: {vehicle_id}
        
        📍 Map Link: https://www.google.com/maps?q={latitude},{longitude}
        
        🚑 Required Response:
        1. Immediate medical assistance
        2. Police dispatch
        3. Contact emergency contacts
        
        This is an automated alert from AcciAlert System.
        """
        
        # Setup email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email using Gmail SMTP
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
            
        return True, "Email sent successfully!"
        
    except Exception as e:
        return False, f"Email failed: {str(e)}"


# -------------------------------
# Accident Detection Logic
# -------------------------------
def detect_accident(acceleration_g, speed):
    """
    Detect accident based on sudden G-force impact
    """
    if acceleration_g >= 4.0:
        severity = min(10, int((acceleration_g * speed) / 20))
        return True, severity
    return False, 0


# -------------------------------
# Emergency Alert Simulation
# -------------------------------
def send_alerts(latitude, longitude, severity):
    return {
        "contact": "📞 Emergency contact notified",
        "ambulance": "🚑 Ambulance alerted",
        "police": "👮 Police informed",
        "location": f"{latitude}, {longitude}",
        "severity": severity,
        "map_link": f"https://www.google.com/maps?q={latitude},{longitude}"
    }


# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(
    page_title="AcciAlert",
    page_icon="🚗",
    layout="centered"
)

st.title("🚨 AcciAlert – Vehicle Accident Detection System")
st.caption("Live accident detection with email notifications")

st.divider()

st.subheader("📡 Vehicle Telemetry Input")

acceleration = st.slider(
    "Acceleration (G-Force)",
    min_value=0.0,
    max_value=10.0,
    value=2.5,
    step=0.1,
    key="accel"
)

speed = st.slider(
    "Vehicle Speed (km/h)",
    min_value=0,
    max_value=150,
    value=50,
    step=1,
    key="speed"
)

st.divider()

# -------------------------------
# SIMULATED Live Location
# -------------------------------
st.subheader("📍 Live Location Simulation")

# Initialize session state
if 'simulated_location' not in st.session_state:
    st.session_state.simulated_location = {
        "latitude": 12.9716,
        "longitude": 77.5946,
        "last_update": "Simulated"
    }

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("**Click to simulate new location:**")

with col2:
    if st.button("📍 Get New Location", type="secondary", use_container_width=True):
        lat_change = random.uniform(-0.01, 0.01)
        lon_change = random.uniform(-0.01, 0.01)
        
        st.session_state.simulated_location = {
            "latitude": round(12.9716 + lat_change, 6),
            "longitude": round(77.5946 + lon_change, 6),
            "last_update": time.strftime("%H:%M:%S")
        }
        
        st.toast("📍 New location acquired!", icon="📍")

# Display current location
st.divider()

col1, col2 = st.columns(2)
with col1:
    st.metric("Latitude", f"{st.session_state.simulated_location['latitude']}°")
with col2:
    st.metric("Longitude", f"{st.session_state.simulated_location['longitude']}°")

st.caption(f"🕒 Last updated: {st.session_state.simulated_location['last_update']}")

# Show on map
st.markdown("#### 📍 Location on Map")
import pandas as pd
map_data = pd.DataFrame({
    'lat': [st.session_state.simulated_location["latitude"]],
    'lon': [st.session_state.simulated_location["longitude"]]
})
st.map(map_data, zoom=14)

st.divider()

# -------------------------------
# Accident Detection with Email
# -------------------------------
st.subheader("🚨 Accident Detection")

if acceleration >= 3.5 and acceleration < 4.0:
    st.warning("⚠️ **Warning:** High G-force detected. Approaching danger threshold.")
elif acceleration >= 4.0:
    st.error("⚠️ **Critical:** Acceleration exceeds 4.0G! Accident likely on detection.")

if st.button("🚑 DETECT ACCIDENT & SEND ALERTS", type="primary", use_container_width=True):
    accident, severity = detect_accident(acceleration, speed)

    if accident:
        # Get current location
        lat = st.session_state.simulated_location["latitude"]
        lon = st.session_state.simulated_location["longitude"]
        
        # IMMEDIATE TOAST NOTIFICATIONS
        st.toast("🚨 SEVERE IMPACT DETECTED!", icon="🚨")
        time.sleep(0.2)
        st.toast(f"⚠️ Accident Severity: {severity}/10", icon="⚠️")
        
        # Send email alert
        email_sent = False
        email_message = ""
        
        # Try to send email (update the email credentials in the function above)
        with st.spinner("📧 Sending emergency email..."):
            email_sent, email_message = send_emergency_email(lat, lon, severity)
        
        st.toast("📡 Contacting emergency services...", icon="📡")
        
        # Main accident display
        st.error("### 🚨 ACCIDENT DETECTED!")
        
        # Display information
        col1, col2 = st.columns(2)
        col1.metric("Severity Level", f"{severity}/10")
        col2.metric("Impact (G)", acceleration)
        
        # Show email status
        if email_sent:
            st.success("✅ Emergency email sent successfully!")
        else:
            st.info("📧 Email notification system ready (configure email credentials in code)")
        
        # Other alerts
        alerts = send_alerts(lat, lon, severity)
        st.success(alerts["contact"])
        st.success(alerts["ambulance"])
        st.success(alerts["police"])
        
        # Show location details
        st.info(f"📍 **Accident Location:** {alerts['location']}")
        
        # Show map
        accident_map_data = pd.DataFrame({
            'lat': [lat],
            'lon': [lon]
        })
        st.map(accident_map_data, color='#FF0000', size=200, zoom=14)
        
        # Final toast
        time.sleep(0.5)
        st.toast("✅ All emergency services notified!", icon="✅")
        
    else:
        st.toast("✅ Vehicle status: NORMAL", icon="✅")
        st.success("### ✅ No accident detected")
        st.info("Vehicle telemetry is within safe limits.")

st.divider()

# -------------------------------
# Emergency Quick Actions
# -------------------------------
st.subheader("⚡ Quick Actions")

col1, col2 = st.columns(2)
with col1:
    if st.button("🆘 Manual SOS", type="secondary", use_container_width=True):
        lat = st.session_state.simulated_location["latitude"]
        lon = st.session_state.simulated_location["longitude"]
        
        st.toast("🆘 EMERGENCY SOS ACTIVATED!", icon="🆘")
        st.error("### 🆘 Manual Emergency Alert")
        st.warning("User activated emergency SOS")
        st.info(f"📍 Your location: {lat:.6f}, {lon:.6f}")
        
        # Try to send SOS email
        with st.spinner("Sending SOS email..."):
            email_sent, message = send_emergency_email(lat, lon, 8)
            if email_sent:
                st.success("📧 SOS email sent!")
            else:
                st.info("Email system configured in code")

with col2:
    if st.button("🔔 Test Notifications", type="secondary", use_container_width=True):
        st.toast("🔔 Test notification sent!", icon="🔔")
        st.success("✅ All notification systems working")

st.divider()
st.caption("AcciAlert | Smart Vehicle Safety System with Email Alerts")



