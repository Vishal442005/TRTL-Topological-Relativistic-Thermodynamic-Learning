"""
OMML Equation Builder for TRTL Manuscript
Generates fully valid Office Math Markup Language XML for all paper equations.
"""

def omml_wrap(math_xml, eq_num=None):
    """Wraps math XML in an oMathPara with optional equation number."""
    if eq_num:
        # Standard Word scientific equation table or paragraph with right-aligned number
        return (
            f'<m:oMathPara xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">'
            f'<m:oMath>{math_xml}</m:oMath>'
            f'</m:oMathPara>'
        )
    else:
        return (
            f'<m:oMathPara xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">'
            f'<m:oMath>{math_xml}</m:oMath>'
            f'</m:oMathPara>'
        )

# 1. Relativistic Metric Dilatation: d_{i,rel}(x) = ||x - x_i||_W * \gamma_i, \gamma_i = 1 / sqrt(1 - \beta (H_i / H_max)^2)
def eq_ramd():
    return (
        '<m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>d</m:t></m:r></m:e>'
        '<m:sub><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>i</m:t></m:r><m:r><m:t>,rel</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t>(</m:t></m:r><m:r><m:rPr><m:sty m:val="b"/><m:scr m:val="it"/></m:rPr><m:t>x</m:t></m:r><m:r><m:t>) = </m:t></m:r>'
        '<m:d><m:dPr><m:begChr m:val="&#x2225;"/><m:endChr m:val="&#x2225;"/></m:dPr><m:e>'
        '<m:r><m:rPr><m:sty m:val="b"/><m:scr m:val="it"/></m:rPr><m:t>x</m:t></m:r>'
        '<m:r><m:t> &#x2212; </m:t></m:r>'
        '<m:sSub><m:e><m:r><m:rPr><m:sty m:val="b"/><m:scr m:val="it"/></m:rPr><m:t>x</m:t></m:r></m:e>'
        '<m:sub><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>i</m:t></m:r></m:sub></m:sSub>'
        '</m:e></m:d>'
        '<m:sSub><m:e><m:r><m:t></m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="b"/><m:scr m:val="it"/></m:rPr><m:t>W</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t> &#x22C5; </m:t></m:r>'
        '<m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>&#x03B3;</m:t></m:r></m:e>'
        '<m:sub><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>i</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t>,     </m:t></m:r>'
        '<m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>&#x03B3;</m:t></m:r></m:e>'
        '<m:sub><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>i</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t> = </m:t></m:r>'
        '<m:f><m:num><m:r><m:t>1</m:t></m:r></m:num><m:den>'
        '<m:rad><m:radPr><m:degHide m:val="on"/></m:radPr><m:deg/><m:e>'
        '<m:r><m:t>1 &#x2212; </m:t></m:r>'
        '<m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>&#x03B2;</m:t></m:r>'
        '<m:sSup><m:e><m:d><m:e>'
        '<m:f><m:num><m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>H</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>i</m:t></m:r></m:sub></m:sSub></m:num>'
        '<m:den><m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>H</m:t></m:r></m:e><m:sub><m:r><m:t>max</m:t></m:r></m:sub></m:sSub></m:den></m:f>'
        '</m:e></m:d></m:e><m:sup><m:r><m:t>2</m:t></m:r></m:sup></m:sSup>'
        '</m:e></m:rad>'
        '</m:den></m:f>'
    )

