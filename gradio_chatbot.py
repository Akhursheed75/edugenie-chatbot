import gradio as gr
from groq import Groq
import logging

# Logging setup
logging.basicConfig(filename="chatbot.log", level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Groq API Client
import os
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
chat_history = []

# Chatbot logic
def chatbot(message, history):
    global chat_history
    logging.debug(f"Received message: {message}")
    chat_history.append({"role": "user", "content": message})
    try:
        messages = [{"role": "system", "content": "You are EduGenie, created by xAI. Respond helpfully and truthfully."}] + chat_history
        logging.debug("Sending request to Groq API...")
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama3-8b-8192",
        )
        response = chat_completion.choices[0].message.content
        logging.debug(f"Received response: {response}")
        chat_history.append({"role": "assistant", "content": response})
        history.append((message, response))
        return history, ""
    except Exception as e:
        logging.error(f"Error in Groq API call: {str(e)}")
        return history, f"Error: {str(e)}"

# Gradio App
with gr.Blocks(title="EduGenie", css="""
    body { background-color: #000000; color: white; }
    #chatbox { background-color: #111111; border-radius: 8px; }
    .gr-textbox textarea { background-color: #222; color: white; border: 1px solid #444; }
    .gr-button { background-color: #333 !important; color: white !important; border: none; }
    .gr-button:hover { background-color: #444 !important; }
""") as demo:

    # Custom Header with Black Text Inside White Box
    with gr.Row():
        with gr.Column():
            gr.HTML(
                """
                <div style='text-align: center; margin-bottom: 20px;'>
                    <h1 style='display: inline-block; background-color: white; color: black; font-weight: bold; padding: 10px 25px; border-radius: 12px;'>
                        🧠 EduGenie
                    </h1>
                    <p style='color: white; font-size: 16px; margin-top: 10px;'>
                        Your AI assistant by xAI — ask anything, learn everything!
                    </p>
                </div>
                """
            )

    # Chat UI
    with gr.Row():
        with gr.Column(scale=1, min_width=500):
            chatbot_ui = gr.Chatbot(height=400, show_copy_button=True, label="Chat History", elem_id="chatbox")
            msg = gr.Textbox(placeholder="💬 Ask something...", show_label=False)
            with gr.Row():
                send_btn = gr.Button("🚀 Send")
                clear = gr.Button("🧹 Clear Chat", variant="secondary")

    # Events
    msg.submit(chatbot, [msg, chatbot_ui], [chatbot_ui, msg])
    send_btn.click(chatbot, [msg, chatbot_ui], [chatbot_ui, msg])
    clear.click(lambda: ([], ""), None, [chatbot_ui, msg])

logging.debug("Launching Gradio app...")
demo.launch()
