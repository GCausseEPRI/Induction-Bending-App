from branding.load import load_str

# icons must be SVG with viewBox defined
_icons = {
    'mdiOpenInNew': load_str(r'./branding/icons/mdiOpenInNew.svg'),
}

def get(icon, style):
    '''
    Returns an SVG string containing the given icon with optional style attribute
    '''

    if style:
        return _icons[icon].replace('<svg', f'<svg style="{style}"', 1)
    else:
        return _icons[icon]
