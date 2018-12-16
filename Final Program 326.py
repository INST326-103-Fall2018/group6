#!/Usr/bin/env python3
# _*_ coding:utf-8 _*_
import pandas as pd
import matplotlib.pyplot as plt  # added plotly function for bar graph
from matplotlib import style
import csv
import sys

global project_df
# Load the CSV file into a dataframe
#Saagar added sys.argv
inputfile = sys.argv[1]
project_df = pd.read_csv(inputfile, low_memory=False)

# tells number of rows and columns in the csv file dataframe.
print('There are', project_df.shape[0], 'Rows', '\nAnd', project_df.shape[1], 'Columns')

# setting the code indexed by state
firstAnalysis_df = project_df
secondConfigure_df = project_df

# extracts first 52 rows and first 12 columns to shorten the huge csv
# shows needed rows and columns but also saves the changes made as firstcode_df
firstAnalysis_df = firstAnalysis_df.iloc[:52, :12]

first_df = firstAnalysis_df  # set up temporary dataframe to avoid losing any progress here on out

first_df = first_df.drop(first_df.index[10])  # removes guam and puerto rico
first_df = first_df.drop(first_df.index[38])

firstAnalysis_df = first_df  # return to original data frame
firstAnalysis_df = firstAnalysis_df.sort_values(by='LocationDesc')

# sets LocationDesc, the state names, as index
firstAnalysis_df.set_index('LocationDesc', inplace=True)

states_list = firstAnalysis_df.index.values.tolist()  # creats a dictionary of all the states/abbr for later use of order
for v in states_list:
    print('{0}'.format(v))


# compares rates of alcohol use among youth in any two of the 50 states that the user chooses.
# This function was made by Emmanuel
def compare_any50():
    print(
        'Select two states to compare their rates at which alcohol is used among youth. Please use correct capitalization.')
    ## a test code can be written for user that input an invalid state.
    state_1 = input('Pick one state:')
    state_2 = input('Pick another state:')
    if state_1 in states_list and state_2 in states_list:  # added states_list in front of state_1
        value_1 = firstAnalysis_df.loc[state_1, 'DataValueAlt']
        value_2 = firstAnalysis_df.loc[state_2, 'DataValueAlt']

        print("Percent of alcohol use among youth in " + state_1 + ": " + str(value_1))
        print("Percent of alcohol use among youth in " + state_2 + ": " + str(value_2))

        if pd.isnull(value_1) and pd.isnull(value_2):
            print("Both states you have entered do not have a recorded percent frequency of alcohol use among youth.")
        elif pd.isnull(value_1):
            print("The first state you entered does not have a recorded percent frequency of alcohol use among youth.")
        elif pd.isnull(value_2):
            print("The second state you entered does not have a recorded percent frequency of alcohol use among youth.")
        else:
            if value_1 > value_2:
                print(state_1 + " has a greater percent frequency of alcohol use among youth than " + state_2)
            else:
                print(state_2 + " has a greater percent frequency of alcohol use among youth than " + state_1)

        ##Creating a bar graph to comapare the two different states
        ##comparing the rates of alcohol use among youths in two states
        x = value_1
        y = value_2
        plt.bar(x, label='Graph', color='red', height=x)
        plt.bar(y, color='blue', height=y)
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.title('Bar Graph on rates of alcohol use for\n' + state_1 + ' and ' + state_2)
        plt.show()
    else:
        print("Please input valid states in the U.S. with correct spelling and capitalization")
    print('\n')



secondcode_df = project_df.iloc[11670:12102]  # extracts asthma prevalence rows

secondcode_df = secondcode_df.sort_values('LocationDesc')  # alphabetized states

secondcode_df = secondcode_df.set_index('LocationDesc')  # indexed 'LocationDesc' instead of numerical row values
# drop unnecessary columns
secondcode_df = secondcode_df.drop(['DataValueTypeID', 'QuestionID', 'GeoLocation', 'ResponseID',
                                    'LocationID', 'StratificationCategory2', 'Stratification2',
                                    'StratificationCategory3',
                                    'Stratification3', 'DataSource', 'Response', 'TopicID', 'DataValueFootnoteSymbol',
                                    'LowConfidenceLimit', 'HighConfidenceLimit', 'DatavalueFootnote',
                                    'StratificationCategoryID2', 'StratificationID2', 'StratificationCategoryID3',
                                    'StratificationID3'], axis=1)

# remove rows that are not U.S. states
secondcode_df = secondcode_df.drop(['Virgin Islands', 'United States', 'Guam', 'Puerto Rico', 'District of Columbia'])

# brings up updated data frame
# created a new dataframe where overall asthma percents are displayed for each state
overallasthma_df = secondcode_df[secondcode_df.StratificationID1 == 'OVR']

# remove extra/multiple Ohio row
overallasthma_df = overallasthma_df[overallasthma_df.Topic == 'Asthma']


# this dataframe contains all female asthma prevalence values for each state
female_asthma_df = secondcode_df[secondcode_df.StratificationID1 == 'GENF']  # made the column change values to GENF

