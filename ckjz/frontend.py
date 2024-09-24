from nicegui import ui
from ckjz.constants import TOILET_TYPE, COLORS, FAINT_COLORS


JS_SCRIPT = f"""
<script>

const ws = new WebSocket("ws://localhost:3001/ws");

ws.onmessage = function(event) {{
    const status = JSON.parse(event.data);

    for (const [name, value] of Object.entries(status)) {{
        const shape = document.getElementById(`shape-${{name}}`);
        const polygon = document.getElementById(`polygon-${{name}}`);
        if (value === "unknown") {{
            shape.style.stroke = "{COLORS['unknown']}";
            polygon.style.fill = "{FAINT_COLORS['unknown']}";
        }} else if (value === "free") {{
            shape.style.stroke = "{COLORS['free']}";
            polygon.style.fill = "{FAINT_COLORS['free']}";
        }} else if (value === "occupied") {{
            shape.style.stroke = "{COLORS['occupied']}";
            polygon.style.fill = "{FAINT_COLORS['occupied']}";
        }} else {{
            console.error(`Unknown status: ${{value}}`);
        }}
    }}
}};
</script>
"""

HTML_CODE = (
    """
<style>
@font-face {
    font-family: 'Millunium_medium';
    src: url('/static/millunium_medium.woff') format('woff');
}
body { background-color: #182752; }
</style>
"""
    + JS_SCRIPT
)

TEXT_STYLE = "font-family: Millunium_medium; color: #54b848;"
ROW_STYLE = "margin: auto; width: 100%;"
COLUMN_STYLE = "flex: 1; margin: auto; width: 100%; margin-left: 2%; margin-right: 2%;"

ORIGIN = (-28, 0)
POLYGON_U_COORDINDATES = {
    TOILET_TYPE.UL2: [
        [0.0, 0.0],
        [56.0, 0.0],
        [56.0, 58.0],
        [43.0, 58.0],
        [43.0, 68.0],
        [0.0, 68.0],
    ],
    TOILET_TYPE.UM2: [[56.0, 0.0], [92.0, 0.0], [92.0, 58.0], [56.0, 58.0]],
    TOILET_TYPE.UL1: [[92.0, 0.0], [132.0, 0.0], [132.0, 58.0], [92.0, 58.0]],
    TOILET_TYPE.UM1: [
        [0.0, 68.0],
        [43.0, 68.0],
        [43.0, 58.0],
        [78.0, 58.0],
        [78.0, 86.0],
        [0.0, 86.0],
    ],
}
POLYGON_G_COORDINDATES = {
    TOILET_TYPE.GL: [[15.0, 3.0], [49.0, 3.0], [49.0, 56.0], [15.0, 56.0]],
    TOILET_TYPE.GM: [[49.0, 3.0], [83.0, 3.0], [83.0, 56.0], [49.0, 56.0]],
}
SHAPES_CENTROIDS = {
    TOILET_TYPE.UL2: [27.5, 25.0],
    TOILET_TYPE.UM2: [75.0, 26.0],
    TOILET_TYPE.UL1: [113.0, 25.0],
    TOILET_TYPE.UM1: [59.0, 70.0],
    TOILET_TYPE.GL: [32.5, 25.0],
    TOILET_TYPE.GM: [66.5, 25.0],
}


def u_coordinates_to_str(coordinates: list[list[float]]) -> str:
    return " ".join([f"{c[0] + ORIGIN[0]},{c[1]}" for c in coordinates])


def g_coordinates_to_str(coordinates: list[list[float]]) -> str:
    return " ".join([f"{c[0]},{c[1]}" for c in coordinates])


def get_shape(name: TOILET_TYPE) -> str:
    style = "fill: rgba(230, 230, 230, 0.0); stroke: green; stroke-width: 1.2;"
    x: float = SHAPES_CENTROIDS[name][0] + (
        ORIGIN[0] if name in POLYGON_U_COORDINDATES else 0
    )
    y: float = SHAPES_CENTROIDS[name][1]
    if name in [TOILET_TYPE.UL2, TOILET_TYPE.UL1, TOILET_TYPE.GL]:
        # draw a circle
        radius: float = 3
        return f'<circle id="shape-{name.value}" cx="{x}" cy="{y}" r="{radius}" style="{style}" />'
    else:
        distance: float = 2.5
        traingle_top = [x, y - distance]
        traingle_left = [x - distance, y + distance]
        traingle_right = [x + distance, y + distance]
        return (
            f'<polygon id="shape-{name.value}" '
            f'points="{traingle_top[0]},{traingle_top[1]} '
            f"{traingle_left[0]},{traingle_left[1]} "
            f'{traingle_right[0]},{traingle_right[1]}" '
            f'style="{style}" />'
        )


@ui.page("/")
def show():
    ui.add_head_html(HTML_CODE)
    with ui.row().style("margin: auto; margin-top: 2%; margin-bottom: 4%;"):
        ui.label("Is the kibel occupied?").classes("text-9xl").style(TEXT_STYLE)
    with ui.row().style(ROW_STYLE):
        with ui.column().classes("items-center").style(COLUMN_STYLE):
            ui.label("Ground floor").classes("text-8xl").style(TEXT_STYLE)
        with ui.column().classes("items-center").style(COLUMN_STYLE):
            ui.label("First floor").classes("text-8xl").style(TEXT_STYLE)

    with ui.row().style(ROW_STYLE):
        for image, coordinates_set in [
            ("/static/downstairs.svg", POLYGON_G_COORDINDATES),
            ("/static/upstairs.svg", POLYGON_U_COORDINDATES),
        ]:
            callback = (
                u_coordinates_to_str if "upstairs" in image else g_coordinates_to_str
            )
            with ui.column().classes("items-center").style(COLUMN_STYLE):
                ui.html(
                    f"""
                    <div style="position: relative; display: inline-block;">
                        <img src="{image}" style="max-width: 100%; position: relative; z-index: 1;">
                        <svg viewBox="0 0 100 100" width="100%" height="100%" style="position: absolute; top: 0; left: 0; z-index: -1;">

                        {
                            ''.join([
                                f'<polygon id="polygon-{name.value}" points="{callback(coordinates)}" '
                                f'style="fill: rgba(230, 230, 230, 0.1); stroke: green; stroke-width: 0;" />'
                                f'{get_shape(name)}'
                                for name, coordinates in coordinates_set.items()
                            ])
                        }
                        '</svg>'
                    </div>
                """
                )
    with ui.row().style("margin-left: auto; width: 10%; margin-top: 4%;"):
        ui.label("Legend").classes("text-5xl").style(TEXT_STYLE)
    for status, color in COLORS.items():
        with ui.row().style("margin-left: auto; width: 10%;"):
            ui.label(status).style(f"color: {color}; font-size: 2em;")
