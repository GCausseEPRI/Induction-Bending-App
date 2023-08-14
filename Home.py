import streamlit as st

from branding import epri, icons # EPRI branding and style customizations

def main() -> None:
	epri.init_page(page_title='Home', layout='wide')	

	st.title('Welcome to the Induction Bend App!')
	st.image('images/mapping.png')
	return

if __name__ == '__main__':
	main()