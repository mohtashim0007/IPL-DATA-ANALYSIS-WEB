
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import cv2
import streamlit as st

fig_colors = ['Set1', 'Set2', 'Set3', 'tab10' ,'deep', 'hls', 'husl', 'rocket_r', 'YlOrBr', 'Spectral']

df_matches = pd.read_csv('IPL Matches 2008-2020.csv')
df_ball = pd.read_csv('./IPL Ball-by-Ball 2008-2020.csv')

#batsman stats aganst a particular bowler

def batsman_against_bowler(batsman_name, bowler_name):
  temp15 = df_ball[ df_ball['bowler'] == bowler_name ]
  temp15 =  temp15[temp15['batsman'] == batsman_name ]
  total_balls_faced = temp15.shape[0]
  if total_balls_faced == 0:
    return []

  four_six = temp15['batsman_runs'].value_counts()
  sixs = 0
  fours = 0
  runs_index = four_six.index.tolist()
  if 4 in runs_index:
    fours = four_six[4]
  if 6 in runs_index:
    sixs = four_six[6]
  total_runs = temp15['total_runs'].sum()
  is_wicket = temp15['is_wicket'].sum()
  total_matches_played = temp15['id'].nunique()
  total_balls_faced = temp15.shape[0]
  avg_per_over = round((total_runs/total_balls_faced)*6,2)

  return [total_matches_played, total_runs,is_wicket, total_balls_faced,fours,sixs]


#function to collect team1 batting stats against team2 bowlers
def team_batting_stats(team1,team2):
  player_stats_list = []

  for batsman in team1:
    batsman_stats = []
    for bowler in team2:
      #result is in the form of   return [total_matches_played, total_runs,is_wicket, total_balls_faced,fours,sixs]
      result = batsman_against_bowler(batsman, bowler)
      if len(result)>0:
        if len(batsman_stats)>0:
          batsman_stats = list(np.add(batsman_stats,result))
        else:
          batsman_stats = result

    #run_rate = round((total_runs/total_balls_faced)*6,2)
    if len(batsman_stats) > 0:
      run_rate =   round((batsman_stats[1]/batsman_stats[3])*6,2)
      strike_rate = round((batsman_stats[1]/batsman_stats[3])*100,2)

      player_stats_list.append([batsman] + batsman_stats + [ run_rate, strike_rate])

  return player_stats_list


#function to collect bowlers stats against team 2
def team_bowling_stats(team1,team2):
  player_stats_list = []

  for bowler in team1:
    bowler_stats = []
    for batsman in team2:
      result = batsman_against_bowler(batsman, bowler)
      #result format   return [total_matches_played, total_runs,is_wicket, total_balls_faced,fours,sixs]
      if len(result)>0:
        if len(bowler_stats)>0:
          bowler_statss = list(np.add(bowler_stats,result))
        else:
          bowler_stats = result

    if len(bowler_stats) > 0:
      economy =   round((bowler_stats[1]/bowler_stats[3])*6,2)
      player_stats_list.append([bowler] + bowler_stats + [ economy])

  return player_stats_list



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


#IPL TEAM NAMES
MI = ['KH Pandya','Q de Kock','RG Sharma','SA Yadav','Ishan Kishan','HH Pandya','KA Pollard','NM Coulter-Nile','RD Chahar','JJ Bumrah','TA Boult']
SRH = ['DA Warner','JM Bairstow','MK Pandey','Abdul Samad','KS Williamson','PK Garg','Abhishek Sharma','Sandeep Sharma','KK Ahmed','T Natarajan','Rashid Khan']
CSK = ['F du Plessis','AT Rayudu','SM Curran','DL Chahar','RD Gaikwad','MS Dhoni','SN Thakur','Imran Tahir','N Jagadeesan','RA Jadeja','JR Hazlewood']
KXIPB = ['KL Rahul','CH Gayle','N Pooran','Mandeep Singh','DJ Hooda','JDS Neesham','CJ Jordan','MA Agarwal','Mohammed Shami','Ravi Bishnoi','M Ashwin']
KKR = ['EJG Morgan', 'AD Russell', 'PJ Cummins', 'RA Tripathi', 'KD Karthik', 'KL Nagarkoti', 'Shubman Gill', 'N Rana','SP Narine','Shivam Mavi','CV Varun']
RR = ['RV Uthappa','BA Stokes','SV Samson','JC Buttler','SPD Smith','R Tewatia', 'JC Archer', 'Kartik Tyagi', 'S Gopal','JD Unadkat']
DC = ['SS Iyer','RR Pant','SO Hetmyer', 'AR Patel', 'MP Stoinis', 'AM Rahane', 'S Dhawan','R Ashwin', 'K Rabada','A Nortje','P Dubey']
RCB = ['V Kohli','D Padikkal','AJ Finch', 'AB de Villiers', 'MM Ali', 'S Dube', 'Washington Sundar','NA Saini','Mohammed Siraj','A Zampa','YS Chahal']

