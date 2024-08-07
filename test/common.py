import os
import unittest

from src.parser import Parser
from src.builder import Builder


class YAMscgenTestCommon(unittest.TestCase):
    def generate_img(self, input_txt):
        this_dir_path = os.path.dirname(os.path.realpath(__file__))
        test_name = self.id().split('.')[-1]
        test_path = os.path.join(this_dir_path, "test_svgs")
        if not os.path.exists(test_path):
            os.makedirs(test_path)
        file_path = os.path.join(test_path, test_name)
        builder = Builder(Parser(input_txt))
        images = builder.generate()
        if len(images) > 1:
            for i, image in enumerate(images):
                with open(f"{file_path}-{i}.svg", "wb+") as f:
                    f.write(image)
        else:
            with open(f"{file_path}.svg", "wb+") as f:
                f.write(images[0])
