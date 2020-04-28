import json

import networkx as nx

from bokeh.io import show
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, TapTool, BoxSelectTool, PanTool, WheelZoomTool, ResetTool
from bokeh.models.graphs import NodesAndLinkedEdges
from bokeh.palettes import Plasma11, Greys4
from bokeh.plotting import from_networkx, figure, ColumnDataSource
from bokeh.transform import linear_cmap

class Visualise():
	def __init__(self):
		pass

	def sort_by_val_len(self, u_dict):
		sorted_lst = sorted(u_dict.items(), key=lambda item : len(item[1]), reverse=True)
		return sorted_lst

	def bar_total_following(self, user_dict, sort=0, disp_avg=0):
		if sort:
			temp_list = self.sort_by_val_len(user_dict)
		else:
			temp_list = list(user_dict.items())
		user_list = []
		user_count = []
		for x in temp_list:
			user_list.append(x[0])
			user_count.append(len(x[1]))
		bar = figure(
			x_range=user_list,
			plot_width=1350,
			plot_height=720)
		bar.add_tools(
			HoverTool(tooltips=[('User','@user_list'),
				('following', '@user_count')]),
			BoxSelectTool(),
			TapTool())
		data = {
			'user_count': user_count,
			'user_list': user_list
		}
		bar.vbar(x='user_list',top='user_count', width=0.8, source=data)
		bar.xgrid.grid_line_color = None
		bar.xaxis.major_label_orientation = 1
		if disp_avg:
			avg = int(sum(user_count)/len(user_count))
			bar.line(x=user_list, y=avg, color='red', line_width=2)
		show(bar)

	def add_nodes(self, graph, user_dict):
		for key in user_dict:
			graph.add_node(key)
			for underkey in user_dict[key]:
				graph.add_node(underkey)
	
	def add_edges(self, graph, user_dict):
		for key in user_dict:
			for underkey in user_dict[key]:
				graph.add_edge(key, underkey)

	def get_list_of_edges(self, graph):
		edge_list = []
		for node in graph.nodes():
			edge_list.append(len(list(graph.neighbors(node))))
		return edge_list

	def network_total_following(self, user_dict, n_neighbors=5):
		graph = nx.Graph()
		self.add_nodes(graph, user_dict)
		self.add_edges(graph, user_dict)
		for node in list(graph.nodes()):
			if len(list(graph.neighbors(node))) < n_neighbors:
				graph.remove_node(node)
		plot = Plot(
			plot_width=1140,
			plot_height=720,
			x_range=Range1d(-1.1,1.1),
			y_range=Range1d(-1.1,1.1))
		plot.add_tools(
			HoverTool(tooltips=[('User','@name'),
				('Neighbors', '@neighbors')],
				line_policy='nearest'),
			TapTool(),
			BoxSelectTool(),
			PanTool(),
			WheelZoomTool(),
			ResetTool())
		graph_render = from_networkx(graph, nx.spring_layout, scale=2.5, center=(0,0))
		graph_render.node_renderer.data_source.data['name'] = list(graph.nodes())
		list_edges = self.get_list_of_edges(graph)
		graph_render.node_renderer.data_source.data['neighbors'] = list_edges
		mapper = linear_cmap('neighbors', palette=Plasma11, low=min(list_edges), high=max(list_edges))
		graph_render.node_renderer.glyph = Circle(
			size=10,
			fill_color=mapper)
		graph_render.node_renderer.hover_glyph = Circle(
			size=200,
			fill_color=mapper)
		graph_render.node_renderer.selection_glyph = Circle(
			size=200,
			fill_color=mapper)
		graph_render.edge_renderer.glyph = MultiLine(
			line_color=Greys4[2],
			line_alpha=0.3,
			line_width=1)
		graph_render.edge_renderer.hover_glyph = MultiLine(
			line_color=Greys4[1],
			line_width=2)
		graph_render.edge_renderer.selection_glyph = MultiLine(
			line_color=Greys4[0],
			line_width=3)
		graph_render.selection_policy = NodesAndLinkedEdges()
		graph_render.inspection_policy = NodesAndLinkedEdges()
		plot.renderers.append(graph_render)
		show(plot)

with open('user_dict.json', 'r') as fd:
	user_dict = json.load(fd)
bar = Visualise()
# bar.network_total_following(user_dict, n_neighbors=6) # takes user dictionary, optional args: n_neigbors
bar.bar_total_following(user_dict, sort=True, disp_avg=True) # takes user dictionary, optional args: sort, diplay_average