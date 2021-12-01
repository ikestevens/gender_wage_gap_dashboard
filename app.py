import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
import flask
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

summary = '''
#### Gender Wage Gap In America

Despite efforts to erase the wage gap in America, research shows that the gender wage gap has hardly shrunk in
recent decades. In the New York Times article ["In 25 years, the Pay Gap Has Shrunk By Just 8 Cents"](https://www.nytimes.com/2021/03/24/us/equal-pay-day-explainer.html),
Donner and Goldberg explain that the pay gap has decreased marginally in the last 25 years. Though many women clearly
have the same skills and backgrounds as their male counterparts, there exists discrimination and bias that prevent
women from receiving equal pay.


##### General Social Survey Data

Since 1972, the General Social Survey (GSS) has conducted comprehensive surveys to monitor social trends and
general metric shifts in the American population. These metrics include recording American attitudes toward a wide array
of topics such as crime and violence, group tolerance, religion, national spending, psychological well-being, social mobility, and stress and traumatic events.
The General Social Survey has been collecting this data in order to provide researchers free and high-quality data to
understand and research American societal changes and trends.

'''

gss = pd.read_csv("wage_gap2.csv")

'''
gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])
'''

#gss.to_csv("wage_gap2.csv")

mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk']
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight',
                              'educ':'education',
                              'coninc':'income',
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige',
                              'papres10':'father_job_prestige',
                              'sei10':'socioeconomic_index',
                              'fechld':'relationship',
                              'fefam':'male_breadwinner',
                              'fehire':'hire_women',
                              'fejobaff':'preference_hire_women',
                              'fepol':'men_bettersuited',
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')
gss_clean['Education'] = pd.cut(gss_clean['education'], bins = [0, 11, 15, 25], labels = ['Not Graduated', "High School Graduate", "Advanced Degrees"])


gender_group = gss_clean.groupby("sex").mean().round(2).reset_index()[['sex', 'income', 'job_prestige', 'socioeconomic_index']]
gender_group = gender_group.rename(columns={'sex':'Gender', 'income': 'Income', 'job_prestige': 'Occupational Prestige', 'socioeconomic_index': 'Socioeconomic Index'})
table_prob2 = ff.create_table(gender_group)

labels = ['satjob', 'relationship', 'male_breadwinner', 'men_bettersuited', 'child_suffer', 'men_overwork']

group_prob4 = gss_clean.groupby('sex').mean().reset_index()

prob4 = px.scatter(gss_clean.head(200), x='job_prestige', y='income',
                 color = 'sex',
                 trendline='ols',
                 height=600, width=600,
                 title="Occupational Prestige and Income Scatterplot by Gender",
                 hover_data=['education', 'socioeconomic_index'],
                 color_discrete_map = {'male':'blue', 'female':'red'},
                 labels={'job_prestige':'Occupational Prestige Score',
                        'income':'Income Level'})

prob6_df = gss_clean[['income', 'sex', 'job_prestige']]
prob6_df['job_status_bucket'] = pd.cut(gss_clean["job_prestige"], bins = [16, 26, 37, 47, 58, 68, 80], labels = ["Low", "Medium Low", "Medium", "Medium High", "High", "Super High"])
prob6_df = prob6_df.dropna()

fig6 = px.box(prob6_df, x='income', color = 'sex',
             facet_col = 'job_status_bucket', facet_col_wrap=2,
             labels={'income':'Income'},
             title="Income Distibution By Job Prestige and By Gender",
             color_discrete_map = {'male':'blue', 'female':'red'},
            category_orders={"job_status_bucket": ["Low", "Medium Low", "Medium", "Medium High", "High", "Super High"]})
fig6.for_each_annotation(lambda a: a.update(text=a.text.replace("job_status_bucket=", "")))

prob5_1 = px.box(gss_clean, x='income', color = 'sex',
                   labels={'income':'Income'},
                   title="Income Distribution By Gender",
                   color_discrete_map = {'male':'blue', 'female':'red'})

