"""Main module."""
import os
import pathlib

import jinja2

from .elements import Table
from .utils import include_file


class Report:
    def __init__(self):
        # self.subtitle = "subtitle"
        self.title = ""
        self.version = ""
        self.subtitle = ""
        self.show_analysis_time = False
        self.creation_date = ""
        self.show_analysis_paths = "./"
        self.analysis_dir = []
        self.table_script = Table.to_datatable_script()
        sections = [
            {
                "name": "",
                "anchor": "",
                "description": "",
                "comment": "",
                "helptext": "",
                "content": "",
                "print_section": True,
            }
        ]

        self.modules_output = [
            {
                "sections": sections,
                "description": "",
                "comment": "",
                "anchor": "",
                "name": "",
                "content": "",
                "helptext": "",
            },
        ]

    def save(
        self,
        filename,
        config,
        template_dir=os.path.join(pathlib.Path(__file__).parents[1], "template"),
    ):
        self.table_script = Table.to_datatable_script()
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
        env.globals["include_file"] = include_file
        j_template = env.get_template("base.html")

        report_output = j_template.render(report=self, config=config)

        with open(filename, "w") as f:
            f.write(report_output)


class Configure:
    def __init__(self):
        self.custom_logo_url = None
        self.custom_logo = None
