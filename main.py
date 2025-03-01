import streamlit as st
import pandas as pd
import pydeck as pdk
import json

pages = {
    "My Flighty": [
        st.Page("map.py", title="Map"),
        st.Page("statistics.py", title="Statistics"),
        st.Page("add_info.py", title="Add New Flight"),
        
    ]
}

pg = st.navigation(pages)
pg.run()