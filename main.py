import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

fig_colors = ['Set1', 'Set2', 'Set3', 'tab10' ,'deep', 'hls', 'husl', 'rocket_r', 'YlOrBr', 'Spectral']

df_matches = pd.read_csv('IPL Matches 2008-2020.csv')




import streamlit as st


radio = st.sidebar.radio('Main Menu : ', ('Match Stats', 'Player stats', 'Dream 11'))
if radio == 'Match Stats':
  st.header('IPL Team Wise Data' )


elif radio == 'Player stats':
  st.header('IPL Players Data' ) 


elif radio == 'Dream 11':
  st.header('AI Based Recommended Dream11 Players' )

