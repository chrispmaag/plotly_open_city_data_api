import pandas as pd
import plotly.graph_objs as go
import requests

# Use this file to read in your data and prepare the plotly visualizations.

# Save data to a dataframe
def open_data_to_df(url, params=None):
    """ Input url and convert to Pandas dataframe"""
    request_object = requests.get(url, params)
    request_object_json = request_object.json()
    return pd.DataFrame([entry for entry in request_object_json])

# Data for plot 1
wages_url = 'https://data.seattle.gov/resource/ssah-h43e.json?$select=department, hourly_rate limit 50000'
seattle_wages = open_data_to_df(wages_url)

# Convert hourly_rate column from string to float
seattle_wages['hourly_rate'] = pd.to_numeric(seattle_wages['hourly_rate'])
median_wages = seattle_wages.groupby('department').median().sort_values('hourly_rate').reset_index()
top_median_wages = median_wages[24:]

# Data for plot 2
crime_url = 'https://data.seattle.gov/resource/xurz-654a.json?$where=reported_date >= "2018-01-01" \
             order by reported_date limit 50000'
seattle_crime = open_data_to_df(crime_url)
seattle_crime['reported_date'] = pd.to_datetime(seattle_crime['reported_date'])
crime = seattle_crime[['crime_description', 'precinct']].groupby('crime_description').count().reset_index()\
        .sort_values('precinct', ascending=False)[:10]
crime.columns = ['crime_description', 'count']

# Data for plot 3
budget_url = 'https://data.seattle.gov/resource/4fzy-5niz.json?fiscal_year=2018'
seattle_budget = open_data_to_df(budget_url)
seattle_budget['approved_amount'] = pd.to_numeric(seattle_budget['approved_amount'])
seattle_budget_top_10 = seattle_budget[['department', 'approved_amount']].groupby('department').sum() \
                .reset_index().sort_values('approved_amount', ascending=False)[:10]

# Data for plot 4
yearly_budget_url = 'https://data.seattle.gov/resource/4fzy-5niz.json?$select=fiscal_year, \
                   sum(approved_amount) as approved_amount\
                   where fiscal_year between 2010 and 2018 \
                   group by fiscal_year \
                   order by fiscal_year'
yearly_budget = open_data_to_df(yearly_budget_url)

# Convert approved_amount from string to numeric
yearly_budget['approved_amount'] = pd.to_numeric(yearly_budget['approved_amount'])

###########################################################################

def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """

    # First plot on Top 10 Median Hourly Wages by Department
    
    graph_one = []    
    graph_one.append(
      go.Bar(
      x = top_median_wages['hourly_rate'].tolist(),
      y = top_median_wages['department'].tolist(),
      orientation = 'h'
      )
    )

    layout_one = dict(title = 'IT Ranks 5th in Median Hourly Wages',
                xaxis = dict(title = 'Median Hourly Wage'),
                yaxis = dict(title = 'Department'),
                margin = dict(l=220)
                )

# Second chart plots Top 10 Crime Descriptions by Number of Occurrences  
    graph_two = []

    graph_two.append(
      go.Bar(
      x = crime['count'][::-1].tolist(),
      y = crime['crime_description'][::-1].tolist(),
      orientation = 'h'
      )
    )

    layout_two = dict(title = 'Theft and Burglary are the Most Common Crimes',
                xaxis = dict(title = 'Count'),
                #yaxis = dict(title = 'Crime Description')
                margin = dict(l=220)
                )


# Third chart plots Top 10 Deparments by Approved Operating Budget
    graph_three = []
    graph_three.append(
      go.Bar(
      x = seattle_budget_top_10['approved_amount'][::-1].tolist(),
      y = seattle_budget_top_10['department'][::-1].tolist(),
      orientation = 'h'
      )
    )

    layout_three = dict(title = 'City Light and Utilities Have the Largest Budgets in 2018',
                xaxis = dict(title = 'Approved Amount ($)'),
                yaxis = dict(title = 'Department'),
                margin = dict(l=260)
                       )
    
# Fourth chart shows budget growth over the last 9 years
    graph_four = []
    
    graph_four.append(
      go.Scatter(
      x = yearly_budget['fiscal_year'].tolist(),
      y = yearly_budget['approved_amount'].tolist(),
      mode = 'lines+markers'
      )
    )

    layout_four = dict(title = "Annual Budget Grew by $2 Billion Over The Last 9 Years",
                xaxis = dict(title = 'Year'),
                yaxis = dict(title = 'Approved Amount (Billions)')
                )

    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))

    return figures