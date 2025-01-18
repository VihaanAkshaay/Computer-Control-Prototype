'''
Supporting functions for the main script
'''


from PIL import Image
import io

def display_graph(graph):
    try:
        # Generate the PNG image bytes from the graph
        png_data = graph.get_graph().draw_mermaid_png()
        
        # Open the image from the byte stream
        img = Image.open(io.BytesIO(png_data))
        
        # Show the image using the default viewer
        img.show()
    except Exception as e:
        print("Failed to display graph:", e)

# Get list of local apps 

