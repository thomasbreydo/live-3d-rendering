import numpy as np
import plotly.graph_objects as go

from .local_stats import build_hover_data


def render(image, width, height, colorscale=None, rx=None, ry=None, *args, **kwargs):
    """Create a surface figure from a 2D image through linear interpolation.

    Args:
        image (numpy.ndarray | PIL.Image): image to display
        width: width of 3D plot
        height: height of 3D plot
        colorscale: colorscale for plot
        rx: distance from center to leftmost pixel in window for local
            stats (default 2)
        ry: distance from center to bottommost pixel in window for
            local stats (default 2)

    Returns:
        The surface figure object.
    """

    if colorscale is None:
        colorscale = ["black", "rgb(192, 192, 192)"]
    ar = np.array(image).T
    fig = go.Figure(
        data=[
            go.Surface(
                z=ar,
                colorscale=colorscale,
                showscale=False,
                customdata=build_hover_data(ar, rx=rx, ry=ry),
                hovertemplate="<em>Local stats</em>"
                "<br>min: %{customdata[0]}"
                "<br>max: %{customdata[1]}"
                "<br>mean: %{customdata[2]:.2f}"
                "<br>variance: %{customdata[3]:.2f}<extra></extra>",
            )
        ]
    )
    layout = dict(
        autosize=True,
        width=width,
        height=height,
        hovermode="closest",
        showlegend=False,
        scene=dict(
            xaxis=dict(title="", showticklabels=False),
            yaxis=dict(title="", showticklabels=False),
            zaxis=dict(title="", showticklabels=False),
        ),
        margin=dict(r=0, l=0, t=0, b=0),
        uirevision="constant",
        *args,
        **kwargs,
    )
    fig.update_layout(layout)
    return fig


def display(image, width, height, colorscale=None, *args, **kwargs):
    """Display the 2D image in an interactive 3D plot.

    Args:
        colorscale: colorscale for plot
        width: width of 3D plot
        height: height of 3D plot
        image (numpy.ndarray | PIL.Image): image to display
    """
    fig = render(image, width, height, colorscale, *args, **kwargs)
    fig.show()
