"""
reportly element
"""
import os
import uuid

from .utils import file2data

app_prefix = "reportly"


class Table:
    """
    Parameters
    ----------
    dataframe : pandas.DataFrame
        dataframe is the data source
    section_idx: int
        xx

    Example
    --------
    df = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
        columns=['a', 'b', 'c'])
    tab01 = Table(df, section_idx=1, desc='tab01 description',
               comment='tab01 comment')
    tab01_html = tab01.to_html()
    """

    table_idx = {}  # 静态变量
    datatable_script = ""

    def __init__(
        self,
        dataframe,
        section_idx=1,
        desc="",
        comment="",
        export_button=True,
        header_prefix="Table",
        classes=["table", "table-bordered", "hover"],
        **kargs,
    ):
        self.table_id = str(uuid.uuid4())
        self.table_html = dataframe.to_html(
            table_id=self.table_id, classes=classes, **kargs
        )
        self.table_desc = desc
        self.export_button = export_button
        self.table_comment = comment
        self.header_prefix = header_prefix
        self.section_idx = section_idx
        if section_idx not in Table.table_idx:
            Table.table_idx[section_idx] = 1
        Table.table_idx[section_idx] += 1
        Table.datatable_script += self.js_script()

    def __repr__(self):
        return self.get_header()

    def get_header(self):
        # section_idx = self.section_idx
        return f"{self.header_prefix} {self.section_idx}.{Table.table_idx[self.section_idx]} {self.table_desc}"

    def js_script(self):
        table_id = self.table_id
        if self.export_button:
            script = (
                """
    $('#%s').DataTable( {
        dom: 'Bfrtip',
        buttons: [
            'copyHtml5',
            'excelHtml5',
            'csvHtml5',
        ]
    });
            """
                % table_id
            )
        else:
            script = (
                """
$('#%s').DataTable( {});
            """
                % table_id
            )
        return script

    def to_html_custom(self):
        """header + table + comment"""
        header = self.get_header()
        table = self.table_html
        table_comment = self.table_comment
        if table_comment:
            table_comment = (
                f"""<p class='{app_prefix}_table_comment'> {table_comment} </p>"""
            )
        else:
            table_comment = ""

        table_html = f"""
<div class="{app_prefix}_table">
    <p class='reportly_table_header'>{header}</p>
    {table}
    {table_comment}
</div>
"""
        return table_html

    def to_html_bootstrap(self):
        """
        bootstrap
        """
        header = self.get_header()
        table = self.table_html
        table_comment = self.table_comment
        if table_comment:
            table_comment = f"""<div class="panel-footer {app_prefix}_table_comment">{table_comment}</div> """
        else:
            table_comment = ""

        table_html = f"""
<div class="{app_prefix}_table">
  <div class="panel panel-default">
    <div class="panel-heading">
      <p class='{app_prefix}_table_header panel-title'>{header}</p>
    </div>
    <div class="panel-body">
      {table}
    </div>
    {table_comment}
 </div>
</div>
        """
        return table_html

    def to_html(self):
        return self.to_html_bootstrap()

    def to_datatable_script():

        table_jscript = (
            """
    <script>
    function renderTable(){
     %s
     }
    if (document.readyState === "complete") {
      renderTable()
    } else {
      $(document).ready(renderTable);
    }

    </script>
    """
            % Table.datatable_script
        )
        return table_jscript


class Figure:
    figure_idx = {}  # 静态变量
    plotly_script = ""

    def __init__(self, fig, section_idx=1, desc="", legned_prefix="Figure"):

        self.figure_id = str(uuid.uuid4())
        self.desc = desc
        self.section_idx = section_idx
        self.fig = fig

        self.legned_prefix = legned_prefix

        if section_idx not in Figure.figure_idx:
            Figure.figure_idx[section_idx] = 1
        Figure.figure_idx[section_idx] += 1

    def plotly_js_script(self):
        self.plotly_json = self.fig.to_json()
        script = f"""
        <script>
        data={self.plotly_json}
        Plotly.newPlot('{self.figure_id}', data['data'], data['layout']);
         </script>
        """
        return script

    def get_legend(self):
        # section_idx = self.section_idx
        return f"{self.legned_prefix} {self.section_idx}.{Figure.figure_idx[self.section_idx]} {self.desc}"

    def plotly_to_html(self):
        """plot + figure legend"""
        legend = self.get_legend()
        #         html = f"""
        # <div class="{app_prefix}_figure">
        #     <div id='{self.figure_id}'></div>

        # </div>
        # """
        html = f"""
<div class="{app_prefix}_figure">
  <div class="panel panel-default">

    <div class="panel-body">
      <div id='{self.figure_id}'></div>
    </div>
      <div class="panel-footer {app_prefix}_figure_legend"><p>{legend}</p></div>

 </div>
 {self.plotly_js_script()}
</div>
"""
        return html

    def image_to_html(self):

        _, file_ext = self.fig.rsplit(".", 2)
        if file_ext not in ["gif", "png", "jpg", "jpeg"]:
            raise TypeError("fig file must be the one of gif, png, jpg, jpeg")
        img_data = file2data(self.fig)

        legend = self.get_legend()
        # legend = f"""<p class='reportly_figure_legend'><p>{legend}</p></p>"""

        #         html = f"""
        #         <div class="{app_prefix}_figure">
        #          <img src="data:image/{file_ext};base64,{img_data}" class="img-fluid">
        #           {legend}
        # </div>
        #         """
        html = f"""
<div class="{app_prefix}_figure">
  <div class="panel panel-default">

    <div class="panel-body">
      <img src="data:image/{file_ext};base64,{img_data}" class="img-fluid">
    </div>
      <div class="panel-footer {app_prefix}_figure_legend">{legend}</div>
 </div>
</div>
"""
        return html

    def to_html(self):
        import plotly

        if isinstance(self.fig, plotly.graph_objs._figure.Figure):
            return self.plotly_to_html()
        elif isinstance(self.fig, str) and os.path.exists(self.fig):
            return self.image_to_html()
        else:
            raise TypeError(
                "fig must be plotly.graph_objs._figure.Figure or image file"
            )
