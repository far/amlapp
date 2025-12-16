import os
import tempfile

from fpdf import FPDF
from fpdf.enums import XPos, YPos

reports_dir: str | None = None


def init_reports_dir() -> str:
    global reports_dir
    if reports_dir is None:
        reports_dir = tempfile.mkdtemp(prefix='aml_reports_')
    return reports_dir


def get_reports_dir() -> str | None:
    return reports_dir


def generate_report(report_data: dict) -> None:
    if reports_dir is None:
        raise RuntimeError('Reports directory not initialized')

    file_name = report_data.get('file_name', 'report.pdf')
    file_path = os.path.join(reports_dir, f'{file_name}.pdf')

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Helvetica', size=12)

    for key, value in report_data.items():
        if key != 'file_name':
            pdf.cell(
                0, 10, f'{key}: {value}', new_x=XPos.LMARGIN, new_y=YPos.NEXT
            )

    pdf.output(file_path)
