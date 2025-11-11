import streamlit as st
from datetime import timedelta, date
from hijridate import Hijri, Gregorian

st.set_page_config(page_title="Hijri ↔ Gregorian Converter", layout="centered")

st.title("🕌 Hijri ↔ Gregorian Date Converter")

st.write("Enter a date in either Hijri (e.g., 05/09/1405) or Gregorian (e.g., 25/05/1985).")

date_input = st.text_input("Enter date (DD/MM/YYYY):", "")

def is_hijri_date(day, month, year):
    return year < 1600

def convert_line(date_str):
    try:
        day, month, year = map(int, date_str.split('/'))
        if is_hijri_date(day, month, year):
            # Hijri → Gregorian (+1 day correction)
            g = Hijri(year, month, day).to_gregorian()
            g_date = date(g.year, g.month, g.day) + timedelta(days=1)
            return f"{g_date.day:02d}/{g_date.month:02d}/{g_date.year}", "Hijri → Gregorian"
        else:
            # Gregorian → Hijri
            h = Gregorian(year, month, day).to_hijri()
            return f"{h.day:02d}/{h.month:02d}/{h.year}", "Gregorian → Hijri"
    except Exception as e:
        return f"Invalid date format ({e})", None

if date_input:
    result, mode = convert_line(date_input)
    if mode:
        st.success(f"**{mode}:** {result}")
    else:
        st.error(result)
