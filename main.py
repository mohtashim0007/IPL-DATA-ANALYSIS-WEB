

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
  plt.savefig('./fig1.jpg')
  img = cv2.imread('./fig1.jpg')
  img = cv2.resize(img, (880,824))
  _,col,_ = st.columns([1,4,1])
  with col:
    st.image(img)
  

#MATCHES WON BY RUNS/WICKETS
def matches_won_by_runs_wickets(team_name):
  temp5 = df_matches[df_matches['team1'] == team_name]
  temp5 = temp5[temp5['winner'] == temp5['team1']]
  temp6 = df_matches[df_matches['team2'] == team_name]
  temp6 = temp6[temp6['winner'] == temp6['team2']]

  temp7 = pd.concat([temp5, temp6],ignore_index = True)
  
  sns.countplot(x ='result', data = temp7, dodge=False, palette = np.random.choice(fig_colors)) 
  plt.title('Bar graph depicts no. of matches won by runs/wickets')
  plt.xlabel('Runs/Wickets')
  plt.ylabel('Matches Won ')
  plt.xticks([0,1,2],['Runs', 'Wickets', 'Tie'], rotation = 45)
  plt.savefig('./fig2.jpg')
  img2 = cv2.imread('./fig2.jpg')
  img2 = cv2.resize(img2, (880,524))
  st.image(img2)





radio = st.sidebar.radio('Main Menu :', ('Match Stats', 'Player stats', 'Dream 11'))

#MATCH STATS RADIO BUTTON
if radio == 'Match Stats':
  _,col,_ = st.columns([1,2,1])
  with col:
    st.header('IPL Team Wise Data' )
  st.text('')
  
  team_names_list =['Royal Challengers Bangalore', 'Kings XI Punjab', 'Chennai Super Kings', 'Mumbai Indians', 'Kolkata Knight Riders', 'Rajasthan Royals', 'Deccan Chargers', 'Kochi Tuskers Kerala','Pune Warriors','Sunrisers Hyderabad','Gujarat Lions','Delhi Daredevils','Rising Pune Supergiant','Delhi Capitals']

  #COMAPRISION OF TEAMS CHECKBOX
  if st.checkbox('Comparision of two IPL Teams'):
    team1 = st.selectbox('Select first Team from the list : ', (team_names_list), index = 2)
    team2 = st.selectbox('Select second team from the list : ', (team_names_list), index = 3)
    if st.button('Submit',key= '1') and team1 != team2:
      matches_won_by_team1_team2(team1, team2)

  
  #nUMBER OF MATCHES WON BY EACH TEAM
  st.text(' ')
  if st.checkbox('Number of Matches won by each Team :'):
    st.write('Bar chart showing mathes won by the teams :')
    img = cv2.imread('./matches_won_by_each_team_barplot.jpg')
    st.image(img)
    st.text(' ')
    st.write('Pie Chart showing percentage os matches won by each team :')
    img = cv2.imread('./matches_won_by_each_team_pieChart.jpg')
    st.image(img)


  #Matches won by runs/wicets
  st.text(' ') 
  if st.checkbox('Matches won by Runs/Wickets or Tie :'):
    
    radio_button = st.radio('Click on the radio button :', (['Graph for each teams','Team wise Graph']))
    
    if radio_button == 'Graph for each teams':      
      fig = plt.figure(figsize = (18,8))
      sns.countplot(x='winner', hue='result', data = df_matches, palette=np.random.choice(fig_colors))
      plt.xticks(rotation = 45)
      plt.savefig('fig1.jpg')
      img = cv2.imread('fig1.jpg')
      st.image(img)
      st.text(' ')
      
    elif radio_button == 'Team wise Graph':      
      st.write('View Team wise :')
      team = st.selectbox('',team_names_list, index = 3)
      #if st.button('Submit',key = '2'):
      matches_won_by_runs_wickets(team)
   
  #IPL Umpires
  if st.checkbox('IPL Umpires'):
    st.write('Graph shows umpires with the number of matches they umpired.')
    img = cv2.imread('./Umpire_fig.jpg')
    st.image(img)
    
  #Man of the matches
  st.text(' ')
  if st.checkbox('Man of the Matches Awards'):
    MoM = df_matches['player_of_match'].value_counts()
    st.table(MoM[0:5])
    st.text('')
    fig = plt.figure()
    sns.barplot(MoM[0:5].index.tolist(), MoM[0:5].tolist(),palette = np.random.choice(fig_colors))
    plt.ylabel('No of times Player of the Match Won')
    plt.xlabel('Player Names')
    plt.title('Top 5 Players who won Man of the Match')
    plt.ylim(0,25)
    plt.savefig('fig1.jpg')
    img = cv2.imread('fig1.jpg')
    st.image(img)
    
    player = st.selectbox('Select your favourite player to check his Man of the Matches :', (MoM.index), index = 2)
    st.write('Man of the Matches for ',player,' is ',MoM[player]) 
    
    
    



#PLAYER STATS MENU RADIO BUTTON
elif radio == 'Player stats':
  _,col,_ = st.columns([1,2,1])
  with col:
    st.header('IPL Players Data' )



#DREAM 11 TEAM SGGESTIONS RADIO BUTTON
elif radio == 'Dream 11':
  _,col,_ = st.columns([1,2,1])
  with col:
    st.header('AI Based Recommended Dream11 Players')
