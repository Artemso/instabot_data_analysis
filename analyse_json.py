import json
import plotly.graph_objects as go
import networkx as nx
from bokeh.io import output_file, show
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, TapTool, BoxSelectTool, PanTool, WheelZoomTool, ResetTool
from bokeh.models import HoverTool, TapTool, BoxSelectTool
from bokeh.models.graphs import NodesAndLinkedEdges, EdgesAndLinkedNodes
from bokeh.palettes import Spectral4
from bokeh.plotting import from_networkx

class Visualise():
	def __init__(self):
		return None

	def sort_by_val_len(self, u_dict):
		sorted_lst = sorted(u_dict.items(), key=lambda item : len(item[1]), reverse=True)
		return sorted_lst

	def bar_total_following(self, user_dict, sort=0, disp_avg=0):
		if sort:
			temp_lst = self.sort_by_val_len(user_dict)
		else:
			temp_lst = list(user_dict.items())
		user_list = []
		user_count = []
		for x in temp_lst:
			user_list.append(x[0])
			user_count.append(len(x[1]))
		fig = go.Figure()
		fig.add_trace(go.Bar(name='followng', x=user_list, y=user_count))
		if disp_avg:
			avg = int(sum(user_count)/len(user_count))
			lst = [avg] * len(user_count)
			fig.add_trace(go.Scatter(name='average', x=user_list, y=lst))
		fig.show()
	
	def add_nodes(self, graph, user_dict):
		for key in user_dict:
			graph.add_node(key)
			for underkey in user_dict[key]:
				graph.add_node(underkey)
	
	def add_edges(self, graph, user_dict):
		for key in user_dict:
			for underkey in user_dict[key]:
				graph.add_edge(key, underkey)

	def network_total_following(self, user_dict):
		graph = nx.Graph()
		self.add_nodes(graph, user_dict)
		self.add_edges(graph, user_dict)
		# graph.remove_node('artmslpv')
		for node in list(graph.nodes()):
			if len(list(graph.neighbors(node))) < 2:
				graph.remove_node(node)
		for node in list(graph.nodes()):
			if len(list(graph.neighbors(node))) < 7:
				graph.remove_node(node)
		plot = Plot(
			plot_width=1140,
			plot_height=720,
			x_range=Range1d(-1.1,1.1),
			y_range=Range1d(-1.1,1.1))
		plot.add_tools(
			HoverTool(tooltips=[('','@name')],
				line_policy='nearest'),
			TapTool(),
			BoxSelectTool(),
			PanTool(),
			WheelZoomTool(),
			ResetTool())
		graph_render = from_networkx(graph, nx.spring_layout, scale=1.8, center=(0,0))
		graph_render.node_renderer.data_source.data['name'] = list(graph.nodes())
		graph_render.node_renderer.glyph = Circle(
			size=10,
			fill_color=Spectral4[0])
		graph_render.node_renderer.hover_glyph = Circle(
			size=15,
			fill_color=Spectral4[1])
		graph_render.node_renderer.selection_glyph = Circle(
			size=20,
			fill_color=Spectral4[2])
		graph_render.edge_renderer.glyph = MultiLine(
			line_color="#CCCCCC",
			line_alpha=0.2,
			line_width=2)
		graph_render.edge_renderer.hover_glyph = MultiLine(
			line_color=Spectral4[1],
			line_width=3)
		graph_render.edge_renderer.selection_glyph = MultiLine(
			line_color=Spectral4[2],
			line_width=5)
		graph_render.selection_policy = NodesAndLinkedEdges()
		graph_render.inspection_policy = NodesAndLinkedEdges()
		plot.renderers.append(graph_render)
		show(plot)
		# pos = nx.spring_layout(graph, k=0.5, iterations=20)
		# edge_x = []
		# edge_y = []
		# for edge in graph.edges():
		# 	x0, y0 = pos.get(edge[0])
		# 	x1, y1 = pos.get(edge[1])
		# 	edge_x.append(x0)
		# 	edge_x.append(x1)
		# 	edge_x.append(None)
		# 	edge_y.append(y0)
		# 	edge_y.append(y1)
		# 	edge_y.append(None)
		# edge_trace = go.Scatter(
		# 	x =edge_x, y = edge_y,
		# 	line=dict(width=0.5, color='#888'),
		# 	hoverinfo='none',
		# 	mode='lines'
		# )
		# node_x = []
		# node_y = []
		# for node in graph.nodes():
		# 	x, y = pos.get(node)
		# 	node_x.append(x)
		# 	node_y.append(y)
		# node_trace = go.Scatter(
		# 	x = node_x, y = node_y,
		# 	mode='markers',
		# 	hoverinfo='text'
		# )
		# node_trace.text = list(graph.nodes())
		# fig = go.Figure(data=[edge_trace, node_trace],
		# layout=go.Layout(
		# 	title='Network graph of people I\'m following',
		# 	titlefont_size=16,
		# 	showlegend=False,
		# 	hovermode='closest',
		# 	margin=dict(b=20,l=5,r=5,t=40),
		# 	xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        #     yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
		# ))
		# fig.show()




with open('user_dict.json', 'r') as fd:
	user_dict = json.load(fd)
bar = Visualise()
bar.network_total_following(user_dict)
# bar.bar_total_following(user_dict, sort=False, disp_avg=False) # takes user dictionary, optional args: sort, diplay_average