male_asthma_df = secondcode_df[secondcode_df.StratificationID1 == 'GENM']  # changed the column values to GENM



# this function allows the user to input up to 5 different states of their choosing and compare overall asthma rates of
# each state
# This function was made by Rohan
def compare_any50asthma():
    print("Compare up to five different states' overall asthma rates for 2015. If less than 5,\n"
          "type 'done' when you have entered all the states you wish to investigate. You must enter at least one state."
          )
    any_stateslist = []  # list for states that the user chooses, up to 5

    while len(any_stateslist) <= 4:
        any_state = input('Please enter a valid U.S. state. Use correct capitalization:')
        if any_state in states_list:
            any_stateslist.append(any_state)
        elif any_state == 'done':
            if len(any_stateslist) == 0:
                print("You have not entered any valid U.S. states.")
            else:
                break
        else:
            print('What you have entered is not a valid U.S. state. Please enter a valid U.S. state.')

    print(any_stateslist)
    print("Percent rates of asthma in chosen state(s):")
    for state in any_stateslist:
        print(state + ': ' + str(overallasthma_df.loc[state, 'DataValueAlt']))

    # make new dataframa to graph states chosen by user
    statedict = {}

    for state in any_stateslist:
        statedict[state] = overallasthma_df.loc[state, 'DataValueAlt']

    plt.bar(range(len(statedict)), list(statedict.values()), align='center')
    plt.xticks(range(len(statedict)), list(statedict.keys()))
    plt.show()
    print('\n')


# This code allows user to input one state and get the male, female, and overall asthma prevalence compared side by
# side in a graph
# This function was made by Michael 
def compare_genderasthma():

    print('Select one state in which you would like to see male, female, and overall percent prevalence of \n'
          'asthma among adults in 2015. Use correct capitalization. Note: There is no comparison data for'
          ' Alaska, Kansas, or Virginia.')
    one_state = []  # list for states that the user chooses

    while len(one_state) < 1:  # increment through a loop
        asthma_state = input('Please enter a valid U.S. state: ')

        if asthma_state in states_list:  # Get the index of each state
            if asthma_state == 'Kansas' or asthma_state == 'Alaska' or asthma_state == 'Virginia':
                print('There is no numerical data to compare for this state.')
            else:
                one_state.append(asthma_state)
                print('Overall percent prevalence of asthma in ' + asthma_state + ': ' + str(
                    overallasthma_df.loc[asthma_state, 'DataValueAlt']))
                print('Male percent prevalence of asthma in ' + asthma_state + ': ' + str(
                    male_asthma_df.loc[asthma_state, 'DataValueAlt']))
                print('Female percent prevalence of asthma in ' + asthma_state + ': ' + str(
                    female_asthma_df.loc[asthma_state, 'DataValueAlt']))
        else:
            print('What you have entered is not a valid state in the U.S. Please enter a valid state.')

    statedict = {'Female': female_asthma_df.loc[asthma_state, 'DataValueAlt'], 'Male': male_asthma_df.loc[asthma_state,
                                                                                                          'DataValueAlt'],
                 'Overall': overallasthma_df.loc[asthma_state, 'DataValueAlt']}

    plt.bar(range(len(statedict)), list(statedict.values()), align='center')  # Begin to use pandas for ploting graph
    plt.xticks(range(len(statedict)), list(statedict.keys()))
    plt.show()
    print('\n')



#Saagar Mehta wrote sys.argv functions
inputfiletwo = sys.argv[2]
project_df = pd.read_csv(inputfiletwo, low_memory=False)
#Ayomide Akinkuade
def Aqi():
    # importing AQI data per state capital - air quality Index(AQI)
    # Load the AQI CSV file into a dataframe
    Asthma_AQI_df = pd.read_csv(inputfiletwo, low_memory=True)
    # (Asthma_AQI dataframe contains the AQI (air quality index) of each state capital
    Asthma_AQI_df.columns = Asthma_AQI_df.columns.str.strip()
    # sorts dataframe by alphabetical order of states
    Asthma_AQI_df = Asthma_AQI_df.sort_values(by='State')

    # there is no Tennessee in overall asthma dataframe so we will remove it from AQI dataframe as well
    Asthma_AQI_df = Asthma_AQI_df.drop(Asthma_AQI_df.index[41])

    # sets index to states with object values. The two dataframes will not concatenate properly if the index is left as
    #numbers
    Asthma_AQI_df.set_index('State', inplace=True)

    # combines the overall asthma dataframe and the air quality index dataframe
    combined_asthmaAQI_df = pd.concat([overallasthma_df, Asthma_AQI_df], axis=1)

    # scatterplot comparing overall asthma percent rates to air quality indexes for each state, excluding Tennessee
    combined_asthmaAQI_df.plot.scatter(x='DataValueAlt', y='AQI by Capitol')
    plt.title('This Scatter shows the overall \n'
              'asthma percentage rates to air quality indexes for all the states')
    plt.show()


def main():
    compare_any50()
    compare_any50asthma()
    compare_genderasthma()
    Aqi()


if __name__ == '__main__':
    main()

