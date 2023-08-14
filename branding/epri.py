# packages
import streamlit as st
import rcssmin as rc

# local modules
import app
from branding.load import load_css, load_base64

# file paths relative to the current working directory
icon_path = r'./branding/epri-icon-32px.png'
logo_path = r'./branding/epri-logo-color.svg'
epri_css_path  = r'./branding/epri-style.css'
more_css_path = r'./branding/more-style.css'

# preload custom CSS and additional CSS
css = load_css(epri_css_path) + load_css(more_css_path)

if app.show_logo:
    # preload logo as CSS background image (also see epri-style.css)
    css += rc.cssmin(f"""
        .stApp > header,
        .appview-container > [data-testid="stSidebar"] > :first-child {{
            background-image: url(data:image/svg+xml;base64,{load_base64(logo_path)});
        }}""")

# unicode representation of a quotation mark (")
css_double_quote = r'\000022'

if app.show_site_title_in_sidebar and app.site_title:
    # preload site title in sidebar as CSS content (also see epri-style.css)
    css += rc.cssmin(f"""
        .appview-container > [data-testid="stSidebar"] > :first-child::before {{
            content: "{app.site_title.replace('"', css_double_quote)}";
        }}""")

else:
    # no site title in sidebar
    # we must offset the sidebar's nav links container so it won't scroll over the logo
    css += rc.cssmin(f"""
        .appview-container > [data-testid="stSidebar"] > :first-child > [data-testid="stSidebarNav"] {{
            margin-top: 46px; /* 46px = header height that contains the logo */
        }}""")

def init_page(page_title='', layout='centered', initial_sidebar_state='auto'):
    '''
    Initializes a Streamlit page using EPRI branding and custom styles.

    `page_title` is an optional title for the page, which will be shown
    in browser tab along with the app's site_title and title_suffix

    `layout` specifies a Streamlit layout:
    - `"centered"` constrains main content to a fixed width
    - `"wide"` allows main content to expand across the entire screen

    `initial_sidebar_state` specifies initial visibility of the sidebar: 
    - `"auto"` hides the sidebar on small screens, otherwise shows it
    - `"expanded"` shows the sidebar, regardless of screen size
    - `"collapsed"` hides the sidebar, regardless of screen size
    '''

    if page_title and app.site_title:
        title = f'{page_title} | {app.site_title}'
    elif page_title:
        title = page_title
    else:
        title = app.site_title

    if title and app.title_suffix:
        title += f' | {app.title_suffix}'

    # set Streamlit's page config
    st.set_page_config(title, icon_path, layout, initial_sidebar_state)

    # load custom styles into an empty container
    # this will be hidden at the top of the page (see epri-style.css)
    customStyle = st.empty()
    customStyle.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