def IPL_Teams_name(team):
  if team == 'MI':
    team = MI
  elif team == 'SRH':
    team = SRH
  elif team == 'CSK':
    team = CSK  
  elif team == 'KXIPB':
    team = KXIPB
  elif team == 'KKR':
    team = KKR
  elif team == 'RR':
    team = RR
  elif team == 'DC':
    team = DC
  elif team == 'RCB':
    team = RCB
  return team


# WEB APP CODING

radio = st.sidebar.radio('Main Menu :', ('Dream 11', 'Match Stats', 'Player stats' ))


#DREAM 11 TEAM SGGESTIONS RADIO BUTTON
if radio == 'Dream 11':
  _,col,_ = st.columns([1,2,1])
  with col:
    st.header('AI Based Recommended Dream11 Players')

  # playing 11 teams

  if st.checkbox('View IPL Teams Playing 11  '):
    team = st.selectbox('Select IPL Team to view Playing 11 :', (['MI','SRH','CSK','KXIPB','KKR','RR','DC','RCB']), index=0)
    #team getting string values so map this to the list
    team = IPL_Teams_name(team)
    st.table(team)
  

  if st.checkbox('Team A vs Team B '):
    team1 = st.selectbox('Select Team A :', (['MI','SRH','CSK','KXIPB','KKR','RR','DC','RCB']), index = 2)
    #team1_str hold string value of teams eg 'MI'
    team1_str = team1
    team1 = IPL_Teams_name(team1)
    team2 = st.selectbox('Select Team B :', (['MI','SRH','CSK','KXIPB','KKR','RR','DC','RCB']), index = 0)
    team2_str = team2
    team2 = IPL_Teams_name(team2)

    team1_batting_stats = pd.DataFrame(data = team_batting_stats(team1, team2), columns = ['Name', 'Matches', 'Runs','Out','Balls Played','fours','sixs' ,'Run Rate', 'Strike Rate'])
    team1_bowling_stats = pd.DataFrame(data = team_bowling_stats(team1, team2), columns = ['Name', 'Matches', 'Runs','wickets','Balls','fours','sixs' ,'Economy'])

    
    st.write(team1_str, ' Batsman Data against ', team2_str, ' Bowlers : ')
    st.table(team1_batting_stats)
    st.text(' ')
    st.write(team1_str , ' Bowlers Data against ', team2_str, ' Batsman : ')
    st.table(team1_bowling_stats)
    st.text(' ')

    team2_batting_stats = pd.DataFrame(data = team_batting_stats(team2, team1),columns = ['Name', 'Matches', 'Runs','Out','Balls Played' ,'fours','sixs','Run Rate', 'Strike Rate'] )
    team2_bowling_stats = pd.DataFrame(data = team_bowling_stats(team2, team1),columns = ['Name', 'Matches', 'Runs','wickets','Balls' ,'fours','sixs','Economy' ])

    st.write(team2_str, ' Batsman Data against ', team1_str, ' Bowlers : ')
    st.table(team2_batting_stats)
    st.text(' ')
    st.write(team2_str , ' Bowlers Data against ', team1_str, ' Batsman : ')
    st.table(team2_bowling_stats)
    st.text(' ')

  if st.checkbox('Batsman Data against a Bowler :'):
    batsman = st.selectbox('Select the batsman name : ', (df_ball['batsman'].unique().tolist()), index = 15)
    bowler = st.selectbox('Select the bowler name : ', (df_ball['bowler'].unique().tolist()), index = 15)
    #return [total_matches_played, total_runs,is_wicket, total_balls_faced,fours,sixs]
    result = batsman_against_bowler(batsman, bowler)
    if (len(result) > 1):
      st.write('Total matches played = ', result[0])
      st.write('Runs Scored = ', result[1])
      st.write('Nuber of times Out = ', result[2])
      st.write('Total balls faced = ', result[3])
      st.write('Fours = ', result[4])
      st.write('Sixes = ', result[5])
    else:
      st.write('They both did not faced each other.')



