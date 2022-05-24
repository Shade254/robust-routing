from calendar import c
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick

#A function that converts a string with a percentage value to a float
def convert_percentage_to_float(percentage):
    return float(percentage[:-1])

def is_value_str(value):
    return isinstance(value, str)

#A function that returns true if values in a dataframe column has a percentage sign
def column_is_percentage_column(column):
    for value in column:
        if is_value_str(value) and '%' in value:
            return True
    return False

columns = ['Strategy',
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
            
column = 'Executed distance increase from shortest paths execution'
graph = '50_1_1'


df = pd.read_csv(f'test_processed_results\dynamic_{graph}.csv')

df.drop(df.index[df['Strategy'] == 'ShortestPath'], inplace=True)

df2 = pd.read_csv(f'test_processed_results\\routing_{graph}.csv')

df = df.append(df2,ignore_index=True)


if(column_is_percentage_column(df[column])):
    df[column] = df[column].apply(convert_percentage_to_float)



colors = [
    'red', #'ShortestPath'      ,
    'orange', #'SafestPathV1'      ,
    'yellow', #'SafestPathV2'      ,
    'green', #'VectorSafePath'    ,
    'cyan', #'VectorSafePathCut7',
    'white', #'1/x'               ,
    'grey', #'sinus'             ,
    'black' #'7-x'               
]

column_order = [
    'ShortestPath'      ,
    'SafestPathV1'      ,
    'SafestPathV2'      ,
    'VectorSafePath'    ,
    'VectorSafePathCut7',
    '1/x'               ,
    'sinus'             ,
    '7-x'               
]

# ax = sns.barplot(x = 'Strategy',
#             y = column,
#             order=column_order,
#             data = df,
#             #kind = 'bar',
#             palette = sns.color_palette(colors),
#             edgecolor='black'
#             )

ax = sns.catplot(x = 'Disturbance player',
            y = column,
            hue = 'Strategy',
            hue_order=column_order,
            data = df,
            kind = 'bar',
            palette = sns.color_palette(colors),
            edgecolor='black'
            )

y_tickers = ['0%','20%', '40%', '60%', '80%', '100%', '120%']#'140%','160%']
ax.set_yticklabels(y_tickers)
ax.set_ylabels(column)

#ax.set(ylim=(0, 9))

x_tickers = ['Malicous', 'Periodic', '0.2', '0.5']
ax.set_xlabels('Disturbance player')
ax.set_xticklabels(x_tickers)

plt.show();