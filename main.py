import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

def main():

    # --- PAGE CONFIG AND TITLE --- #
    st.set_page_config(page_title = "FDI Calc", layout = "wide")
    st.title("Fire Danger Rating Calculator :fire:")
    st.sidebar.title("Data Inputs")

    # --- DATA INPUT SLIDERS --- #
    df = st.sidebar.slider("Drought Factor", 0, 10, 8)

    temp = st.sidebar.slider("Temperature (C)", 0, 50, 35)

    rel_hum = st.sidebar.slider("Relative Humidity", 0, 100, 20)

    wind_speed = st.sidebar.slider("Wind Speed (km/h)", 0, 100, 30)

    curing = st.sidebar.slider("Curing (%)", 0, 100, 50)

    # --- FFDI (McArthur) CALCULATOR --- #
    st.subheader("FFDI Calculation")
    st.write("The FFDI requires inputs of drought factor, temperature, relative humidity and wind speed.")
    ffdi = ffdi_calc(df, temp, rel_hum, wind_speed)
    st.write("The FFDI is: ", ffdi)

    # --- GFDI (McArthur) CALCULATOR --- #
    st.subheader("GFDI Calculation")
    st.write("The GFDI requires inputs of drought factor, temperature, relative humidity, wind speed and curing.")
    gfdi = gfdi_calc(df, temp, rel_hum, wind_speed, curing)
    st.write("The GFDI is: ", gfdi)

def ffdi_calc(df, temp, rel_hum, wind_speed):
    ffdi = 2 * math.exp(-0.45 + 0.987 * math.log(df + 0.001) - 0.03458 * rel_hum + 0.0338 * temp + 0.0234 * wind_speed) # https://dayboro.au/fire-danger-index/
    return ffdi

def gfdi_calc(df, temp, rel_hum, wind_speed, curing):
    gfdi = 2 * math.exp(-23.6 + 5.01 * math.log(curing) + 0.0281 * temp - 0.226 * math.sqrt(rel_hum) + 0.633 * math.sqrt(wind_speed))
    return gfdi

if __name__ == '__main__':
    main()
