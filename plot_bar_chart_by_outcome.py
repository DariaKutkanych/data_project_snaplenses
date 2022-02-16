import pandas as pd
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from plotly.offline import iplot

def plot_bar_chart_by_outcome(var_name, df, outcome='top'):
    """
    Function plots the bar plot of the ratio of variable grouped by the outcome."""
    # get the size of each combination of var_name and outcome
    temp_df = pd.DataFrame(df.groupby([outcome, var_name]).size())
    temp_df = temp_df.reset_index(drop=False)
    temp_df.rename(columns={0: 'count'}, inplace=True)

    # get the total amount of var_name observations
    total_count_df = temp_df.groupby(var_name, as_index=False)[['count']].sum()
    total_count_df.rename(columns={'count': 'total_count'}, inplace=True)

    # combine two tables together
    temp_df = temp_df.merge(
        total_count_df,
        how='left')

    # calculate the ratio
    temp_df['ratio'] = (temp_df['count'] / temp_df['total_count']).apply(lambda x: round(x, 3))

    # create a plot
    trace1 = go.Bar(
        x=temp_df['ratio'][temp_df[outcome] == 0],
        y=temp_df[var_name][temp_df[outcome] == 0],
        text=temp_df['count'][temp_df[outcome] == 0].apply(lambda x: str(x) + ' observations'),
        name='Unsuccessful',
        orientation='h',
        marker=dict(color='rgba(255, 80, 80, 0.8)'),
        legendgroup='Unsuccessful'
    )

    trace2 = go.Bar(
        x=temp_df['ratio'][temp_df[outcome] == 1],
        y=temp_df[var_name][temp_df[outcome] == 1],
        text=temp_df['count'][temp_df[outcome] == 1].apply(lambda x: str(x) + ' observations'),
        name='Successful',
        orientation='h',
        marker=dict(color='rgba(153, 255, 102, 0.8)'),
        legendgroup='Successful'
    )

    layout = go.Layout(
        height=400,
        width=800,
        barmode='stack',
        title=f'Ratio of {var_name} by {outcome}',
        xaxis={'title': 'Ratio'},
        yaxis={'title': var_name}
    )

    data = [trace1, trace2]
    fig = go.Figure(data, layout)
    iplot(fig)
