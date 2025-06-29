import gradio as gr

def say_hello(name):
    return f"Hello {name}!"

demo = gr.Interface(fn=say_hello, inputs="text", outputs="text")
demo.launch()
