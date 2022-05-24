import pandas as pd

import utils as ut


# a function that reads a csv file from a given path and returns a pandas dataframe object
def read_csv(path):
    return pd.read_csv(path, sep=',')


# a function that prints the content of a specific column of a pandas dataframe object
def print_column(df, column_name):
    print(df[column_name])


# numbers of elements in a dataframe
def num_of_elements(df):
    return len(df)


# save dataframe to csv file
def save_csv(df, path):
    df.to_csv(path, index=False)


# Get a row from a dataframe based on name and index
def get_row(df_dict, name, index):
    return df_dict[name].iloc[index]


def get_first_row_of_df(df):
    return df.iloc[0]


def group_df_by_column(df, column_names, reset_index=True, drop_column=True):
    grouped = df.groupby(column_names)
    groups_dict = {}
    for name, group in grouped:
        if reset_index:
            group.reset_index(inplace=True, drop=True)
        if drop_column:
            group.drop(column_names, axis=1, inplace=True)
        groups_dict[name] = group

    return groups_dict


def get_planned_path_of_strategy(df_dict, graph, function, disturbanceplayer, start, end):
    df = df_dict[(function, disturbanceplayer)]
    df_result = df.loc[
        (df['Graph'] == graph) & (df['Start'] == start) & (df['End'] == end)]
    return get_first_row_of_df(df_result)


def get_path_avg_planned_robustness(df_row):
    return ut.get_avg_marking(df_row['PlannedPathMarking'])


def get_path_avg_executed_robustness(df_row):
    return ut.get_avg_marking(df_row['ExecutedPathMarking'])


def get_path_planned_length(df_row):
    return ut.get_number_of_pairs(df_row['PlannedPath'])


def get_path_executed_length(df_row):
    return ut.get_number_of_pairs(df_row['ExecutedPathMarking'])


class Path_Data:
    def __init__(self, df_row):
        self.path_length = get_path_planned_length(df_row)
        self.executed_length = get_path_executed_length(df_row)
        self.avg_planned_robustness = get_path_avg_planned_robustness(df_row)
        self.avg_executed_robustness = get_path_avg_executed_robustness(df_row)
        self.success = df_row['Success']


