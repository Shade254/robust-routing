import pandas as pd
import utils as ut

#a function that reads a csv file from a given path and returns a pandas dataframe object
def read_csv(path):
    return pd.read_csv(path, sep=',')

#a function that prints the content of a specific column of a pandas dataframe object
def print_column(df, column_name):
    print(df[column_name])

#numbers of elements in a dataframe
def num_of_elements(df):
    return len(df)

#save dataframe to csv file
def save_csv(df, path):
    df.to_csv(path, index=False)

#df = read_csv("DynamicProgrammingStrategy_May_10_2022_18_03.csv")
df = read_csv("DynamicProgrammingStrategy_May_10_2022_19_16.csv")

output_columns = columns=['strategy','success_rate','increase_in_length','executed_increase_in_length','avg_planned_marking','avg_executed_marking']
df_output = pd.DataFrame(columns=output_columns)

grouped = df.groupby(df.Function)

for name, group in grouped:
    print(name)
    succes_rate = group['Success'].value_counts(normalize=True).mul(100).iloc[0].astype(str)+'%'
    increase_in_length = 0
    executed_increase_in_length = 0
    avg_planned_marking = 0
    avg_executed_marking = 0
    for index, row in group.iterrows():
        shortest_path_length = ut.get_manhattan_distance(row['Start'], row['End'])
        planned_path_length = ut.get_number_of_pairs(row['PlannedPath'])
        executed_path_length = ut.get_number_of_pairs(row['ExecutedPath'])
        increase_in_length += (planned_path_length - shortest_path_length)/shortest_path_length
        executed_increase_in_length += (executed_path_length - shortest_path_length)/shortest_path_length

        avg_planned_marking += ut.get_avg_marking(row['PlannedPathMarking'])
        avg_executed_marking += ut.get_avg_marking(row['ExecutedPathMarking'])

    increase_in_length = round(increase_in_length/num_of_elements(group),2)
    executed_increase_in_length = round(executed_increase_in_length/num_of_elements(group),2)
    avg_planned_marking = round(avg_planned_marking/num_of_elements(group),3)
    avg_executed_marking = round(avg_executed_marking/num_of_elements(group),3)

    df_output.loc[len(df_output), df_output.columns] = [name, succes_rate, ut.get_percentage(increase_in_length), ut.get_percentage(executed_increase_in_length), avg_planned_marking, avg_executed_marking]

save_csv(df_output, "output.csv")
print(df_output)
       

#loop through the dataframe and print the values of the column 'Success'


#Do below for each strategy


#Calculate succes rate 
#Calculate planned distance from shortest path as percent
#Calculate executed distance from shortest path as percent
#Min planned marking
#Max planned marking
#Avg planned marking
#Min Executed marking
#Max Executed marking
#Avg Exectude marking

#Average out over all strategies