# 2. Wavefield Superposition: Psi_c(x) = sum_{i in C_c} A_i exp(-1/2 mu d_{i,rel}^2) exp(i k d_{i,rel})
def eq_twil():
    return (
        '<m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>&#x03A8;</m:t></m:r></m:e>'
        '<m:sub><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>c</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t>(</m:t></m:r><m:r><m:rPr><m:sty m:val="b"/><m:scr m:val="it"/></m:rPr><m:t>x</m:t></m:r><m:r><m:t>) = </m:t></m:r>'
        '<m:nary><m:naryPr><m:chr m:val="&#x2211;"/><m:limLoc m:val="undOvr"/></m:naryPr>'
        '<m:sub><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>i</m:t></m:r><m:r><m:t>&#x2208;</m:t></m:r><m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>C</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>c</m:t></m:r></m:sub></m:sSub></m:sub>'
        '<m:sup/>'
        '<m:e>'
        '<m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>A</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>i</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t> exp</m:t></m:r>'
        '<m:d><m:e>'
        '<m:r><m:t>&#x2212;</m:t></m:r>'
        '<m:f><m:num><m:r><m:t>1</m:t></m:r></m:num><m:den><m:r><m:t>2</m:t></m:r></m:den></m:f>'
        '<m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>&#x03BC;</m:t></m:r>'
        '<m:sSup><m:e><m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>d</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>i</m:t></m:r><m:r><m:t>,rel</m:t></m:r></m:sub></m:sSub></m:e><m:sup><m:r><m:t>2</m:t></m:r></m:sup></m:sSup>'
        '</m:e></m:d>'
        '<m:r><m:t> exp</m:t></m:r>'
        '<m:d><m:e>'
        '<m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>i k d</m:t></m:r>'
        '<m:sSub><m:e><m:r><m:t></m:t></m:r></m:e><m:sub><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>i</m:t></m:r><m:r><m:t>,rel</m:t></m:r></m:sub></m:sSub>'
        '</m:e></m:d>'
        '</m:e></m:nary>'
    )

# 3. Decision Rule with argmax: y_hat(x) = argmax_{c in {1,...,C}} S_c(x)
def eq_argmax_decision():
    return (
        '<m:acc><m:accPr><m:chr m:val="&#x0302;"/></m:accPr><m:e>'
        '<m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>y</m:t></m:r></m:e></m:acc>'
        '<m:r><m:t>(</m:t></m:r><m:r><m:rPr><m:sty m:val="b"/><m:scr m:val="it"/></m:rPr><m:t>x</m:t></m:r><m:r><m:t>) = </m:t></m:r>'
        '<m:undOvr>'
        '<m:undOvrPr><m:pos m:val="und"/></m:undOvrPr>'
        '<m:e><m:r><m:rPr><m:nor/></m:rPr><m:t>argmax</m:t></m:r></m:e>'
        '<m:sub>'
        '<m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>c</m:t></m:r>'
        '<m:r><m:t>&#x2208;{1,&#x2026;,</m:t></m:r>'
        '<m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>C</m:t></m:r>'
        '<m:r><m:t>}</m:t></m:r>'
        '</m:sub>'
        '</m:undOvr>'
        '<m:r><m:t> </m:t></m:r>'
        '<m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>S</m:t></m:r></m:e>'
        '<m:sub><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>c</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t>(</m:t></m:r><m:r><m:rPr><m:sty m:val="b"/><m:scr m:val="it"/></m:rPr><m:t>x</m:t></m:r><m:r><m:t>)</m:t></m:r>'
    )

