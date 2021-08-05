from typing import Union, Any, Optional

from PIL.Image import Image
import numpy as np
import plotly.graph_objects as go


def render(
    image: Union[np.ndarray, Image],
    width: Optional[int] = None,
    height: Optional[int] = None,
    colorscale: Optional[Any] = None,
):
    """Create a surface figure from a 2D image through linear interpolation

    Args:
        image: image to display
        width: width of 3D plot
        height: height of 3D plot
        colorscale: colorscale for plot
    Returns:
        The surface figure object.
    """

    if colorscale is None:
        colorscale = ["black", "rgb(192, 192, 192)"]
    ar = np.array(image)[::-1]
    fig = go.Figure(
        [
            go.Surface(
                z=ar,
                colorscale=colorscale,
                showscale=False,
                hovertemplate="(x=%{x}, y=%{y})<extra></extra>",
            )
        ]
    )
    layout = dict(
        autosize=True,
        showlegend=False,
        scene=dict(
            xaxis=dict(title="x", showticklabels=False),
            yaxis=dict(title="y", showticklabels=False),
            zaxis=dict(title="", showticklabels=False),
        ),
        margin=dict(r=0, l=0, t=0, b=0),
        uirevision=True,
        width=width,
        height=height,
    )
    camera = dict(eye=dict(x=0.0, y=-0.75, z=2.5), up=dict(x=0, y=1, z=0))
    modebar = dict(color="rgb(0, 0, 0)")
    fig.update_layout(layout, scene_camera=camera, modebar=modebar)
    return fig
