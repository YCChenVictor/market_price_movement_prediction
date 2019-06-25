"""
The forceatlas2 source: https://github.com/bhargavchippada/forceatlas2
"""

import networkx as nx
from fa2 import ForceAtlas2
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt


class Create_Network:  # try the data visualization to make correct decision

    def __init__(self, connectedness_table):
        self.Connectedness_table = connectedness_table
        self.Names = None
        self.From_other = None
        self.To_other = None
        self.Graph = None
        self.Plot = None

    def change_names(self, names):

        self.Names = names

    def create_network(self):

        graph = nx.Graph()

        connectedness_table = self.Connectedness_table

        self.From_other = connectedness_table.iloc[:, -1]
        self.To_other = connectedness_table.iloc[-1, :]

        connectedness_table = connectedness_table[:-1]
        connectedness_table = connectedness_table.iloc[:, :-1]

        connectedness = connectedness_table.values

        for i in range(len(connectedness)):
            for j in range(len(connectedness[i])):
                """
                Use average of to and from connectedness to represent the
                degree of bondness, however, causing we can't tell the to and
                from degree, needs more modification

                connectedness[i][j] means
                """
                if i == j:
                    break
                else:
                    if self.Names is None:
                        graph.add_edge(i, j, weight=(connectedness[i][j] +
                                                     connectedness[j][i]) / 2)
                    else:
                        graph.add_edge(self.Names[i], self.Names[j],
                                       weight=(connectedness[i][j] +
                                               connectedness[j][i]) / 2)

        self.Graph = graph

    def plot(self):

        forceatlas2 = ForceAtlas2(

            # Behavior alternatives
            outboundAttractionDistribution=False,  # Dissuade hubs
            linLogMode=False,  # NOT IMPLEMENTED
            adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
            edgeWeightInfluence=1.0,

            # Performance
            jitterTolerance=1.0,  # Tolerance
            barnesHutOptimize=True,
            barnesHutTheta=1.2,
            multiThreaded=False,  # NOT IMPLEMENTED

            # Tuning
            scalingRatio=2.0,
            strongGravityMode=False,
            gravity=1.0,

            # Log
            verbose=True)

        # fixed_positions = {"^TWII_vol": (0, 0)}

        positions = (forceatlas2.
                     forceatlas2_networkx_layout(self.Graph,
                                                 pos=None, iterations=1000000))
        self.Plot = nx.draw_networkx(self.Graph, positions,
                                     with_labels=True)
        self.Plot = nx.draw_networkx_edges(self.Graph, positions,
                                           edge_color="green", alpha=0.4)
        self.Plot = nx.draw_networkx_nodes(self.Graph, positions,
                                           node_size=50,
                                           node_color="blue", alpha=0.4)

    def show_draw(self):

        plt.axis('off')
        plt.show(self.Plot)

    def close_draw(self):

        plt.close(self.Plot)


class Specific_Network(Create_Network):

    def __init__(self, vol_df, periods_one_conn):
        self.vol_df = vol_df
        self.periods_one_conn = periods_one_conn
        self.vol_dict = None

    def divide_vol_dataframe(self):

        # required variables
        dataframe = self.vol_df
        periods = self.periods_one_conn

        # list to save the data
        vol_dict = {}

        # iteratively divide dataframe
        for i in range(len(dataframe)):

            # get divided data
            data = dataframe.iloc[i: periods+i, :]
            if len(data) < periods:
                break

            # reset the index and get the end date
            data = data.reset_index(drop=True)
            end_dt = data["Date"].iloc[-1]
            # print(end_dt)

            # add to data_dict
            vol_dict[end_dt] = data

        self.vol_dict = vol_dict
