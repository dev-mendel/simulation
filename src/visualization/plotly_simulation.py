import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.offline import iplot, init_notebook_mode


def create_graph(balls, cyas, bubbles):
    assert len(balls) == len(cyas) and len(cyas) == len(bubbles)
    trace0 = go.Scatter(x=list(range(len(balls))),
                        y=balls,
                        mode="lines",
                        name="balls")
    trace1 = go.Scatter(x=list(range(len(cyas))),
                        y=cyas,
                        mode="lines",
                        name="cyas")
    trace2 = go.Scatter(x=list(range(len(bubbles))),
                        y=bubbles,
                        mode="lines",
                        name="bubbles")
    data = [trace0, trace1, trace2]

    layout = {
        "title": "My awesome title",
        "xaxis": {"title":"Iteration"},
        "yaxis": {"title":"Object count"},
        }
    fig = go.Figure(data=data, layout=layout)
    fig.write_html("data.html")

if __name__ == "__main__":
    # run example
    create_graph([20, 18, 15, 10, 18, 15, 10, 20, 18, 15, 10],
                 [10, 12, 14, 13, 12, 14, 13, 10, 12, 14, 13],
                 [2, 3, 2, 4, 2, 3, 2, 4, 2, 3, 2])
