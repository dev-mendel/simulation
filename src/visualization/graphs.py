import json

import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.offline import iplot, init_notebook_mode

def getJsonArray(filepath):
    with open(filepath) as file:
        lines = file.readlines()
        #print(lines[0:4])
        return list(map(lambda x: json.loads(x[7:]),
                        filter(lambda x: x[0:5] == "Event" and x[7] == '{', lines)))
        """
        lines = list(filter(lambda x: x[0:5] == "Event" and x[7] == '{', lines))
        result = []
        for i in range(len(lines)):
            print(i)
            result.append(json.loads(lines[i][7:]))
        return result
        """

def count_objects(object_type, json_array):
    """
    Count objects of chosen type from json_array.
    Returns List[int]
    """
    filtered_arrays = map(lambda item: list(filter(lambda obj: obj["type"] == "ObjectTypes." + object_type, item["values"])), json_array)
    lengths = map(len, filtered_arrays)
    return list(lengths)

def create_cyanobacteria_and_bacteria_graph(jsonArray, output_filename):
    ball_count = count_objects("BALL", jsonArray)
    cyanobacteria_count = count_objects("CYANO_BACTERIA", jsonArray)

    trace_ball = go.Scatter(x=list(range(len(ball_count))),
                            y=ball_count,
                            mode="lines",
                            name="Ball")
    trace_cyanobacteria = go.Scatter(x=list(range(len(cyanobacteria_count))),
                                     y=cyanobacteria_count,
                                     mode="lines",
                                     name="Cyanobacteria")

    data = [trace_ball, trace_cyanobacteria]

    layout = {
        "title": "Dependency of cyanobacteria and ball on time",
        "xaxis": {"title":"Iteration number"},
        "yaxis": {"title":"Object count"},
        }
    fig = go.Figure(data=data, layout=layout)
    fig.write_html(output_filename)

