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

#Get a row from a dataframe based on name and index
def get_row(df_dict, name, index):
    return df_dict[name].iloc[index]


def group_df_by_column(df, column_name, reset_index=True, drop_column=True):
    grouped = df.groupby([column_name])
    groups_dict = {}
    for name, group in grouped:
        if reset_index:
            group.reset_index(inplace=True, drop=True)
        if drop_column:
            group.drop([column_name], axis=1, inplace=True)
        groups_dict[name] = group

    return groups_dict
    
output_columns = columns=['strategy','success_rate','increase_in_planned_distance','increase_in_distance_with_wind','planned_robustness_increase','robustness_increase_with_wind']
df_output = pd.DataFrame(columns=output_columns)

#df = read_csv("DynamicProgrammingStrategy_May_10_2022_18_03.csv")
df = read_csv("strategies_results.csv")

grouped_df_dict = group_df_by_column(df,'Function')
print(get_row(grouped_df_dict, 'ShortestLength', 1))

for name, group in grouped_df_dict.items():
    print(name)
    print(group)
    succes_rate = group['Success'].value_counts(normalize=True).mul(100).iloc[0].astype(str)+'%'
    increase_in_length = 0
    executed_increase_in_length = 0
    avg_planned_marking = 0
    avg_executed_marking = 0
    num_of_succesfull_runs = 0
    for index, row in group.iterrows():
        if row['Success'] == True:
            num_of_succesfull_runs += 1
        else :
            continue
        shortest_path_data = get_row(grouped_df_dict, 'ShortestLength', index)
        
        shortest_path_length = ut.get_number_of_pairs(shortest_path_data['PlannedPath'])
        planned_path_length = ut.get_number_of_pairs(row['PlannedPath'])
        executed_path_length = ut.get_number_of_pairs(row['ExecutedPath'])
        increase_in_length += (planned_path_length - shortest_path_length)/shortest_path_length
        executed_increase_in_length += (executed_path_length - shortest_path_length)/shortest_path_length

        shortest_path_marking = ut.get_avg_marking(shortest_path_data['PlannedPathMarking'])
        avg_planned_marking += ut.get_avg_marking(row['PlannedPathMarking'])-shortest_path_marking
        avg_executed_marking += ut.get_avg_marking(row['ExecutedPathMarking'])-shortest_path_marking

    increase_in_length = round(increase_in_length/num_of_succesfull_runs,2)
    executed_increase_in_length = round(executed_increase_in_length/num_of_succesfull_runs,2)
    avg_planned_marking = round(avg_planned_marking/num_of_succesfull_runs,3)
    avg_executed_marking = round(avg_executed_marking/num_of_succesfull_runs, 3)

    df_output.loc[len(df_output), df_output.columns] = [name, succes_rate, ut.get_percentage(increase_in_length), ut.get_percentage(executed_increase_in_length), avg_planned_marking, avg_executed_marking]

save_csv(df_output, "output2.csv")
print(df_output)