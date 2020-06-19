import dash
import dash_core_components as dcc
import dash_html_components as html

import magic


def generate_table(columns, rows):
    return html.Table(
        [
            html.Thead(html.Tr([html.Th(col) for col in columns])),
            html.Tbody([html.Tr([html.Td(r) for r in row]) for row in rows]),
        ]
    )


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.css.config.serve_locally = True

magic.set_log()
estrategia, small_caps, numero_empresas, setor = magic.parse_param()
rank = magic.rank(estrategia, small_caps, numero_empresas, setor)

app.layout = html.Div(
    children=[
        html.H4(children="Magic Formula"),
        generate_table(rank["collumns"], rank["data"][:30]),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
