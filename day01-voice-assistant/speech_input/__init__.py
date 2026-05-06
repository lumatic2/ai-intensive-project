import pathlib
import streamlit.components.v1 as components

_func = components.declare_component(
    "speech_input",
    path=str(pathlib.Path(__file__).parent),
)

def speech_input(dark_mode: bool = True, key: str = None) -> str | None:
    return _func(dark_mode=dark_mode, key=key, default=None)