# 4. Ginzburg-Landau Gradient Flow: dS_c / dt = - (T - T_c) S_c - b S_c^3 + h_c - \xi S_c sum_{c' != c} S_{c'}^2
def eq_ginzburg_landau():
    return (
        '<m:f><m:num><m:r><m:t>&#x2202;</m:t></m:r><m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>S</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>c</m:t></m:r></m:sub></m:sSub></m:num>'
        '<m:den><m:r><m:t>&#x2202;</m:t></m:r><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>t</m:t></m:r></m:den></m:f>'
        '<m:r><m:t> = &#x2212;</m:t></m:r>'
        '<m:d><m:e>'
        '<m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>T</m:t></m:r>'
        '<m:r><m:t> &#x2212; </m:t></m:r>'
        '<m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>T</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>c</m:t></m:r></m:sub></m:sSub>'
        '</m:e></m:d>'
        '<m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>S</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>c</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t> &#x2212; </m:t></m:r>'
        '<m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>b</m:t></m:r>'
        '<m:sSup><m:e><m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>S</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>c</m:t></m:r></m:sub></m:sSub></m:e><m:sup><m:r><m:t>3</m:t></m:r></m:sup></m:sSup>'
        '<m:r><m:t> + </m:t></m:r>'
        '<m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>h</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>c</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t> &#x2212; </m:t></m:r>'
        '<m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>&#x03BE; S</m:t></m:r>'
        '<m:sSub><m:e><m:r><m:t></m:t></m:r></m:e><m:sub><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>c</m:t></m:r></m:sub></m:sSub>'
        '<m:nary><m:naryPr><m:chr m:val="&#x2211;"/><m:limLoc m:val="undOvr"/></m:naryPr>'
        '<m:sub><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>c</m:t></m:r><m:r><m:t>&#x2032;&#x2260;</m:t></m:r><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>c</m:t></m:r></m:sub>'
        '<m:sup/>'
        '<m:e>'
        '<m:sSup><m:e><m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>S</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>c</m:t></m:r><m:r><m:t>&#x2032;</m:t></m:r></m:sub></m:sSub></m:e><m:sup><m:r><m:t>2</m:t></m:r></m:sup></m:sSup>'
        '</m:e></m:nary>'
    )

# 5. Certified Invariance Radius: r_cert(x_0) = Delta S(x_0) / (2 L_S)
def eq_certified_radius():
    return (
        '<m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>r</m:t></m:r></m:e><m:sub><m:r><m:t>cert</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t>(</m:t></m:r><m:sSub><m:e><m:r><m:rPr><m:sty m:val="b"/><m:scr m:val="it"/></m:rPr><m:t>x</m:t></m:r></m:e><m:sub><m:r><m:t>0</m:t></m:r></m:sub></m:sSub><m:r><m:t>) = </m:t></m:r>'
        '<m:f><m:num><m:r><m:t>&#x0394;</m:t></m:r><m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>S</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>c</m:t></m:r><m:r><m:t>*</m:t></m:r></m:sub></m:sSub><m:r><m:t>(</m:t></m:r><m:sSub><m:e><m:r><m:rPr><m:sty m:val="b"/><m:scr m:val="it"/></m:rPr><m:t>x</m:t></m:r></m:e><m:sub><m:r><m:t>0</m:t></m:r></m:sub></m:sSub><m:r><m:t>)</m:t></m:r></m:num>'
        '<m:den><m:r><m:t>2 </m:t></m:r><m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>L</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>S</m:t></m:r></m:sub></m:sSub></m:den></m:f>'
        '<m:r><m:t>,     where </m:t></m:r>'
        '<m:r><m:t>&#x0394;</m:t></m:r><m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>S</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>c</m:t></m:r><m:r><m:t>*</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t> = </m:t></m:r>'
        '<m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>S</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>c</m:t></m:r><m:r><m:t>*</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t> &#x2212; </m:t></m:r>'
        '<m:undOvr>'
        '<m:undOvrPr><m:pos m:val="und"/></m:undOvrPr>'
        '<m:e><m:r><m:rPr><m:nor/></m:rPr><m:t>max</m:t></m:r></m:e>'
        '<m:sub><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>c</m:t></m:r><m:r><m:t>&#x2260;</m:t></m:r><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>c</m:t></m:r><m:r><m:t>*</m:t></m:r></m:sub>'
        '</m:undOvr>'
        '<m:r><m:t> </m:t></m:r>'
        '<m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>S</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>c</m:t></m:r></m:sub></m:sSub>'
    )

