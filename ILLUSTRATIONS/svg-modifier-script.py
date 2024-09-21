import sys
from bs4 import BeautifulSoup

def modify_svg(input_file, output_file):
    # Read the input SVG file
    with open(input_file, 'r') as file:
        svg_content = file.read()

    # Parse the SVG content
    soup = BeautifulSoup(svg_content, 'xml')

    # Find the svg element
    svg = soup.find('svg')

    # Remove the pan/zoom controls
    controls = svg.find(id="svg-pan-zoom-controls")
    if controls:
        controls.decompose()

    # Center the image
    # First, find the viewport
    viewport = svg.find(id=lambda x: x and x.startswith("viewport-"))
    if viewport:
        # Get the current transform
        transform = viewport.get('transform', '')
        
        # Extract the scale if it exists
        scale = 1
        if 'scale' in transform:
            scale = float(transform.split('scale(')[1].split(')')[0])
        
        # Set a new transform to center the image
        viewport['transform'] = f'translate(50%, 50%) scale({scale})'

    # Remove the style tag that sets display to none
    style_tag = svg.find('style', string=lambda text: text and 'display: none' in text)
    if style_tag:
        style_tag.decompose()

    # Write the modified SVG to the output file
    with open(output_file, 'w') as file:
        file.write(str(soup))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input_file.svg output_file.svg")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    modify_svg(input_file, output_file)
    print(f"Modified SVG saved to {output_file}")
