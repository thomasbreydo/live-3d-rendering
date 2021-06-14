import base64

import dash
import dash_core_components as dcc
import dash_html_components as html
import io
import live_3d_rendering as l3d

from PIL import Image, ImageFilter
from dash.dependencies import Input, Output, State

app = dash.Dash(
    __name__,
    external_stylesheets=[
        "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
    ],
)
server = app.server
app.title = "Image2Surface"

app.layout = html.Div(
    className="main-page",
    children=[
        html.H2("Image2Surface"),
        dcc.Upload(
            id="upload-data",
            children=html.Div(["Drag and Drop or ", html.A("Upload Image")]),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "20px 0",
            },
            multiple=False,
        ),
        html.Div(
            [
                "Smooth (least to most): ",
                dcc.Input(
                    id="blur-amt",
                    value="2",
                    min="0",
                    max="9",
                    step="1",
                    type="range",
                    style={"width": "100%"},
                ),
            ]
        ),
        html.Div(
            id="output-data-upload",
            style={
                "padding": "20px 0px",
            },
            children=html.Em("Loading..."),
        ),
        html.Footer(
            "© 2021 Thomas Breydo",
            style={"padding-top": "30px"},
            className="text-muted",
        ),
    ],
)


def render_plot(blur_radius, contents, filename, date):
    if blur_radius is None:
        blur_radius = 2
    if contents is None or filename is None or date is None:
        image = Image.open("assets/img/figure3.jpg")
    else:
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)
        try:
            image = Image.open(io.BytesIO(decoded))
        except Exception as e:
            print(e)
            return html.Div(["There was an error processing your image."])
    fig = l3d.render(
        l3d.preprocess(image).filter(ImageFilter.GaussianBlur(blur_radius)),
        width=850,
        height=550,
    )
    return dcc.Graph(id="3d-plot", figure=fig)


@app.callback(
    Output("output-data-upload", "children"),
    Input("blur-amt", "value"),
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
    State("upload-data", "last_modified"),
)
def update_plot(b, c, n, d):
    return render_plot(int(b), c, n, d)


if __name__ == "__main__":
    app.run_server(debug=True)
