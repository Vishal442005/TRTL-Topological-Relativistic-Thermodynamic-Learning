import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

import omml_equations as oeq

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

def add_omml_display_equation(doc, math_xml, eq_number=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    omml = (
        f'<m:oMathPara xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">'
        f'<m:oMath>{math_xml}</m:oMath>'
        f'</m:oMathPara>'
    )
    p._p.append(parse_xml(omml))

    if eq_number:
        r_num = p.add_run(f"    ({eq_number})")
        r_num.font.name = "Calibri"
        r_num.font.size = Pt(10)
        r_num.font.color.rgb = RGBColor(0, 0, 0)

def eq_wave_energy_xml():
    return (
        '<m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>E</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>c</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t>(</m:t></m:r><m:r><m:rPr><m:sty m:val="b"/><m:scr m:val="it"/></m:rPr><m:t>x</m:t></m:r><m:r><m:t>) = </m:t></m:r>'
        '<m:r><m:rPr><m:nor/></m:rPr><m:t>max</m:t></m:r>'
        '<m:d><m:e><m:r><m:t>0, </m:t></m:r>'
        '<m:sSup><m:e><m:d><m:dPr><m:begChr m:val="|"/><m:endChr m:val="|"/></m:dPr><m:e>'
        '<m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>&#x03A8;</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>c</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t>(</m:t></m:r><m:r><m:rPr><m:sty m:val="b"/><m:scr m:val="it"/></m:rPr><m:t>x</m:t></m:r><m:r><m:t>)</m:t></m:r>'
        '</m:e></m:d></m:e><m:sup><m:r><m:t>2</m:t></m:r></m:sup></m:sSup>'
        '<m:r><m:t> &#x2212; </m:t></m:r>'
        '<m:f><m:num><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>&#x03BA;</m:t></m:r></m:num><m:den><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>C</m:t></m:r><m:r><m:t>&#x2212;1</m:t></m:r></m:den></m:f>'
        '<m:nary><m:naryPr><m:chr m:val="&#x2211;"/><m:limLoc m:val="undOvr"/></m:naryPr>'
        '<m:sub><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>c</m:t></m:r><m:r><m:t>&#x2032;&#x2260;</m:t></m:r><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>c</m:t></m:r></m:sub><m:sup/>'
        '<m:e><m:sSup><m:e><m:d><m:dPr><m:begChr m:val="|"/><m:endChr m:val="|"/></m:dPr><m:e>'
        '<m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>&#x03A8;</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>c</m:t></m:r><m:r><m:t>&#x2032;</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t>(</m:t></m:r><m:r><m:rPr><m:sty m:val="b"/><m:scr m:val="it"/></m:rPr><m:t>x</m:t></m:r><m:r><m:t>)</m:t></m:r>'
        '</m:e></m:d></m:e><m:sup><m:r><m:t>2</m:t></m:r></m:sup></m:sSup></m:e></m:nary>'
        '</m:e></m:d>'
        '<m:r><m:t> &#x22C5; </m:t></m:r>'
        '<m:sSub><m:e><m:r><m:rPr><m:sty m:val="b"/><m:scr m:val="it"/></m:rPr><m:t>1</m:t></m:r></m:e><m:sub><m:d><m:e><m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>d</m:t></m:r></m:e><m:sub><m:r><m:t>min</m:t></m:r></m:sub></m:sSub><m:r><m:t>&#x2264;</m:t></m:r><m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>R</m:t></m:r></m:e><m:sub><m:r><m:t>cut</m:t></m:r></m:sub></m:sSub></m:e></m:d></m:sub></m:sSub>'
    )

def eq_consensus_decision_xml():
    return (
        '<m:acc><m:accPr><m:chr m:val="&#x0302;"/></m:accPr><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>y</m:t></m:r></m:e></m:acc>'
        '<m:r><m:t>(</m:t></m:r><m:r><m:rPr><m:sty m:val="b"/><m:scr m:val="it"/></m:rPr><m:t>x</m:t></m:r><m:r><m:t>) = </m:t></m:r>'
        '<m:undOvr><m:undOvrPr><m:pos m:val="und"/></m:undOvrPr><m:e><m:r><m:rPr><m:nor/></m:rPr><m:t>argmax</m:t></m:r></m:e>'
        '<m:sub><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>k</m:t></m:r><m:r><m:t>&#x2208;{1,&#x2026;,</m:t></m:r><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>K</m:t></m:r><m:r><m:t>}</m:t></m:r></m:sub></m:undOvr>'
        '<m:r><m:t> </m:t></m:r>'
        '<m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>P</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>k</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t>(</m:t></m:r><m:r><m:rPr><m:sty m:val="b"/><m:scr m:val="it"/></m:rPr><m:t>x</m:t></m:r><m:r><m:t>)</m:t></m:r>'
    )

def eq_total_loss_xml():
    return (
        '<m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>L</m:t></m:r></m:e><m:sub><m:r><m:t>total</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t> = </m:t></m:r>'
        '<m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>L</m:t></m:r></m:e><m:sub><m:r><m:t>CE</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t>(</m:t></m:r><m:acc><m:accPr><m:chr m:val="&#x0302;"/></m:accPr><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>p</m:t></m:r></m:e></m:acc><m:r><m:t>, y) + </m:t></m:r>'
        '<m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>&#x03BB;</m:t></m:r></m:e><m:sub><m:r><m:t>1</m:t></m:r></m:sub></m:sSub>'
        '<m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>L</m:t></m:r></m:e><m:sub><m:r><m:t>entropy</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t>(</m:t></m:r><m:r><m:rPr><m:sty m:val="b"/><m:scr m:val="it"/></m:rPr><m:t>W</m:t></m:r><m:r><m:t>) + </m:t></m:r>'
        '<m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>&#x03BB;</m:t></m:r></m:e><m:sub><m:r><m:t>2</m:t></m:r></m:sub></m:sSub>'
        '<m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>L</m:t></m:r></m:e><m:sub><m:r><m:t>sparse</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t>(</m:t></m:r><m:r><m:rPr><m:sty m:val="b"/><m:scr m:val="it"/></m:rPr><m:t>W</m:t></m:r><m:r><m:t>) + </m:t></m:r>'
        '<m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>&#x03BB;</m:t></m:r></m:e><m:sub><m:r><m:t>3</m:t></m:r></m:sub></m:sSub>'
        '<m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>L</m:t></m:r></m:e><m:sub><m:r><m:t>barrier</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t>(</m:t></m:r><m:r><m:rPr><m:sty m:val="b"/><m:scr m:val="it"/></m:rPr><m:t>W</m:t></m:r><m:r><m:t>, &#x03A8;)</m:t></m:r>'
    )

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
