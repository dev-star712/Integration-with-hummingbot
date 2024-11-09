import time

import threading

from prompt_toolkit.application import Application
from prompt_toolkit.document import Document
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import SearchToolbar, TextArea

help_text = """
Type any expression (e.g. "4 + 4") followed by enter to execute.
Press Control-C to exit.
"""


def main():
    # The layout.
    search_field = SearchToolbar()  # For reverse search.

    output_field = TextArea(style="class:output-field", text=help_text)
    input_field = TextArea(
        height=1,
        prompt=">>> ",
        style="class:input-field",
        multiline=False,
        wrap_lines=False,
        search_field=search_field,
    )

    container = HSplit(
        [
            output_field,
            Window(height=1, char="-", style="class:line"),
            input_field,
            search_field,
        ]
    )

    # Attach accept handler to the input field. We do this by assigning the
    # handler to the `TextArea` that we created earlier. it is also possible to
    # pass it to the constructor of `TextArea`.
    # NOTE: It's better to assign an `accept_handler`, rather then adding a
    #       custom ENTER key binding. This will automatically reset the input
    #       field and add the strings to the history.
    def accept(buff):
        # Evaluate "calculator" expression.
        try:
            output = f"\n\nIn:  {input_field.text}\nOut: {eval(input_field.text)}"  # Don't do 'eval' in real code!
        except BaseException as e:
            output = f"\n\n{e}"
        new_text = output_field.text + output

        # Add text to output buffer.
        output_field.buffer.document = Document(
            text=new_text, cursor_position=22
        )

    input_field.accept_handler = accept

    # The key bindings.
    kb = KeyBindings()

    @kb.add("c-c")
    @kb.add("c-q")
    def _(event):
        "Pressing Ctrl-Q or Ctrl-C will exit the user interface."
        event.app.exit()

    # Style.
    style = Style(
        [
            ("output-field", "bg:#000044 #ffffff"),
            ("input-field", "bg:#000000 #ffffff"),
            ("line", "#004400"),
        ]
    )

    # Run application.
    application = Application(
        layout=Layout(container, focused_element=input_field),
        key_bindings=kb,
        style=style,
        mouse_support=True,
        full_screen=True,
    )

    application.run()



def StartDA():
    # for i in range(10):
    #     print("Hello, world!")
    # DACommand = StartDACommand()
    # DACommand.run()
    main()
        

def getData():
    ip_addr = "220.73.120.40"
    
class StartDACommand:
    
    def __init__(self):
        self.thread = threading.Thread(target = self.clock())
    
    def redraw(self):
        self.app.invalidate()
        
    def start_clock(self):
        self.thread.start()
        
    def clock(self):
        # result = prompt([("bg:#008800 #ffffff", f"{datetime.datetime.now().strftime('%H:%M:%S')}")], refresh_interval=0.5)
        # print(f"You said: {result}")
        while True:
            print("Hello, world")
            time.sleep(2)
    
    def run(self):
        main()