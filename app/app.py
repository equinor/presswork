from flask import Flask
from flask import request
from justifytext import justify


app = Flask(__name__)


template=r"""
<svg width="{width}" height="{height}">

    <defs>
        <linearGradient id="Color" gradientTransform="rotate(65)" gradientUnits="userSpaceOnUse">
            <stop offset="0%" stop-color="#8A2387" />
            <stop offset="50%" stop-color="#E94057" />
            <stop offset="100%" stop-color="#F27121" />
        </linearGradient>
    </defs>

    <style>
        .line {{
            font-family: monospace;
            font-weight: bold;
            font-size: {font_size};
        }}
    </style>
    <g fill="url(#Color)">
        {shapes}
    </g>
</svg>
"""


def str2svg(str, font_size, line_length):
    print(str, font_size, line_length)
    lines = justify(str, line_length)
    lines = map(lambda ln: ln.replace(' ', '&nbsp;'), lines)
    return '\n'.join(
        f'<text y="{(i + 1) * font_size}px" class="line">{ln}</text>'
        for i, ln in enumerate(lines)
    )


@app.route('/epic/<string>')
def epic(string):
    args = request.args
    font_size = 24 if 'font_size' not in args else int(args['font_size'])
    line_length = 18 if 'line_length' not in args else int(args['line_length'])
    width = 271 if 'width' not in args else int(args['width'])
    height = 150 if 'height' not in args else int(args['height'])

    svg_text = str2svg(string, font_size, line_length)
    svg = template.format(
        width=width,
        height=height,
        font_size=font_size,
        shapes=svg_text,
    )
    return svg


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