#MATCH STATS RADIO BUTTON
elif radio == 'Match Stats':
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
  if st.checkbox('Number of Matches won by each Team '):
    st.write('Bar chart showing mathes won by the teams :')
    img = cv2.imread('./matches_won_by_each_team_barplot.jpg')
    st.image(img)
    st.text(' ')
    st.write('Pie Chart showing percentage os matches won by each team :')
    img = cv2.imread('./matches_won_by_each_team_pieChart.jpg')
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


  #Matches won by runs/wicets
  st.text(' ') 
  if st.checkbox('Matches won by Runs/Wickets or Tie '):
    
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

  #Matches won by chasing 
  st.text(' ')
  if st.checkbox('Matches won by chasing '):
    st.write('Total matches played by fielding first : 496')
    st.write('Matches won  by chasing : 273')
    st.write('Matches lost by chasing : 223')
    st.write('Percentage of winning by chasing :  55.04 %')
    img = cv2.imread('./won_by_chasing.jpg')
    st.image(img)

  #IPL Umpires
  st.text('')
  if st.checkbox('IPL Umpires'):
    st.write('Graph shows umpires with the number of matches they umpired.')
    img = cv2.imread('./Umpire_fig.jpg')
    st.image(img)  



#PLAYER STATS MENU RADIO BUTTON
elif radio == 'Player stats':
  _,col,_ = st.columns([1,2,1])
  with col:
    st.header('IPL Players Data' )


  #Radio 2 on PLAYERS STATS
  radio_2 = st.radio('Select from the below tabs : ', ['Click for Batsman Data', 'Click for Bowler Data'])

  #Radio 2 Click for BATSMAN DATA
  if radio_2 == 'Click for Batsman Data':

    players_stats_df = pickle.load(open('./players_stats_df.pkl', 'rb'))

    #View you favourite batsman runs
    if st.checkbox('View you favourite batsman runs '):
      player_name = st.selectbox('Select player from the list : ',players_stats_df['name'],index = 5 )
      temp13 = players_stats_df[players_stats_df['name'] == player_name]
      st.text('Below is data for  your favourite player :')
      st.table(temp13)

    #top 10 scorer
    if st.checkbox('Top 10 batsman with highest runs '):
      temp = players_stats_df.sort_values(by= ['total_runs'], ascending = False)[0:10]
      st.table(temp)

    #TOP 10 sort playera by strike rate
    if st.checkbox('Players sorted by strike rate '):
      temp11 = players_stats_df[players_stats_df['matches_played'] > 150 ]
      temp11 = temp11.sort_values(by= ['strike_rate'], ascending = False)[0:10]
      st.table(temp11)

    #Top  10 BEST AVERAGE SCORE
    if st.checkbox('Top 10 batsman with best average score'):
      temp12 = players_stats_df.sort_values(by= ['average_score'], ascending = False)[0:10]
      st.table(temp12)

    #TOP 10 BATSMAN WITH HIGHEST SIXES
    if st.checkbox('Top 10 batsman with highest sixes '):
      temp13 = players_stats_df.sort_values(by= ['sixs'], ascending = False)[0:10]
      temp13 = temp13.loc[:, ['name', 'sixs']]
      st.table(temp13)

    #TOP 10 BATSMAN WITH HIGHEST fours
    if st.checkbox('Top 10 batsman with highest fours '):
      temp14 = players_stats_df.sort_values(by= ['fours'], ascending = False)[0:10]
      temp14 = temp14.loc[:, ['name', 'fours']]
      st.table(temp14)  

  
  elif radio_2 == 'Click for Bowler Data':
    st.text('Bowler data')

  


