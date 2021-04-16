from flask import Flask
from flask import Response
from flask import request
from justifytext import justify


app = Flask(__name__)


template=r'''<?xml version="1.0" encoding="utf-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
  "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="{width}" height="{height}" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink= "http://www.w3.org/1999/xlink">
    <style>
        .line {{
            font-family: monospace;
            font-weight: bold;
            font-size: {font_size};
        }}
    </style>
    <defs>
        <linearGradient id="Color" gradientTransform="rotate(65)" gradientUnits="userSpaceOnUse">
            <stop offset="0%" stop-color="#8A2387" />
            <stop offset="50%" stop-color="#E94057" />
            <stop offset="100%" stop-color="#F27121" />
        </linearGradient>
    </defs>
    <g fill="url(#Color)">
        {shapes}
    </g>
</svg>
'''


def str2svg_elements(str, font_size, line_length):
    lines = justify(str, line_length)
    return [
        f'<text y="{(i + 1) * font_size}px" class="line">{ln}</text>'
        for i, ln in enumerate(lines)
    ]


@app.route('/epic/<string>')
def epic(string):
    args = request.args
    font_size = 24 if 'font_size' not in args else int(args['font_size'])
    line_length = 18 if 'line_length' not in args else int(args['line_length'])
    width = 271 if 'width' not in args else int(args['width'])

    lines = str2svg_elements(string, font_size, line_length)
    svg = template.format(
        width=width,
        height=(len(lines) + 1) * font_size,
        font_size=f'{font_size}px',
        shapes='\n'.join(lines),
    )
    return Response(svg, mimetype='image/svg+xml')


if __name__ == '__main__':
    app.run(host="0.0.0.0")
