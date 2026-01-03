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
    slope = st.sidebar.slider("Slope (%)", -50, 50, 0)
    fuel = st.sidebar.slider("Fuel Load (t/ha)", 0, 30, 10)

    # --- FFDI (McArthur) CALCULATOR --- #
    st.subheader("FFDI Calculation")
    st.write("The FFDI requires inputs of drought factor, temperature, relative humidity and wind speed. Add slope and fine fuel for spread rates.")
    ffdi = ffdi_calc(df, temp, rel_hum, wind_speed)
    fros = fros_calc(ffdi, fuel, slope)
    fireint = fire_int(fuel, df, fros)
    st.write("The FFDI is: ", ffdi) 
    st.write("The forward rate of spread is: ", fros, "km/hr")
    st.write("The fire intensity is: ", fireint, "kW/m")

    if ffdi <= 12:
        st.write("**:blue[No Rating]**")
        st.image("img/fdr-no-rating.svg")
    elif ffdi >= 12 and ffdi <= 23:
        st.write("**:green[Moderate]**")
        st.image("img/fdr-moderate.svg")
    elif ffdi >= 24 and ffdi <= 49:
        st.write("**:orange[High]**")
        st.image("img/fdr-high.svg")
    elif ffdi >= 50 and ffdi <= 99:
        st.write("**:orange[Extreme]**")
        st.image("img/fdr-extreme.svg")
    elif ffdi >= 100:
        st.write("**:red[Catastrophic]**")
        st.image("img/fdr-catastrophic.svg")

    # --- GFDI (McArthur) CALCULATOR --- #
    st.subheader("GFDI Calculation")
    st.write("The GFDI requires inputs of drought factor, temperature, relative humidity, wind speed and curing.")
    gfdi = gfdi_calc(df, temp, rel_hum, wind_speed, curing)
    st.write("The GFDI is: ", gfdi)

    st.subheader("What should I do?")
    st.image("img/afdrs.png")

def ffdi_calc(df, temp, rel_hum, wind_speed):
    ffdi = round(2 * math.exp(-0.45 + 0.987 * math.log(df + 0.001) - 0.03458 * rel_hum + 0.0338 * temp + 0.0234 * wind_speed), 2) # https://dayboro.au/fire-danger-index/
    return ffdi

def gfdi_calc(df, temp, rel_hum, wind_speed, curing):
    gfdi = round(2 * math.exp(-23.6 + 5.01 * math.log(curing) + 0.0281 * temp - 0.226 * math.sqrt(rel_hum) + 0.633 * math.sqrt(wind_speed)), 2)
    return gfdi

def fros_calc(ffdi, fuel, slope):
    fros =  round(0.0012 * ffdi * fuel * math.exp(0.069 * slope), 2)
    return fros

def fire_int(fuel, df, fros):
    fireint = round((516.7 * fuel * df / 10 * fros), 2)
    return fireint

if __name__ == '__main__':
    main()
