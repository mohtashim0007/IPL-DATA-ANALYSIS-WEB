

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import cv2
import streamlit as st

fig_colors = ['Set1', 'Set2', 'Set3', 'tab10' ,'deep', 'hls', 'husl', 'rocket_r', 'YlOrBr', 'Spectral']

df_matches = pd.read_csv('IPL Matches 2008-2020.csv')






#matches_won_by_team1_team2

def matches_won_by_team1_team2(team1, team2):
  temp1 = df_matches[ (df_matches['team1'] == team1) & (df_matches['team2']==team2)]
  temp2 = df_matches[ (df_matches['team1'] == team2) & (df_matches['team2']==team1)]

  total_matches = temp1.shape[0] + temp2.shape[0]

  #Matches won by the teams
  matches_won_by_team1 = temp1[temp1['winner'] == team1].shape[0] + temp2[temp2['winner'] == team1].shape[0]

  st.write('Total matches played = ', total_matches)
  st.write('Matches won by ', team1 ,'= ',matches_won_by_team1)
  st.write('Win Percentages = ', round((matches_won_by_team1*100)/total_matches, 2), '%')

  new_df = pd.concat([temp1,temp2], ignore_index = True)

  #plotting
  fig = plt.figure(figsize=(5,5))
  sns.countplot(x = 'winner', data = new_df,dodge= False, palette = np.random.choice(fig_colors))
  plt.title('Matches won against each other')
  plt.xlabel('Teams Name')
  plt.ylabel('Matches Won')
  plt.savefig('fig1.jpg')
  img = cv2.imread('fig1.jpg')
  img = cv2.resize(img, (480,424))
  _,col,_ = st.columns([1,2,1])
  with col:
    st.image(img)
  




radio = st.sidebar.radio('Main Menu :', ('Match Stats', 'Player stats', 'Dream 11'))
if radio == 'Match Stats':
  _,col,_ = st.columns([1,2,1])
  with col:
    st.header('IPL Team Wise Data' )
  st.text('')
  if st.checkbox('Comparision of two IPL Teams'):
    team_names_list =['Royal Challengers Bangalore', 'Kings XI Punjab', 'Chennai Super Kings', 'Mumbai Indians', 'Kolkata Knight Riders', 'Rajasthan Royals', 'Deccan Chargers', 'Kochi Tuskers Kerala','Pune Warriors','Sunrisers Hyderabad','Gujarat Lions','Delhi Daredevils','Rising Pune Supergiant','Delhi Capitals']
    team1 = st.selectbox('Select first Team from the list : ', (team_names_list), index = 2)
    team2 = st.selectbox('Select second team from the list : ', (team_names_list), index = 3)
    if st.button('Submit') and team1 != team2:
      matches_won_by_team1_team2(team1, team2)
    else:
      st.write('Please select two different teams')



elif radio == 'Player stats':
  _,col,_ = st.columns([1,2,1])
  with col:
    st.header('IPL Players Data' )


elif radio == 'Dream 11':
  _,col,_ = st.columns([1,2,1])
  with col:
    st.header('AI Based Recommended Dream11 Players')