prob5_2 = px.box(gss_clean, x='job_prestige', color = 'sex',
                   labels={'job_prestige':'Occupational Prestige'},
                   title="Occupational Prestige Distribution By Gender",
                   color_discrete_map = {'male':'blue', 'female':'red'})

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


app.layout = html.Div(
    [
        html.Div([
            html.H1("Gender Wage Gap Dashboard"),

        ], style={'width': '70%', 'float': 'left'}),

        html.Div([
            html.H3("By Isaac Stevens (is3sb)"),

        ], style={'width': '25%', 'float': 'right'}),

        html.Div(children=[dcc.Markdown(children = summary)], style={"border":"2px black solid", 'float': 'left'}),

        html.Div([

            html.H3("General Overview Averages By Gender"),

            dcc.Graph(figure=table_prob2),

        ]),

        html.H3("Responses to Social Statements (grouped by Sex, Region, or Education)"),

        html.Div([

        html.Div([

            html.P("Select Topic In Dropdown Below:"),

            dcc.Dropdown(id='x-axis',
            options=[{'label': i, 'value': i} for i in labels],
            value='male_breadwinner'),

            html.P("Select Category to Group By:"),

            dcc.Dropdown(id='grouping',
            options=[{'label': i, 'value': i} for i in ['sex', 'region', 'Education']],
            value='sex'),

        ], style={'width': '25%', 'float': 'left'})

        ]),

        html.Div([

            dcc.Graph(id="graph")

        ], style={'width': '70%', 'float': 'right'}),

        html.Div([

            dcc.Graph(figure=fig6)

        ], style={'width': '48%', 'float': 'left'}),

        html.Div([

            dcc.Graph(figure=prob4)

        ], style={'width': '48%', 'float': 'right'}),

        html.Div([

            dcc.Graph(figure=prob5_1)

        ], style = {'width':'48%', 'float':'left'}),

        html.Div([

            dcc.Graph(figure=prob5_2)

        ], style = {'width':'48%', 'float':'right'}),

    ]
)

@app.callback(
    Output(component_id='graph', component_property='figure'),
    [Input(component_id='x-axis', component_property='value'),
    Input(component_id='grouping', component_property='value')]
)
def make_figure(x, y):
    bar_prob3 = gss_clean.groupby([y, x]).size().reset_index()
    return px.bar(bar_prob3, x=x, y=0, color=y,
       barmode = 'group',
       labels={'0':'Count of Responses', 'male_breadwinner':"Response to 'Men Should Work Outside the House and Women Inside'",
                'satjob': "Response to 'How Satisfied Are You With the Work You Do?'",
                'child_suffer': "Response to 'A preschool child is likely to suffer if his or her mother works.'",
                'men_overwork': "Response to 'Family life often suffers because men concentrate too much on their work.'",
                'men_bettersuited': "Response to 'Most men are better suited emotionally for politics than are most women'",
                'relationship': "Response to 'A Working Mother Can Establish Just As Warm and Secure a Relationship with her Children as a Mother who Does Not Work'"},
        category_orders={"male_breadwinner": ["strongly disagree", "disagree", "agree", "strongly disagree"],
                        "relationship": ["strongly disagree", "disagree", "agree", "strongly disagree"],
                        "child_suffer": ["strongly disagree", "disagree", "agree", "strongly disagree"],
                        "men_overwork": ["strongly disagree", "disagree", "neither agree nor disagree", "agree", "strongly disagree"],
                        "men_bettersuited": ["disagree", "agree"],
                          "satjob": ["very dissatisfied", "a little dissat", "mod. satisfied", "very satisfied"]},
        color_discrete_map = {'male':'blue', 'female':'red'}
            )

if __name__ == '__main__':
    app.run_server(debug=True, port=8051, host='0.0.0.0')