def process_test_results(input_file_path, output_file_path):
    df = read_csv(input_file_path)

    output_columns = columns = ['Strategy',
                                'Disturbance player',
                                'Success rate',
                                'Average planned path length',
                                'Average executed successful path length',
                                'Average executed unsuccessful path length',
                                'Planned distance increase from shortest path',
                                'Executed distance increase from shortest paths execution',
                                'Executed distance increase from planned distance',
                                'Average planned robustness',
                                'Average robustness of succesfull executions',
                                'Avg planned robustness as increase to shortest path',
                                'Avg executed robustness as increase to planned path',
                                'Average planned robustness of survived executions',
                                'Average planned robustness of fatal executions',
                                'Executions where executed and shortest path were both succesfull'
                                ]

    df_output = pd.DataFrame(columns=output_columns)

    grouped_df_dict = group_df_by_column(df, ['Function', 'DisturbancePlayer'])

    for key, group in grouped_df_dict.items():
        strategy = key[0]
        disturbance_player = key[1]
        print(f'{strategy} - {disturbance_player}')

        increase_in_planned_distance_to_shortest = 0
        executed_inc_in_distance_to_shortest_executed = 0
        executed_inc_in_distance_to_planned_distance = 0
        avg_planned_robustness_abs = 0
        avg_executed_robustness_abs = 0
        avg_planned_robustness_inc_to_shortest = 0
        avg_executed_marking_inc_to_planned = 0
        planned_robustness_of_suvivors = 0
        planned_robustness_of_unsuvivors = 0

        average_planned_path_length = 0
        average_executed_successful_path_length = 0
        average_executed_unsuccessful_path_length = 0

        num_of_succesfull_runs = 0
        num_of_both_path_succesful = 0
        num_of_unsuccesfull_runs = 0

        for index, evaluated_path_row in group.iterrows():
            # Get data of the shortest path
            shortest_path_row = get_planned_path_of_strategy(grouped_df_dict,
                                                             evaluated_path_row['Graph'],
                                                             'ShortestPath',
                                                             disturbance_player,
                                                             evaluated_path_row['Start'],
                                                             evaluated_path_row['End'])
            ShortestPath = Path_Data(shortest_path_row)

            # Get data of the path that was executed
            EvaluatedPath = Path_Data(evaluated_path_row)

            increase_in_planned_distance_to_shortest += (
                                                                EvaluatedPath.path_length - ShortestPath.path_length) / ShortestPath.path_length
            average_planned_path_length += EvaluatedPath.path_length

            avg_planned_robustness_abs += EvaluatedPath.avg_planned_robustness
            avg_planned_robustness_inc_to_shortest += EvaluatedPath.avg_planned_robustness - ShortestPath.avg_planned_robustness

            # Below is only calculated based on succesfull runs
            if evaluated_path_row['Success'] == True:
                num_of_succesfull_runs += 1

                average_executed_successful_path_length += EvaluatedPath.executed_length

                if ShortestPath.success:
                    num_of_both_path_succesful += 1
                    executed_inc_in_distance_to_shortest_executed += (
                                                                             EvaluatedPath.executed_length - ShortestPath.executed_length) / ShortestPath.executed_length

                executed_inc_in_distance_to_planned_distance += (
                                                                        EvaluatedPath.executed_length - EvaluatedPath.path_length) / EvaluatedPath.path_length

                planned_robustness_of_suvivors += EvaluatedPath.avg_planned_robustness
                avg_executed_robustness_abs += EvaluatedPath.avg_executed_robustness
                avg_executed_marking_inc_to_planned += EvaluatedPath.avg_executed_robustness - EvaluatedPath.avg_planned_robustness

            else:
                average_executed_unsuccessful_path_length += EvaluatedPath.executed_length

                num_of_unsuccesfull_runs += 1
                planned_robustness_of_unsuvivors += EvaluatedPath.avg_planned_robustness

        succes_rate = ut.to_percentage(num_of_succesfull_runs / num_of_elements(group), 2)

        average_planned_path_length = round(
            average_planned_path_length / num_of_elements(group), 2)
        average_executed_successful_path_length = round(
            average_executed_successful_path_length / num_of_succesfull_runs, 2)
        average_executed_unsuccessful_path_length = round(
            average_executed_unsuccessful_path_length / num_of_unsuccesfull_runs, 2)

        increase_in_length_str = ut.to_percentage(
            increase_in_planned_distance_to_shortest / num_of_elements(group), 2)
        if num_of_both_path_succesful > 0:
            executed_increase_in_length_str = ut.to_percentage(
                executed_inc_in_distance_to_shortest_executed / num_of_both_path_succesful,
                2)
        else:
            executed_increase_in_length_str = 0
        executed_inc_in_distance_to_planned_distance_str = ut.to_percentage(
            executed_inc_in_distance_to_planned_distance / num_of_succesfull_runs, 2)

        avg_planned_robustness_abs = round(
            avg_planned_robustness_abs / num_of_elements(group), 3)
        avg_executed_robustness_abs = round(
            avg_executed_robustness_abs / num_of_succesfull_runs, 3)

        avg_planned_robustness_inc_to_shortest = round(
            avg_planned_robustness_inc_to_shortest / num_of_elements(group), 3)
        avg_executed_marking_inc_to_planned = round(
            avg_executed_marking_inc_to_planned / num_of_succesfull_runs, 3)

        planned_robustness_of_suvivors = round(
            planned_robustness_of_suvivors / num_of_succesfull_runs, 3)
        planned_robustness_of_unsuvivors = round(
            planned_robustness_of_unsuvivors / num_of_unsuccesfull_runs, 3)

        df_output.loc[len(df_output), df_output.columns] = [
            strategy,
            disturbance_player,
            succes_rate,
            average_planned_path_length,
            average_executed_successful_path_length,
            average_executed_unsuccessful_path_length,
            increase_in_length_str,
            executed_increase_in_length_str,
            executed_inc_in_distance_to_planned_distance_str,
            avg_planned_robustness_abs,
            avg_executed_robustness_abs,
            avg_planned_robustness_inc_to_shortest,
            avg_executed_marking_inc_to_planned,
            planned_robustness_of_suvivors,
            planned_robustness_of_unsuvivors,
            num_of_both_path_succesful]

    save_csv(df_output, output_file_path)
    print(df_output)


import os

graph_paths = []
graph_paths = [os.path.join('test_raw_results', x) for x in
               os.listdir('test_raw_results')]
for path in graph_paths:
    test = path.split('\\')[1]
    process_test_results(path, f'test_processed_results\{test}')
# path = 'other_test_results\cutoff_50.csv'
# process_test_results(path,f'test_processed_results\cutoff_50.csv')
