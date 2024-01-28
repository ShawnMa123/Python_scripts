import loguru
import xml.dom.minidom
import os
import pathlib


class DemoClass:
    def __init__(self):
        print(f"enter demo class")

    def your_function(self, input_val):
        ret = str(type(input_val))
        return ret
