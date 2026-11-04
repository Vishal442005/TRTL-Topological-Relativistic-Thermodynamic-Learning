from docx import Document
from docx.oxml import parse_xml

doc = Document()
p = doc.add_paragraph()
omml = '''<m:oMathPara xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:oMath>
    <m:acc>
      <m:accPr><m:chr m:val="&#x0302;"/></m:accPr>
      <m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>y</m:t></m:r></m:e>
    </m:acc>
    <m:r><m:t>(</m:t></m:r>
    <m:r><m:rPr><m:sty m:val="b"/><m:scr m:val="it"/></m:rPr><m:t>x</m:t></m:r>
    <m:r><m:t>) = </m:t></m:r>
    <m:sSub>
      <m:e><m:r><m:rPr><m:nor/></m:rPr><m:t>argmax</m:t></m:r></m:e>
      <m:sub>
        <m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>k</m:t></m:r>
        <m:r><m:t>&#x2208;{1,&#x2026;,</m:t></m:r>
        <m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>K</m:t></m:r>
        <m:r><m:t>}</m:t></m:r>
      </m:sub>
    </m:sSub>
    <m:r><m:t> </m:t></m:r>
    <m:sSub>
      <m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>P</m:t></m:r></m:e>
      <m:sub><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>k</m:t></m:r></m:sub>
    </m:sSub>
    <m:r><m:t>(</m:t></m:r>
    <m:r><m:rPr><m:sty m:val="b"/><m:scr m:val="it"/></m:rPr><m:t>x</m:t></m:r>
    <m:r><m:t>)</m:t></m:r>
  </m:oMath>
</m:oMathPara>'''
p._p.append(parse_xml(omml))
doc.save('test_omml.docx')
print('Successfully saved test_omml.docx!')
