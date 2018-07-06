import pytest
import os
import sys

current_path = os.path.dirname(os.path.realpath(__file__))
tohsaka_path = os.path.join(current_path, '..', 'tohsaka')

sys.path.insert(0, tohsaka_path)