# 6. Counterfactual Recourse Velocity: dot{x}(t) = - W^{-1} \nabla_x F(S(x(t)), c_target) - \lambda (x(t) - x_orig)
def eq_recourse_velocity():
    return (
        '<m:acc><m:accPr><m:chr m:val="&#x02D9;"/></m:accPr><m:e>'
        '<m:r><m:rPr><m:sty m:val="b"/><m:scr m:val="it"/></m:rPr><m:t>x</m:t></m:r></m:e></m:acc>'
        '<m:r><m:t>(</m:t></m:r><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>t</m:t></m:r><m:r><m:t>) = &#x2212;</m:t></m:r>'
        '<m:sSup><m:e><m:r><m:rPr><m:sty m:val="b"/><m:scr m:val="it"/></m:rPr><m:t>W</m:t></m:r></m:e><m:sup><m:r><m:t>&#x2212;1</m:t></m:r></m:sup></m:sSup>'
        '<m:sSub><m:e><m:r><m:t>&#x2207;</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="b"/><m:scr m:val="it"/></m:rPr><m:t>x</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t> </m:t></m:r>'
        '<m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>&#x2131;</m:t></m:r>'
        '<m:d><m:e>'
        '<m:r><m:rPr><m:sty m:val="b"/><m:scr m:val="it"/></m:rPr><m:t>S</m:t></m:r><m:r><m:t>(</m:t></m:r><m:r><m:rPr><m:sty m:val="b"/><m:scr m:val="it"/></m:rPr><m:t>x</m:t></m:r><m:r><m:t>(</m:t></m:r><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>t</m:t></m:r><m:r><m:t>)), </m:t></m:r>'
        '<m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>c</m:t></m:r></m:e><m:sub><m:r><m:t>target</m:t></m:r></m:sub></m:sSub>'
        '</m:e></m:d>'
        '<m:r><m:t> &#x2212; </m:t></m:r>'
        '<m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>&#x03BB;</m:t></m:r>'
        '<m:d><m:e>'
        '<m:r><m:rPr><m:sty m:val="b"/><m:scr m:val="it"/></m:rPr><m:t>x</m:t></m:r><m:r><m:t>(</m:t></m:r><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>t</m:t></m:r><m:r><m:t>) &#x2212; </m:t></m:r>'
        '<m:sSub><m:e><m:r><m:rPr><m:sty m:val="b"/><m:scr m:val="it"/></m:rPr><m:t>x</m:t></m:r></m:e><m:sub><m:r><m:t>orig</m:t></m:r></m:sub></m:sSub>'
        '</m:e></m:d>'
    )

# 7. Wave Energy with Cutoff Support
def eq_wave_energy():
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

# 8. Dynamic Temperature Coupling: T(x) = T_0 + \Delta T / (1 + E_tot(x)/\sigma_E)
def eq_temperature_coupling():
    return (
        '<m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>T</m:t></m:r>'
        '<m:r><m:t>(</m:t></m:r><m:r><m:rPr><m:sty m:val="b"/><m:scr m:val="it"/></m:rPr><m:t>x</m:t></m:r><m:r><m:t>) = </m:t></m:r>'
        '<m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>T</m:t></m:r></m:e><m:sub><m:r><m:t>0</m:t></m:r></m:sub></m:sSub>'
        '<m:r><m:t> + </m:t></m:r>'
        '<m:f><m:num><m:r><m:t>&#x0394;</m:t></m:r><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>T</m:t></m:r></m:num>'
        '<m:den>'
        '<m:r><m:t>1 + </m:t></m:r>'
        '<m:f><m:num><m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>E</m:t></m:r></m:e><m:sub><m:r><m:t>tot</m:t></m:r></m:sub></m:sSub><m:r><m:t>(</m:t></m:r><m:r><m:rPr><m:sty m:val="b"/><m:scr m:val="it"/></m:rPr><m:t>x</m:t></m:r><m:r><m:t>)</m:t></m:r></m:num>'
        '<m:den><m:sSub><m:e><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>&#x03C3;</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:scr m:val="it"/></m:rPr><m:t>E</m:t></m:r></m:sub></m:sSub></m:den></m:f>'
        '</m:den></m:f>'
    )

# 9. Discrete Inference Assignment
def eq_discrete_inference():
    return eq_argmax_decision()

# 10. Total Loss Functional
def eq_total_loss():
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
