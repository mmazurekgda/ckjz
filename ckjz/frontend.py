from nicegui import ui


# ui.add_head_html('''
# <style>
# @font-face {
#     font-family: 'Millunium_medium';
#     src: url('/static/millunium_medium.woff') format('woff');
# }
# </style>
# ''')

HTML_CODE = """
<style>
@font-face {
    font-family: 'Millunium_medium';
    src: url('/static/millunium_medium.woff') format('woff');
}
body { background-color: #182752; }
</style>
"""

TEXT_STYLE = 'font-family: Millunium_medium; color: #54b848;'
ROW_STYLE = 'margin: auto; width: 100%;'
COLUMN_STYLE = 'flex: 1; margin: auto; width: 100%;'


@ui.page('/')
def show():
    ui.add_head_html(HTML_CODE)
    with ui.row().style('margin: auto; margin-top: 2%; margin-bottom: 4%;'):
        ui.label('Czy kibel jest zajęty?').classes('text-9xl').style(TEXT_STYLE)
    with ui.row().style(ROW_STYLE):
        with ui.column().classes('items-center').style(COLUMN_STYLE):
            ui.label('Parter').classes('text-8xl').style(TEXT_STYLE)
        with ui.column().classes('items-center').style(COLUMN_STYLE):
            ui.label('1 piętro').classes('text-8xl').style(TEXT_STYLE)
    with ui.row().style(ROW_STYLE):
        with ui.column().classes('items-center').style(COLUMN_STYLE):
            ui.image('/static/upstairs.svg').style("max-width: 90%;")
        with ui.column().classes('items-center').style(COLUMN_STYLE):
            ui.image('/static/downstairs.svg').style("max-width: 70%;")