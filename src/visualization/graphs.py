import json

import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.offline import iplot, init_notebook_mode

def getJsonArray(filepath):
    """deprecated"""
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

def load_json(filepath):
    with open(filepath) as file:
        return json.loads(file.read())

def getDataAtTime(jsonObject):
    return list(map(lambda item: item["values"], jsonObject["data"]))

def filter_objects(object_type, json_object):
    json_array = json_object["data"]
    filtered_arrays = map(lambda item: list(filter(lambda obj: obj["type"] == "ObjectTypes." + object_type, item["values"])), json_array)
    return list(filtered_arrays)

def count_objects(object_type, json_object):
    """
    Count objects of chosen type from json_array.
    Returns List[int]
    """
    filtered_arrays = filter_objects(object_type, json_object)
    lengths = map(len, filtered_arrays)
    return list(lengths)

def create_cyanobacteria_and_bacteria_graph(json_object, output_filename):
    ball_count = count_objects("BALL", json_object)
    cyanobacteria_count = count_objects("CYANO_BACTERIA", json_object)

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


def create_cyanobacteria_and_docked_cyanobacteria_graph(json_object, output_filename):
    ball_objects = filter_objects("BALL", json_object)
    docked_cyanobacterias = list(map(lambda balls: sum(map(lambda ball: ball["docked"], balls)), ball_objects))
    cyanobacteria_count = count_objects("CYANO_BACTERIA", json_object)

    trace_docked = go.Scatter(x=list(range(len(docked_cyanobacterias))),
                              y=docked_cyanobacterias,
                              mode="lines",
                              name="Docked cyanobacteria")
    trace_cyanobacteria = go.Scatter(x=list(range(len(cyanobacteria_count))),
                                     y=cyanobacteria_count,
                                     mode="lines",
                                     name="All cyanobacteria")

    data = [trace_docked, trace_cyanobacteria]

    layout = {
        "title": "Dependency of cyanobacteria and docked cyanobacteria on time",
        "xaxis": {"title":"Iteration number"},
        "yaxis": {"title":"Object count"},
        }
    fig = go.Figure(data=data, layout=layout)
    fig.write_html(output_filename)

def main():
    json = load_json(r"..\..\storage\data.json")
    create_cyanobacteria_and_bacteria_graph(json, "graph1.html")
    create_cyanobacteria_and_docked_cyanobacteria_graph(json, "graph2.html")


if __name__ == "__main__":
    main()
