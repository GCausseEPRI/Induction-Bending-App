import time

import streamlit as st
import pandas as pd
from bokeh.plotting import figure, Figure
from bokeh.models import LinearAxis, Range1d, DatetimeAxis, DatetimeTickFormatter

from branding import epri, icons # EPRI branding and style customizations

def main() -> None:
	# epri.init_page(page_title='Home', layout='wide')	

	st.title('Induction Bend App')

	df = pd.read_pickle('data/machine_file.pickle')
	df['bend time'] = pd.to_datetime(df['bend time'])
	st.header('Machine File Data')
	st.write(df.head(100))
	

	x_column = st.selectbox(
		label='Select a column to use as the X axis',
		options=df.columns
	)
	y_column_left = st.multiselect(
		label='Select columns to attach to the left Y axis',
		options=df.columns,
	)
	y_column_right = st.multiselect(
		label='Select columns to attach to the right Y axis',
		options=df.columns,
	)

	if not y_column_left and not y_column_right:
		st.warning('Please choose at least 1 column for either Y axis to plot')
		return
	
	try:
		if len(y_column_left) > 0:
			left_label = y_column_left[0]
		else:
			left_label = ''
		if len(y_column_left) > 1:
			for column in y_column_left[1:]:
				left_label += ', ' + column
				
		p = figure(
			x_axis_label=x_column,
			y_axis_label=left_label,
			aspect_ratio=(17.5 / 8)
		)

		if pd.api.types.is_datetime64_any_dtype(df[x_column]):
			p.xaxis.formatter = DatetimeTickFormatter()

		for column in y_column_left:
			p.line(
				df[x_column],
				df[column]
			)
		
		if len(y_column_right) > 0:
			right_min = df[y_column_right[0]].min()
			right_max = df[y_column_right[0]].max()
			if len(y_column_right) > 1:
				for column in y_column_right:
					if df[column].min() < right_min:
						right_min = df[column].min()
					if df[column].max() > right_max:
						right_max = df[column].max()
			p.extra_y_ranges['secondary'] = Range1d(right_min, right_max)
			for column in y_column_right:
				p.line(
					df[x_column],
					df[column],
					y_range_name='secondary'
				)
			right_label = y_column_right[0]
			if len(y_column_right) > 1:
				for column in y_column_right[1:]:
					right_label += ', ' + column
			ax2 = LinearAxis(y_range_name='secondary', axis_label=right_label)
			p.add_layout(ax2, 'right')
		p.axis.axis_label_text_font_style = 'normal'
		p.toolbar.logo = None
		st.bokeh_chart(p, use_container_width=True)
	
		return

	except:
		st.warning("We're sorry, something went wrong.")
	
		return

if __name__ == '__main__':
	main()