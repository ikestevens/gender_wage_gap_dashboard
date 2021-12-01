import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])

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

summary = '''
#### Gender Wage Gap In America

Despite efforts to decrease the wage gap in America, research shows that the gender wage gap has hardly shrunk in
recent decades. In the New York Times article ["In 25 years, the Pay Gap Has Shrunk By Just 8 Cents"](https://www.nytimes.com/2021/03/24/us/equal-pay-day-explainer.html),
Donner and Goldberg explain that the pay gap has decreased marginally in the last 25 years. Though many women clearly
have the same skills and disposition as their male counterparts, there exist discrimination and bias that prevent
women from equal pay.


##### General Social Survey Data

Since 1972, the General Social Survey (GSS) has conducted comprehensive surveys to monitor social trends and
general metric shifts in the American population. These metrics include recording American attitudes toward a wide array
of topics such as crime and violence, group tolerance, religion, national spending, psychological well-being, social mobility, and stress and traumatic events.
The General Social Survey has been collecting this data in order to provide researchers free and high-quality data to
understand and research American societal changes and trends.

'''

gender_group = gss_clean.groupby("sex").mean().round(2).reset_index()[['sex', 'income', 'job_prestige', 'socioeconomic_index']]
gender_group = gender_group.rename(columns={'sex':'Gender', 'income': 'Income', 'job_prestige': 'Occupational Prestige', 'socioeconomic_index': 'Socioeconomic Index'})
table_prob2 = ff.create_table(gender_group)

app7 = JupyterDash(__name__, external_stylesheets=external_stylesheets)

app7.layout = html.Div(
    [
        html.H1("Gender Wage Gap Dashboard"),

        dcc.Markdown(children = summary),

        html.H3("Average General Social Survey Metrics by Gender"),

        dcc.Graph(figure=table_prob2)

    ]
)


if __name__ == '__main__':
    app7.run_server(mode='inline', debug=True, port=8051)
