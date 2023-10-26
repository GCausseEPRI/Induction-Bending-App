import time

import streamlit as st
import pandas as pd
from bokeh.plotting import figure, Figure
from bokeh.models import LinearAxis, Range1d, DatetimeAxis, DatetimeTickFormatter, DataRange1d, Grid

from branding import epri, icons # EPRI branding and style customizations

@st.cache_data()
def read_data() -> pd.DataFrame:
	df = pd.read_pickle('data/Final Data.pickle')

	return df

def  display_head(df: pd.DataFrame) -> None:
	st.header('Machine File Data')
	st.write(df.head(100))

def get_plot_columns(columns: list) -> dict:
	x_column = st.selectbox(
		label='Select a column to use as the X axis',
		options=columns
	)
	columns = columns.drop('Bend Time')
	y_column_left = st.multiselect(
		label='Select columns to attach to the left Y axis',
		options=columns,
	)
	y_column_right = st.multiselect(
		label='Select columns to attach to the right Y axis',
		options=columns,
	)

	selected_columns = {
		'x_column': x_column,
		'y_column_left': y_column_left,
		'y_column_right': y_column_right
	}

	return selected_columns

def check_for_column_selection(columns: dict) -> bool:
	return not columns['y_column_left'] and not columns['y_column_right']

def get_left_axis_label(columns: dict) -> str:
	left_label = ''
	if len(columns['y_column_left']) > 0:
		left_label = columns['y_column_left'][0]
	if len(columns['y_column_left']) > 1:
		for column in columns['y_column_left'][1:]:
			left_label += ', ' + column
	
	return left_label

def create_figure(x_axis_label: str, left_label: str) -> Figure:
	p = figure(
			x_axis_label=x_axis_label,
			y_axis_label=left_label,
			aspect_ratio=(17.5 / 8)
		)
	
	return p

def get_plot_details(column: list) -> tuple:
	column_name_column, graph_type_column, graph_style_column, color_column = st.columns(4)
	line_styles = ['solid', 'dashed', 'dotted', 'dotdash', 'dashdot']
	scatter_styles = ['circle', 'square', 'triangle', 'diamond', 'hex']

	column_name_column.selectbox(label='Column Name', options=[column], label_visibility='collapsed', key=f'name_{column}')
	graph_type = graph_type_column.selectbox(label='Graph Type', options=['Line', 'Scatter'], label_visibility='collapsed', key=f'type_{column}')
	style = graph_style_column.selectbox(label='Marker Style', options=line_styles if graph_type == 'Line' else scatter_styles, label_visibility='collapsed', key=f'style_{column}')
	color = color_column.color_picker(label='Color Choice',value='#000', label_visibility='collapsed', key=f'color_{column}')

	return {'type': graph_type, 'style': style, 'color': color}

def main() -> None:
	epri.init_page(page_title='Induction Bend Analysis Tool', layout='wide')	

	st.title('Induction Bend App')
	df = read_data()
	display_head(df)

	columns = get_plot_columns(df.columns)	

	if check_for_column_selection(columns):
		st.warning('Please choose at least 1 column for either Y axis to plot')
		return
	
	left_label = get_left_axis_label(columns)

	p = create_figure(columns['x_column'], left_label)

	try:
		if pd.api.types.is_datetime64_dtype(df[columns['x_column']]):
			p.xaxis.formatter = DatetimeTickFormatter()

		container = st.container()
		plot_dict_left = {}
		for column in columns['y_column_left']:
			plot_dict_left[column] = get_plot_details(column)

		plot_dict_right = {}
		for column in columns['y_column_right']:
			plot_dict_right[column] = get_plot_details(column)
		
		with container:
			if len(columns['y_column_left']) > 0:
				left_min = df[columns['y_column_left'][0]].min()
				left_max = df[columns['y_column_left'][0]].max()
				if len(columns['y_column_left']) > 1:
					for column in columns['y_column_left']:
						if df[column].min() < left_min:
							left_min = df[column].min()
						if df[column].max() > left_max:
							left_max = df[column].max()
			p.y_range = Range1d(left_min - ((left_max - left_min) * 0.08), left_max + ((left_max - left_min) * 0.08))

			for plot, details in plot_dict_left.items():
				if details['type'] == 'Line':
					p.line(
						df[columns['x_column']],
						df[plot],
						color=details['color'],
						line_dash=details['style'],
						line_width=2,
						legend_label=plot
					)
				else:
					p.scatter(
						df[columns['x_column']],
						df[plot],
						color=details['color'],
						marker=details['style'],
						legend_label=plot
					)
			
			if len(columns['y_column_right']) > 0:
				right_min = df[columns['y_column_right'][0]].min()
				right_max = df[columns['y_column_right'][0]].max()
				if len(columns['y_column_right']) > 1:
					for column in columns['y_column_right']:
						if df[column].min() < right_min:
							right_min = df[column].min()
						if df[column].max() > right_max:
							right_max = df[column].max()
				# p.extra_y_ranges = {'secondary': Range1d(right_min, right_max)}
				p.extra_y_ranges = {'secondary': Range1d(right_min - ((right_max - right_min) * 0.08), right_max + ((right_max - right_min) * 0.08))}
				
				for plot, details in plot_dict_right.items():
					if details['type'] == 'Line':
						p.line(
							df[columns['x_column']],
							df[plot],
							color=details['color'],
							line_dash=details['style'],
							line_width=2,
							y_range_name='secondary',
						legend_label=plot
						)
					else:
						p.scatter(
							df[columns['x_column']],
							df[plot],
							color=details['color'],
							marker=details['style'],
							y_range_name='secondary',
							legend_label=plot
						)
						
				right_label = columns['y_column_right'][0]
				if len(columns['y_column_right']) > 1:
					for column in columns['y_column_right'][1:]:
						right_label += ', ' + column
				p.add_layout(LinearAxis(y_range_name='secondary', axis_label=right_label), 'right')
			p.axis.axis_label_text_font_style = 'normal'
			p.toolbar.logo = None

			plot, legend = st.columns([5, 1])
			with legend:
				legend_options = {
					'top_left': 'Top Left',
					'top_right': 'Top Right',
					'bottom_left': 'Bottom Left',
					'bottom_right': 'Bottom Right'
				}
				legend_location = st.radio('Legend Location', options=['top_left', 'top_right', 'bottom_left', 'bottom_right'], format_func=lambda x: legend_options.get(x), index=1)
			p.legend.background_fill_alpha = 0.5
			p.legend.location = legend_location

			with plot:
				st.bokeh_chart(p, use_container_width=True)

		return

	except:
		st.warning("We're sorry, something went wrong.")
	
		return

if __name__ == '__main__':
	main()