"""Streamlit website for both demos. Run: streamlit run streamlit_app.py"""
import streamlit as st
from fleet_orchestrator import simulate
from perception_vv import evaluate

st.set_page_config(page_title="Fleet Orchestration and Perception V&V", layout="wide")
st.title("Fleet Orchestration and Perception V&V")
st.write("Two teaching demos on synthetic data only. Neither uses Zoox data, "
         "and neither is a production dispatch or safety validation system.")

tab1, tab2 = st.tabs(["Fleet orchestration", "Perception V&V"])

with tab1:
    st.header("Fleet orchestration simulator")
    st.write("Riders appear near two demand hotspots. Vehicles are assigned "
             "greedily to the nearest rider, and idle vehicles stage toward hotspots.")
    n_v = st.slider("Vehicles", 5, 50, 20)
    n_r = st.slider("Riders", 20, 300, 100)
    if st.button("Run fleet simulation"):
        r = simulate(n_vehicles=n_v, n_riders=n_r)
        st.write(r)

with tab2:
    st.header("Perception verification and validation")
    st.write("Synthetic ground truth and detector outputs, matched by centre "
             "distance, with precision, recall, F1, and failure rates by condition.")
    noise = st.slider("Detection noise", 0.0, 1.0, 0.3)
    if st.button("Run perception evaluation"):
        r = evaluate(noise=noise)
        st.write(r)
        st.table([{"condition": k, "failure_rate": v}
                  for k, v in r["failure_rate_by_condition"].items()])
