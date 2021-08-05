import base64
import io
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
import live_3d_rendering as l3d
from PIL import Image, ImageFilter
from dash.dependencies import Input, Output, State
from live_3d_rendering.local_stats import get_local_stats
from live_3d_rendering.stats_functions import (
    local_min,
    local_max,
    local_mean,
    local_variance,
)

STATS_FUNCTIONS = [local_min, local_max, local_mean, local_variance]
HOME_ICON = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA5MjguNiAxMDAwIiBjbGFzcz0iaWNvbiIgaGVpZ2h0PSIxZW0iIHdpZHRoPSIxZW0iPjxwYXRoIGQ9Im03ODYgMjk2di0yNjdxMC0xNS0xMS0yNnQtMjUtMTBoLTIxNHYyMTRoLTE0M3YtMjE0aC0yMTRxLTE1IDAtMjUgMTB0LTExIDI2djI2N3EwIDEgMCAydDAgMmwzMjEgMjY0IDMyMS0yNjRxMS0xIDEtNHogbTEyNCAzOWwtMzQtNDFxLTUtNS0xMi02aC0ycS03IDAtMTIgM2wtMzg2IDMyMi0zODYtMzIycS03LTQtMTMtNC03IDItMTIgN2wtMzUgNDFxLTQgNS0zIDEzdDYgMTJsNDAxIDMzNHExOCAxNSA0MiAxNXQ0My0xNWwxMzYtMTE0djEwOXEwIDggNSAxM3QxMyA1aDEwN3E4IDAgMTMtNXQ1LTEzdi0yMjdsMTIyLTEwMnE1LTUgNi0xMnQtNC0xM3oiIHRyYW5zZm9ybT0ibWF0cml4KDEgMCAwIC0xIDAgODUwKSIvPjwvc3ZnPg=="  # noqa line too long
MODE_BAR_BUTTONS_TO_REMOVE = [
    "zoom3d",
    "pan3d",
    "orbitRotation",
    "tableRotation",
    "handleDrag3d",
    "resetCameraLastSave3d",
    "hoverClosest3d",
    "toImage",
]
RX = 25
RY = 25


def format_local_stats(local_stats):
    return html.Ul(
        id="local-stats-list",
        className="mt-3 mb-0",
        children=[
            html.Li(f"Min: {local_stats[0]}"),
            html.Li(f"Max: {local_stats[1]}"),
            html.Li(f"Mean: {local_stats[2]:.2f}"),
            html.Li(f"Variance: {local_stats[3]:.2f}"),
        ],
    )


app = Dash(
    __name__,
    external_stylesheets=[
        "https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css"
    ],
    suppress_callback_exceptions=True,
)
server = app.server
app.title = "Image2Surface"

app.layout = html.Div(
    className="mt-md-4 mb-md-4 mt-3 mb-3",
    children=[
        html.Div(
            className="container",
            children=[
                html.Div(
                    className="row align-items-center",
                    children=[
                        html.Div(
                            className="col-lg-3",
                            children=[
                                html.Div(
                                    id="side-panel",
                                    children=[
                                        html.H3(
                                            children=app.title,
                                        ),
                                        html.Hr(),
                                        html.Div(
                                            children=[
                                                html.B("Camera controls"),
                                                html.Br(),
                                                html.Ol(
                                                    className="mb-0",
                                                    children=[
                                                        html.Li(
                                                            "Left-click and drag to rotate"
                                                        ),
                                                        html.Li(
                                                            "Right-click and drag to pan"
                                                        ),
                                                        html.Li("Scroll to zoom"),
                                                        html.Li(
                                                            html.Div(
                                                                children=[
                                                                    html.Span(
                                                                        "Click the ",
                                                                        className="align-text-middle",
                                                                    ),
                                                                    html.Img(
                                                                        src=HOME_ICON
                                                                    ),
                                                                    html.Span(
                                                                        " icon to reset the camera",
                                                                        className="align-text-middle",
                                                                    ),
                                                                ],
                                                            )
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                        html.Hr(),
                                        html.Div(
                                            children=[
                                                html.B("Image upload"),
                                                html.Br(),
                                                html.Div(
                                                    html.Small(
                                                        "Select an image from your computer.",
                                                    ),
                                                    className="text-muted",
                                                ),
                                                dcc.Upload(
                                                    id="image-upload",
                                                    children=html.Button(
                                                        "Choose file",
                                                        className="btn btn-primary w-100 mt-3",
                                                    ),
                                                    multiple=False,
                                                ),
                                            ]
                                        ),
                                        html.Hr(),
                                        html.Div(
                                            children=[
                                                html.B("Smoothing"),
                                                html.Div(
                                                    html.Small(
                                                        "Control how much sharp edges are smoothed out."
                                                    ),
                                                    className="text-muted",
                                                ),
                                                dcc.Input(
                                                    id="blur-amt",
                                                    value="2",
                                                    min="0",
                                                    max="9",
                                                    step="1",
                                                    type="range",
                                                    className="w-100 mt-3",
                                                ),
                                            ],
                                        ),
                                        html.Hr(),
                                        html.Div(
                                            children=[
                                                html.B("Local stats"),
                                                html.Div(
                                                    html.Small(
                                                        "Click on a point to see local stats.",
                                                    ),
                                                    className="text-muted",
                                                ),
                                                html.Div(
                                                    id="local-stats-inner",
                                                    children=format_local_stats(
                                                        [0] * len(STATS_FUNCTIONS)
                                                    ),
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        html.Div(
                            className="col-lg-9 mt-4 mt-lg-0",
                            children=[
                                dcc.Loading(
                                    id="figure-loading",
                                    type="dot",
                                    color="#0275d8",
                                    children=[
                                        html.Div(
                                            id="figure-container",
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                html.Footer("© 2021 Thomas Breydo", className="text-muted pt-5"),
            ],
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
            return html.Div(
                "There was an error processing your image.",
                className="text-danger text-center",
            )
    fig = l3d.render(
        l3d.preprocess(image).filter(ImageFilter.GaussianBlur(blur_radius)),
        height=700,
    )
    return dcc.Graph(
        id="surface-plot",
        figure=fig,
        config=dict(
            modeBarButtonsToRemove=MODE_BAR_BUTTONS_TO_REMOVE,
            displayModeBar=True,
            displaylogo=False,
        ),
    )


@app.callback(
    Output("figure-container", "children"),
    Input("blur-amt", "value"),
    Input("image-upload", "contents"),
    State("image-upload", "filename"),
    State("image-upload", "last_modified"),
)
def update_plot(blur, uploaded, fname, last_modified):
    return render_plot(int(blur), uploaded, fname, last_modified)


@app.callback(
    Output("local-stats-inner", "children"),
    Input("surface-plot", "clickData"),
    State("surface-plot", "figure"),
)
def on_click(click_data, fig):
    if click_data is None:
        raise PreventUpdate
    clicked = click_data["points"][0]
    local_stats = get_local_stats(
        fig["data"][0]["z"],
        stats_functions=STATS_FUNCTIONS,
        pixel_row=clicked["y"],
        pixel_col=clicked["x"],
        rx=RX,
        ry=RY,
    )
    return format_local_stats(local_stats)


if __name__ == "__main__":
    app.run_server(debug=True)
