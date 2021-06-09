from flask import Flask
from flask import Response
from flask import request
from justifytext import justify
import hyphen
import hyphen.textwrap2
import io
import json


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
            white-space: pre;
        }}
    </style>
    <defs>
        {gradient}
    </defs>
    <g fill="url(#Color)">
        {shapes}
    </g>
</svg>
'''


def gradient2svg(gradient):
    svg_file = io.StringIO()
    print('<linearGradient id="Color" gradientTransform="rotate(65)"'
          ' gradientUnits="userSpaceOnUse">',
          file=svg_file)
    for i, color in enumerate(gradient):
        percentage = i * 100 / (len(gradient) - 1)
        print(f'<stop offset="{percentage}%" stop-color="{color}" />',
              file=svg_file)
    print('</linearGradient>', file=svg_file)
    svg_file.seek(0)
    return svg_file.read()


with open('gradients.json') as f:
    gradients = json.load(f)
    gradients = [gradient2svg(grad["colors"]) for grad in gradients]


def select_gradient(str):
    return gradients[hash(str) % len(gradients)]


def hypenize(str, line_length, hyphenator=hyphen.Hyphenator('en_US')):
    return hyphen.textwrap2.fill(
        str,
        width=line_length,
        use_hyphenator=hyphenator,
    )


def str2svg_elements(str, font_size, line_length):
    hyphenized = hypenize(str, line_length)
    lines = justify(hyphenized, line_length)
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
    gradient = select_gradient(string)
    svg = template.format(
        width=width,
        height=(len(lines) + 1) * font_size,
        font_size=f'{font_size}px',
        gradient=gradient,
        shapes='\n'.join(lines),
    )
    return Response(svg, mimetype='image/svg+xml')


if __name__ == '__main__':
    app.run(host="0.0.0.0")
