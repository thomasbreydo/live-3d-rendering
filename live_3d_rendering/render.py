import numpy as np
import plotly.graph_objects as go


def render(image, colorscale=None, width=500, height=500, *args, **kwargs):
    """Create a surface figure from a 2D image through linear interpolation.

    Args:
        colorscale: colorscale for plot
        width: width of 3D plot
        height: height of 3D plot
        image (numpy.ndarray | PIL.Image): image to display

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
                hoverinfo=None,
            )
        ]
    )
    layout = dict(
        autosize=True,
        width=width,
        height=height,
        hovermode=False,
        showlegend=False,
        scene=dict(
            xaxis=dict(title="", showticklabels=False),
            yaxis=dict(title="", showticklabels=False),
            zaxis=dict(title="", showticklabels=False),
        ),
        *args,
        **kwargs,
    )
    fig.update_layout(layout)
    return fig


def display(image, colorscale=None, width=500, height=500, *args, **kwargs):
    """Display the 2D image in an interactive 3D plot.

    Args:
        colorscale: colorscale for plot
        width: width of 3D plot
        height: height of 3D plot
        image (numpy.ndarray | PIL.Image): image to display
    """
    fig = render(image, colorscale, width, height, *args, **kwargs)
    fig.show()