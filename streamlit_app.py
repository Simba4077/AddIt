# streamlit_app.py
"""
Streamlit front-end for the “Poster → Google Calendar” workflow
---------------------------------------------------------------
1.  User uploads an image (or snaps one with the webcam)
2.  App posts it to /extract  →  Gemini Vision returns JSON
3.  The returned details are shown in an editable form
4.  User tweaks fields  →  clicks “Save to Google Calendar”
5.  App posts the cleaned data to /create  →  Calendar event is made
6.  Success toast + link to the live event is displayed
"""

import io
import requests
import streamlit as st
from PIL import Image

# ─────────────────────────── Config ─────────────────────────── #
BACKEND_URL = "http://127.0.0.1:5000"   # change if your Flask runs elsewhere
MAX_MB      = 10                        # upload size guard
# ─────────────────────────────────────────────────────────────── #

st.set_page_config(page_title="Add Poster Events", page_icon="📅", layout="centered")
st.title("🎞️  Add Poster Events to Google Calendar")

# 1 ─────────────── Image input (file or webcam) ─────────────── #
uploaded_file = st.file_uploader(
    "Upload a poster image",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=False,
    help=f"Limit {MAX_MB} MB • PNG, JPG",
)

use_cam = st.checkbox("…or capture from webcam")
if use_cam:
    cam_img = st.camera_input("Take a photo")
    if cam_img is not None:
        uploaded_file = cam_img      # treat it like a file-uploader result

# keep things tidy
st.markdown("---")

# 2 ─────────────── Extract button ─────────────── #
if "event_data" not in st.session_state:
    st.session_state["event_data"] = None

extract_btn = st.button("Extract event details", disabled=uploaded_file is None)

if extract_btn:
    if uploaded_file is None:
        st.warning("Please upload or capture an image first.")
        st.stop()

    # Safety: cap file size
    uploaded_file.seek(0, io.SEEK_END)
    mb = uploaded_file.tell() / 1_048_576
    uploaded_file.seek(0)
    if mb > MAX_MB:
        st.error(f"File is {mb:.1f} MB — please use < {MAX_MB} MB.")
        st.stop()

    with st.spinner("Calling Gemini Vision…"):
        files = {"image": (uploaded_file.name, uploaded_file, uploaded_file.type)}
        try:
            resp = requests.post(f"{BACKEND_URL}/extract", files=files, timeout=120)
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")
            st.stop()

    if resp.ok:
        st.session_state["event_data"] = resp.json()
        st.success("Got it! Edit anything below then save to Calendar.")
    else:
        try:
            err = resp.json().get("error", resp.text)
        except ValueError:
            err = resp.text
        st.error(f"Gemini extraction failed:\n\n{err}")
        st.stop()

# 3 ─────────────── Editable form ─────────────── #
if st.session_state["event_data"]:
    data = st.session_state["event_data"]

    with st.form("event_form", clear_on_submit=False):
        title = st.text_input("Title", value=data.get("title", ""))
        col1, col2 = st.columns(2)
        with col1:
            date  = st.text_input("Date (YYYY-MM-DD)", value=data.get("date", ""))
        with col2:
            time  = st.text_input("Time (HH:MM, 24h)", value=data.get("time", ""))
        location    = st.text_input("Location", value=data.get("location", ""))
        description = st.text_area("Description", value=data.get("description", ""), height=120)
        saved = st.form_submit_button("Save to Google Calendar")

    # 4 ─────────────── Save handler ─────────────── #
    if saved:
        payload = {
            "title": title.strip(),
            "date":  date.strip(),
            "time":  time.strip(),
            "location": location.strip(),
            "description": description.strip(),
        }

        with st.spinner("Creating Google Calendar event…"):
            try:
                resp = requests.post(f"{BACKEND_URL}/create", json=payload, timeout=60)
            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {e}")
                st.stop()

        if resp.ok:
            link = resp.json().get("eventLink")
            st.success("✅ Event created!")
            st.markdown(f"[Open event in Google Calendar]({link})",
                        unsafe_allow_html=True)
            # reset so user can add another poster
            st.session_state["event_data"] = None
        else:
            try:
                msg = resp.json().get("error", resp.text)
            except ValueError:
                msg = resp.text
            st.error(f"Failed to create event:\n\n{msg}")
