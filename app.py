import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


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

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        html.H1("Gender Wage Gap Dashboard"),

        dcc.Markdown(children = summary),


    ]
)


if __name__ == '__main__':
    app.run_server(debug=True, port=8051, host='0.0.0.0')
