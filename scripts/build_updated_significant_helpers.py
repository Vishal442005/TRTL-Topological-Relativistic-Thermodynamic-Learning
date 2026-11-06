import os
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

import omml_equations as oeq

# --------------------------------------------------------------------------
# PATH CONFIGURATION
# --------------------------------------------------------------------------
BASE_DIR = "Updated_significant"
MANUSCRIPT_DIR = os.path.join(BASE_DIR, "manuscript")
COVER_DIR = os.path.join(BASE_DIR, "cover_letter")
HIGHLIGHTS_DIR = os.path.join(BASE_DIR, "highlights")
STATEMENTS_DIR = os.path.join(BASE_DIR, "statements")
FIGURES_DIR = os.path.join(BASE_DIR, "figures")
TABLES_DIR = os.path.join(BASE_DIR, "tables")
DATA_DIR = os.path.join(BASE_DIR, "data_and_results")

for d in [MANUSCRIPT_DIR, COVER_DIR, HIGHLIGHTS_DIR, STATEMENTS_DIR, FIGURES_DIR, TABLES_DIR, DATA_DIR]:
    os.makedirs(d, exist_ok=True)

# --------------------------------------------------------------------------
# XML UTILITIES FOR ACADEMIC STYLING
# --------------------------------------------------------------------------
def set_booktabs_borders(table):
    tblPr = table._element.xpath('w:tblPr')
    if tblPr:
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>\n'
            f'  <w:top w:val="single" w:sz="12" w:space="0" w:color="000000"/>\n'
            f'  <w:bottom w:val="single" w:sz="12" w:space="0" w:color="000000"/>\n'
            f'  <w:left w:val="none"/>\n'
            f'  <w:right w:val="none"/>\n'
            f'  <w:insideH w:val="none"/>\n'
            f'  <w:insideV w:val="none"/>\n'
            f'</w:tblBorders>'
        )
        tblPr[0].append(borders)

    header_row = table.rows[0]._element.xpath('w:trPr')
    if not header_row:
        header_trPr = parse_xml(f'<w:trPr {nsdecls("w")}/>')
        table.rows[0]._element.insert(0, header_trPr)
    rBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>\n'
        f'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>\n'
        f'</w:tcBorders>'
    )
    for cell in table.rows[0].cells:
        tcPr = cell._element.get_or_add_tcPr()
        tcPr.append(parse_xml(
            f'<w:tcBorders {nsdecls("w")}>\n'
            f'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>\n'
            f'</w:tcBorders>'
        ))

def style_academic_table(table):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_booktabs_borders(table)
    for r_i, row in enumerate(table.rows):
        trPr = row._element.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        if r_i == 0:
            trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
        for cell in row.cells:
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            tcPr = cell._element.get_or_add_tcPr()
            tcMar = parse_xml(
                f'<w:tcMar {nsdecls("w")}>\n'
                f'  <w:top w:w="80" w:type="dxa"/>\n'
                f'  <w:bottom w:w="80" w:type="dxa"/>\n'
                f'  <w:left w:w="120" w:type="dxa"/>\n'
                f'  <w:right w:w="120" w:type="dxa"/>\n'
                f'</w:tcMar>'
            )
            tcPr.append(tcMar)
            for paragraph in cell.paragraphs:
                paragraph.paragraph_format.space_before = Pt(2)
                paragraph.paragraph_format.space_after = Pt(2)
                paragraph.paragraph_format.line_spacing = 1.05
                for run in paragraph.runs:
                    run.font.name = "Calibri"
                    run.font.size = Pt(8.5)
                    run.font.color.rgb = RGBColor(0, 0, 0)
                    if r_i == 0:
                        run.font.bold = True

