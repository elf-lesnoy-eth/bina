import gradio as gr

html_code = """
<iframe src="https://www.openstreetmap.org" width="100%" height="500"></iframe>
"""

gr.Interface(lambda: html_code, inputs=[], outputs="html").launch(share=True)