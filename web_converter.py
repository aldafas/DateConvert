# web_converter_file_clean.py
import streamlit as st
from datetime import timedelta, date
from hijridate import Hijri, Gregorian
import pandas as pd

st.set_page_config(page_title="Hijri ↔ Gregorian Converter", layout="centered")
st.title("🕌 Hijri ↔ Gregorian Date Converter (Batch File)")

st.write("""
Upload a text file with dates (one per line) in **DD/MM/YYYY** format.
The app will detect if each date is Hijri or Gregorian and convert it.
""")

uploaded_file = st.file_uploader("Choose a text file", type=["txt"])


def is_hijri_date(day, month, year):
    """Rough check: Hijri years are usually < 1600"""
    return year < 1600


def convert_line(date_str):
    """Convert one date line between Hijri and Gregorian with 1-day Hijri fix."""
    date_str = date_str.strip()
    if not date_str:
        return "", ""
    try:
        day, month, year = map(int, date_str.split('/'))

        if is_hijri_date(day, month, year):
            # Hijri → Gregorian (+1 day correction)
            g = Hijri(year, month, day).to_gregorian()
            g_date = date(g.year, g.month, g.day) + timedelta(days=1)
            return date_str, f"{g_date.day:02d}/{g_date.month:02d}/{g_date.year}"
        else:
            # Gregorian → Hijri (no correction)
            h = Gregorian(year, month, day).to_hijri()
            return date_str, f"{h.day:02d}/{h.month:02d}/{h.year}"
    except Exception:
        return date_str, "Invalid"


if uploaded_file:
    # Read lines from uploaded file
    lines = uploaded_file.read().decode("utf-8").splitlines()

    # Convert each line
    results = [convert_line(line) for line in lines if line.strip()]

    # Create DataFrame for table display
    df = pd.DataFrame(results, columns=["Original Date", "Converted Date"])

    st.subheader("Conversion Results")
    st.table(df)

    # Optional: allow download of results as text file
    output_text = "\n".join([f"{orig}\t{conv}" for orig, conv in results])
    st.download_button(
        label="Download Results",
        data=output_text,
        file_name="converted_dates.txt",
        mime="text/plain"
    )