def add_table_caption(doc, tab_num, caption_text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r_lbl = p.add_run(f"Table {tab_num}: ")
    r_lbl.font.name = "Calibri"
    r_lbl.font.size = Pt(9.5)
    r_lbl.font.bold = True
    r_lbl.font.color.rgb = RGBColor(0, 0, 0)
    r_txt = p.add_run(caption_text)
    r_txt.font.name = "Calibri"
    r_txt.font.size = Pt(9.5)
    r_txt.font.italic = False
    r_txt.font.color.rgb = RGBColor(0, 0, 0)

def add_figure(doc, img_path, fig_num, title, description, width_in=5.8):
    if not os.path.exists(img_path):
        print(f"[WARNING] Image path not found: {img_path}")
        return
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(12)
    p_img.paragraph_format.space_after = Pt(4)
    p_img.paragraph_format.keep_with_next = True
    run_img = p_img.add_run()
    run_img.add_picture(img_path, width=Inches(width_in))

    p_cap = doc.add_paragraph()
    p_cap.paragraph_format.space_before = Pt(3)
    p_cap.paragraph_format.space_after = Pt(12)
    p_cap.paragraph_format.line_spacing = 1.15
    r_lbl = p_cap.add_run(f"Fig. {fig_num}. {title}. ")
    r_lbl.font.name = "Calibri"
    r_lbl.font.size = Pt(9.0)
    r_lbl.font.bold = True
    r_lbl.font.color.rgb = RGBColor(0, 0, 0)
    r_txt = p_cap.add_run(description)
    r_txt.font.name = "Calibri"
    r_txt.font.size = Pt(9.0)
    r_txt.font.color.rgb = RGBColor(0, 0, 0)

def add_theorem(doc, label, text, proof_text=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.left_indent = Inches(0.2)
    p.paragraph_format.right_indent = Inches(0.2)
    r_lbl = p.add_run(f"{label}. ")
    r_lbl.font.name = "Calibri"
    r_lbl.font.size = Pt(10)
    r_lbl.font.bold = True
    r_lbl.font.color.rgb = RGBColor(0, 0, 0)
    r_txt = p.add_run(text)
    r_txt.font.name = "Calibri"
    r_txt.font.size = Pt(10)
    r_txt.font.italic = True
    r_txt.font.color.rgb = RGBColor(0, 0, 0)

    if proof_text:
        pp = doc.add_paragraph()
        pp.paragraph_format.space_before = Pt(2)
        pp.paragraph_format.space_after = Pt(8)
        pp.paragraph_format.line_spacing = 1.15
        pp.paragraph_format.left_indent = Inches(0.2)
        pp.paragraph_format.right_indent = Inches(0.2)
        r_plbl = pp.add_run("Proof. ")
        r_plbl.font.name = "Calibri"
        r_plbl.font.size = Pt(9.5)
        r_plbl.font.bold = True
        r_plbl.font.color.rgb = RGBColor(0, 0, 0)
        r_ptxt = pp.add_run(proof_text)
        r_ptxt.font.name = "Calibri"
        r_ptxt.font.size = Pt(9.5)
        r_ptxt.font.color.rgb = RGBColor(0, 0, 0)
        r_qed = pp.add_run(" \u25a0")
        r_qed.font.bold = True

def add_omml_display_equation(doc, omml_str, eq_num):
    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(5.8)
    table.columns[1].width = Inches(0.7)
    cell_eq = table.cell(0, 0)
    cell_num = table.cell(0, 1)

    p_eq = cell_eq.paragraphs[0]
    p_eq.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_eq.paragraph_format.space_before = Pt(4)
    p_eq.paragraph_format.space_after = Pt(4)
    eq_elem = parse_xml(omml_str)
    p_eq._p.append(eq_elem)

    p_num = cell_num.paragraphs[0]
    p_num.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_num.paragraph_format.space_before = Pt(4)
    p_num.paragraph_format.space_after = Pt(4)
    r_num = p_num.add_run(f"({eq_num})")
    r_num.font.name = "Calibri"
    r_num.font.size = Pt(10)
    r_num.font.color.rgb = RGBColor(0, 0, 0)

    tblPr = table._element.xpath('w:tblPr')
    if tblPr:
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>\n'
            f'  <w:top w:val="none"/>\n'
            f'  <w:left w:val="none"/>\n'
            f'  <w:bottom w:val="none"/>\n'
            f'  <w:right w:val="none"/>\n'
            f'  <w:insideH w:val="none"/>\n'
            f'  <w:insideV w:val="none"/>\n'
            f'</w:tblBorders>'
        )
        tblPr[0].append(borders)

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(11.5)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

def add_heading_3(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(10.5)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

def add_body_p(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(10)
    r.font.color.rgb = RGBColor(0, 0, 0)
    return p

print("[OK] Helper functions configured.")
