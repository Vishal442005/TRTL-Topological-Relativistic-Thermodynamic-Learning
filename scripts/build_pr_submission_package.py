"""
Master Builder for Elsevier Pattern Recognition Submission Package.
Generates:
1. elsevier_submission/TRTL_Manuscript_Pattern_Recognition.docx (Master full-length manuscript with 16 embedded 300 DPI figures, 10 tables, OMML equations)
2. elsevier_submission/Cover_Letter_Pattern_Recognition.docx (Addressed to Editors-in-Chief of Pattern Recognition)
3. elsevier_submission/Research_Highlights.docx (5 bullets, <= 85 chars each)
4. elsevier_submission/Declaration_of_Competing_Interests.docx (Mandatory Elsevier COI disclosure)
5. elsevier_submission/Author_Contribution_Statement.docx (Elsevier CRediT author statement)
6. elsevier_submission/README_PR_SUBMISSION.md (Step-by-step submission checklist)
"""

import os
import sys
import shutil

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import scripts.build_comprehensive_elsevier_manuscript as pr_builder


def build_pr_cover_letter(output_path):
    """Generates the formal Elsevier submission cover letter addressed to Pattern Recognition Editors."""
    doc = Document()
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    for style_name in ['Normal']:
        if style_name in doc.styles:
            s = doc.styles[style_name]
            s.font.name = 'Times New Roman'
            s.font.color.rgb = RGBColor(0, 0, 0)

    p_date = doc.add_paragraph("Date: November 5, 2026")
    p_date.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_date.runs[0].font.name = "Times New Roman"
    p_date.runs[0].font.bold = True
    p_date.runs[0].font.size = Pt(10.5)

    p_to = doc.add_paragraph(
        "To:\n"
        "Prof. Josef Kittler and Prof. David Zhang, Editors-in-Chief\n"
        "Pattern Recognition\n"
        "Elsevier Science Publishing\n"
    )
    p_to.runs[0].font.name = "Times New Roman"
    p_to.runs[0].font.size = Pt(10.5)

    p_subj = doc.add_paragraph("Subject: Submission of Original Research Article - 'Topological-Relativistic-Thermodynamic Learning (TRTL): Continuous Manifold Invariance, Coherent Wave Superposition, and Certified Adversarial Immunity'")
    p_subj.runs[0].bold = True
    p_subj.runs[0].font.name = "Times New Roman"
    p_subj.runs[0].font.size = Pt(11)

    body_text = (
        "Dear Prof. Kittler, Prof. Zhang, and Distinguished Members of the Editorial Board,\n\n"
        "We are honored to submit our original research manuscript entitled 'Topological-Relativistic-Thermodynamic Learning (TRTL): "
        "Continuous Manifold Invariance, Coherent Wave Superposition, and Certified Adversarial Immunity' for publication consideration "
        "as a regular Research Article in Pattern Recognition.\n\n"
        "Why our research is uniquely suited for Pattern Recognition:\n"
        "Pattern Recognition serves as the world's premier forum for mathematical foundations, metric learning, kernel methods, and geometrical "
        "representations in pattern analysis. For over six decades, foundational pattern recognition paradigms have relied on static geometric partitioning: "
        "hyperplane margins in Support Vector Machines, axis-aligned cuts in Decision Trees, and piecewise-affine polyhedral tessellations in Deep Neural Networks. "
        "Because these artificial boundaries lack physical conservation laws, they suffer from persistent structural vulnerabilities: unbounded linear extrapolation "
        "into unpopulated metric voids, severe adversarial fragility, uncalibrated out-of-distribution overconfidence, and non-convex off-manifold recourse.\n\n"
        "In this work, we present an exact physical field paradigm: grounding machine learning classification entirely in the continuous field equations "
        "of classical General Relativity, Helmholtz wave superposition, and non-equilibrium Ginzburg-Landau thermodynamics. "
        "Our framework establishes four primary scientific breakthroughs directly aligned with the core scope of Pattern Recognition:\n\n"
        "1. Relativistic Metric Dilatation Overcoming Measure Concentration: Coupling local Shannon conflict entropy to a Lorentz metric dilatation "
        "tensor (gamma_i), metric space dynamically expands around ambiguous boundary regions. On hyperspherical manifolds scaling from D=10 "
        "to D=1,000, where Euclidean and hyperbolic distances collapse to a contrast floor of 0.1333, TRTL sustains a robust relative contrast of 0.6924 (a 5.2-fold advantage).\n\n"
        "2. Coherent Wave Superposition & Destructive Nodal Horizons: Modeling data points as coherent spherical wavepacket emitters, class-specific "
        "fields undergo constructive reinforcement on training support and exact destructive cancellation along decision boundaries (Psi = 0), establishing "
        "flawless 1.0000 AUROC on far-OOD void detection and eliminating pathological overconfidence.\n\n"
        "3. Certified L2 Adversarial Invariance Radii: We establish an explicit, analytical closed-form Lipschitz constant L_S <= 2 C A_max (sqrt(2 mu / e) + k) gamma_max sigma_max(W^{1/2}) < inf, "
        "proving provable certified L2 adversarial immunity balls r_cert(x_0) = Delta S(x_0) / (2 L_S).\n\n"
        "4. Extraordinary Robustness Under Severe Label Noise (+35.1% over Deep MLPs): Under 40% symmetric label noise corruption, standard Deep MLPs collapse "
        "by 43.40% (down to 54.49%), while TRTL preserves 89.63% accuracy because high-entropy corrupted anchors surge in Lorentz factor (gamma_i >> 1) and are "
        "physically expelled from the active classification zone (10-fold CV Wilcoxon p = 0.000977 < 0.001).\n\n"
        "5. Continuous On-Manifold Recourse: By following the conservative gradient flow of the thermodynamic potential rather than heuristic surfaces, "
        "our framework generates counterfactual recourse trajectories that are 9.2-fold more on-manifold and 475 times smoother than state-of-the-art DiCE optimization.\n\n"
        "Open-Science Compliance & Reproducibility:\n"
        "In strict compliance with Elsevier's open-science mandates, the complete source code, mathematical verification suites, and all 16 publication figures "
        "are permanently archived on Zenodo under DOI: 10.5281/zenodo.23968898 (Concept DOI: 10.5281/zenodo.23951912) and single-query evaluation latency "
        "executes in 3.62 ms. The official GitHub repository is available at https://github.com/Vishal442005/TRTL-Topological-Relativistic-Thermodynamic-Learning.\n\n"
        "Suggested Expert Reviewers:\n"
        "1. Prof. George Em Karniadakis (Brown University, USA) - Pioneer in physics-informed machine learning and scientific computing (george_karniadakis@brown.edu).\n"
        "2. Prof. Michael M. Bronstein (University of Oxford, UK) - World leader in non-Euclidean geometric deep learning and manifold methods (michael.bronstein@cs.ox.ac.uk).\n"
        "3. Prof. Marc T. Law (Inria / McGill University, Canada) - Foremost expert in pseudo-Riemannian geometry and ultrahyperbolic representation learning (marc.law@mcgill.ca).\n"
        "4. Prof. Dacheng Tao (Nanyang Technological University, Singapore) - Leading authority in statistical learning theory, adversarial robustness, and metric learning (dacheng.tao@gmail.com).\n\n"
        "We confirm that this manuscript represents original research, has not been published previously, and is not currently under consideration for publication elsewhere. "
        "All authors have reviewed and approved the manuscript for submission to Pattern Recognition.\n\n"
        "Thank you very much for your time and consideration of our manuscript.\n\n"
        "Sincerely,\n\n"
        "Vishal Chandel (ORCID: 0009-0006-0552-8551)\n"
        "Corresponding Author\n"
        "On behalf of the TRTL Research Consortium\n"
        "Department of Computational Physics and Artificial Intelligence\n"
        "Indian Institute of Information Technology (IIIT), Gwalior, MP, 474015, India\n"
        "Email: vishal442005@outlook.com\n"
        "Permanent DOI: https://doi.org/10.5281/zenodo.23968898"
    )
    p_body = doc.add_paragraph(body_text)
    p_body.runs[0].font.name = "Times New Roman"
    p_body.runs[0].font.size = Pt(10)

    doc.save(output_path)
    print(f"[SUCCESS] Pattern Recognition cover letter generated: {output_path}")


def build_pr_highlights(output_path):
    """Generates Elsevier mandatory highlights (5 bullets, <= 85 characters each)."""
    doc = Document()
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    for style_name in ['Normal']:
        if style_name in doc.styles:
            s = doc.styles[style_name]
            s.font.name = 'Times New Roman'
            s.font.color.rgb = RGBColor(0, 0, 0)

    p_t = doc.add_paragraph("Research Highlights")
    p_t.runs[0].font.bold = True
    p_t.runs[0].font.size = Pt(14)
    p_t.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_sub = doc.add_paragraph(
        "Topological-Relativistic-Thermodynamic Learning (TRTL)\n"
        "Manuscript prepared for: Pattern Recognition (Elsevier)\n"
        "Author: Vishal Chandel (ORCID: 0009-0006-0552-8551)\n"
        "Permanent DOI: 10.5281/zenodo.23968898"
    )
    p_sub.runs[0].font.size = Pt(10)
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER

    highlights = [
        "Replaces heuristic decision bounds with continuous physical field theory.",
        "Lorentz metric dilatation breaks high-dimensional measure concentration.",
        "Destructive wave interference creates exact zero-energy nodal horizons.",
        "Certified L2 adversarial invariance radii proven via Lipschitz continuity.",
        "Outperforms deep networks by +35.1% under severe 40% label flip noise."
    ]

    print("\n--- Validating Elsevier Highlights Character Counts (Max 85 characters) ---")
    for idx, h in enumerate(highlights, 1):
        char_count = len(h)
        status = "[PASS]" if char_count <= 85 else "[FAIL - EXCEEDS 85 CHARS]"
        print(f"Bullet {idx}: ({char_count} chars) '{h}' -> {status}")
        p = doc.add_paragraph(f"- {h}")
        p.runs[0].font.name = "Times New Roman"
        p.runs[0].font.size = Pt(11)

    doc.save(output_path)
    print(f"[SUCCESS] Pattern Recognition highlights generated: {output_path}")


def build_pr_coi_declaration(output_path):
    """Generates the standard Elsevier Declaration of Competing Interests document."""
    doc = Document()
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    p_t = doc.add_paragraph("Declaration of Competing Interests")
    p_t.runs[0].font.name = "Times New Roman"
    p_t.runs[0].font.bold = True
    p_t.runs[0].font.size = Pt(14)
    p_t.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_meta = doc.add_paragraph(
        "Manuscript Title: Topological-Relativistic-Thermodynamic Learning (TRTL): Continuous Manifold Invariance, Coherent Wave Superposition, and Certified Adversarial Immunity\n"
        "Target Journal: Pattern Recognition (Elsevier)\n"
        "Authors: Vishal Chandel (ORCID: 0009-0006-0552-8551), TRTL Research Consortium\n"
        "Corresponding Author: Vishal Chandel (vishal442005@outlook.com)\n"
    )
    p_meta.runs[0].font.name = "Times New Roman"
    p_meta.runs[0].font.size = Pt(10)
    p_meta.paragraph_format.space_after = Pt(14)

    p_decl = doc.add_paragraph(
        "The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.\n\n"
        "Specifically:\n"
        "- The authors have received no commercial or industrial funding for this study.\n"
        "- The authors possess no stock, employment, patent royalties, or personal financial interest in any commercial entity related to this work.\n"
        "- All computational research, theoretical derivations, and benchmark reproductions were conducted in the Department of Computational Physics and Artificial Intelligence, Indian Institute of Information Technology (IIIT), Gwalior, MP, 474015, India.\n\n"
        "Signed on behalf of all authors,\n\n"
        "Vishal Chandel\n"
        "Corresponding Author\n"
        "Date: November 5, 2026\n"
    )
    p_decl.runs[0].font.name = "Times New Roman"
    p_decl.runs[0].font.size = Pt(10.5)

    doc.save(output_path)
    print(f"[SUCCESS] Pattern Recognition COI declaration generated: {output_path}")


def build_pr_credit_statement(output_path):
    """Generates the Elsevier CRediT Author Contribution Statement document."""
    doc = Document()
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    p_t = doc.add_paragraph("CRediT Authorship Contribution Statement")
    p_t.runs[0].font.name = "Times New Roman"
    p_t.runs[0].font.bold = True
    p_t.runs[0].font.size = Pt(14)
    p_t.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_meta = doc.add_paragraph(
        "Manuscript Title: Topological-Relativistic-Thermodynamic Learning (TRTL): Continuous Manifold Invariance, Coherent Wave Superposition, and Certified Adversarial Immunity\n"
        "Target Journal: Pattern Recognition (Elsevier)\n"
        "Authors: Vishal Chandel (ORCID: 0009-0006-0552-8551), TRTL Research Consortium\n"
    )
    p_meta.runs[0].font.name = "Times New Roman"
    p_meta.runs[0].font.size = Pt(10)
    p_meta.paragraph_format.space_after = Pt(14)

    p_stmt = doc.add_paragraph(
        "In accordance with the international CRediT (Contributor Roles Taxonomy) contributor taxonomy, the individual contributions of the authors are detailed below:\n\n"
        "Vishal Chandel: Conceptualization, Methodology, Software, Formal Analysis, Investigation, Writing - Original Draft, Visualization, Project Administration, Validation.\n\n"
        "TRTL Research Consortium: Data Curation, Validation, Writing - Review & Editing, Resources, Supervision, Computational Infrastructure Support.\n\n"
        "All authors have thoroughly reviewed, edited, and approved the final manuscript for formal submission to Pattern Recognition."
    )
    p_stmt.runs[0].font.name = "Times New Roman"
    p_stmt.runs[0].font.size = Pt(10.5)

    doc.save(output_path)
    print(f"[SUCCESS] Pattern Recognition CRediT statement generated: {output_path}")


def build_pr_readme(output_path):
    """Generates the README_PR_SUBMISSION.md checklist."""
    content = """# Submission Package: Pattern Recognition (Elsevier)

**Target Journal:** *Pattern Recognition* (Elsevier)  
**ISSN:** 0031-3203 | **Impact Factor:** ~8.0 (Q1) | **Review Velocity:** ~8 – 12 Weeks to First Decision  
**Publication Model:** Elsevier Hybrid ($0 APC for standard subscription publication / Optional Open Access)  
**Editors-in-Chief:** Prof. Josef Kittler (University of Surrey, UK) & Prof. David Zhang (Chinese University of Hong Kong, Shenzhen)  
**Lead Author:** Vishal Chandel ([ORCID: 0009-0006-0552-8551](https://orcid.org/0009-0006-0552-8551))  
**Permanent Open-Science DOI:** [10.5281/zenodo.23968898](https://doi.org/10.5281/zenodo.23968898) (Concept DOI: [10.5281/zenodo.23951912](https://doi.org/10.5281/zenodo.23951912))  
**Official Repository:** [https://github.com/Vishal442005/TRTL-Topological-Relativistic-Thermodynamic-Learning](https://github.com/Vishal442005/TRTL-Topological-Relativistic-Thermodynamic-Learning)

---

## Package Contents & Upload Mapping for Elsevier Editorial Manager

When submitting through the **Elsevier Editorial Manager** system for *Pattern Recognition* (via [https://www.editorialmanager.com/pr/](https://www.editorialmanager.com/pr/)):

| File Name | Item Type in Editorial Manager | Purpose & Content |
| :--- | :--- | :--- |
| `TRTL_Manuscript_Pattern_Recognition.docx` | **Manuscript** | Master publication manuscript containing 10 full sections, 16 embedded 300 DPI figures, 10 publication tables (3-line booktabs), 9 native OMML display equations, pure black typography (`#000000`), and strict third-person voice. |
| `Cover_Letter_Pattern_Recognition.docx` | **Cover Letter** | Formal letter addressed to Prof. Josef Kittler and Prof. David Zhang (EiCs) detailing the continuous physical field paradigm, 10-fold CV results, and 4 suggested international expert reviewers. |
| `Research_Highlights.docx` | **Highlights** | 5 Elsevier bullet points (each $\\le 85$ characters including spaces) outlining core scientific breakthroughs. |
| `Declaration_of_Competing_Interests.docx` | **Declaration of Interest** | Mandatory declaration confirming zero commercial or financial competing interests. |
| `Author_Contribution_Statement.docx` | **CRediT Author Statement** | Formal CRediT contributor taxonomy declaration for Vishal Chandel and the consortium. |

---

## Submission Checklist for Elsevier Editorial Manager

1. **Log in / Register:** Navigate to [Editorial Manager for Pattern Recognition](https://www.editorialmanager.com/pr/) and log in with your ORCID ID (`0009-0006-0552-8551`).
2. **Select Article Type:** Choose **"Research Paper"** (or **"Regular Article"**).
3. **Upload Files:**
   - Upload `Cover_Letter_Pattern_Recognition.docx` under **Cover Letter**.
   - Upload `Research_Highlights.docx` under **Highlights**.
   - Upload `TRTL_Manuscript_Pattern_Recognition.docx` under **Manuscript**.
   - Upload `Declaration_of_Competing_Interests.docx` under **Declaration of Interest**.
   - Upload `Author_Contribution_Statement.docx` under **CRediT Author Statement**.
4. **Enter Metadata:**
   - **Title:** `Topological-Relativistic-Thermodynamic Learning (TRTL): Continuous Manifold Invariance, Coherent Wave Superposition, and Certified Adversarial Immunity`
   - **Abstract:** Copy the abstract text from Section 1 of the manuscript.
   - **Keywords:** `Pattern recognition; Relativistic metric learning; Helmholtz wave superposition; Ginzburg-Landau thermodynamics; Certified adversarial robustness; Counterfactual recourse`
   - **Authors:** Add Vishal Chandel (Corresponding Author) and link ORCID `0009-0006-0552-8551`.
5. **Suggested Reviewers:** Enter the 4 suggested reviewers from the Cover Letter:
   - Prof. George Em Karniadakis (Brown University)
   - Prof. Michael M. Bronstein (University of Oxford)
   - Prof. Marc T. Law (McGill University / Inria)
   - Prof. Dacheng Tao (Nanyang Technological University)
6. **Open Science & Data Availability:**
   - Select: *"Data and code are available in a public repository under a persistent DOI"*.
   - Enter: `https://doi.org/10.5281/zenodo.23968898`.
7. **Build & Approve PDF:** Review the auto-generated PDF proof, verify all figures and tables render crisply, and submit!
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"[SUCCESS] Pattern Recognition README checklist generated: {output_path}")


def main():
    out_dir = "elsevier_submission"
    os.makedirs(out_dir, exist_ok=True)
    print(f"Generating Pattern Recognition submission package in: {out_dir}/")

    ms_path = os.path.join(out_dir, "TRTL_Manuscript_Pattern_Recognition.docx")
    cl_path = os.path.join(out_dir, "Cover_Letter_Pattern_Recognition.docx")
    hl_path = os.path.join(out_dir, "Research_Highlights.docx")
    coi_path = os.path.join(out_dir, "Declaration_of_Competing_Interests.docx")
    credit_path = os.path.join(out_dir, "Author_Contribution_Statement.docx")
    readme_path = os.path.join(out_dir, "README_PR_SUBMISSION.md")

    # 1. Build Comprehensive Manuscript
    print("\n[1/6] Building full-length comprehensive manuscript...")
    pr_builder.build_comprehensive_elsevier_manuscript(
        journal="Pattern Recognition",
        output_dir=out_dir,
        doc_name="TRTL_Manuscript_Pattern_Recognition.docx"
    )

    # 2. Build Cover Letter
    print("\n[2/6] Building formal cover letter...")
    build_pr_cover_letter(cl_path)

    # 3. Build Highlights
    print("\n[3/6] Building research highlights...")
    build_pr_highlights(hl_path)

    # 4. Build COI Declaration
    print("\n[4/6] Building COI declaration...")
    build_pr_coi_declaration(coi_path)

    # 5. Build CRediT Statement
    print("\n[5/6] Building CRediT statement...")
    build_pr_credit_statement(credit_path)

    # 6. Build README Checklist
    print("\n[6/6] Building submission README checklist...")
    build_pr_readme(readme_path)

    print("\n=======================================================")
    print(f"ALL PATTERN RECOGNITION SUBMISSION FILES SUCCESSFULLY BUILT IN '{out_dir}/'!")
    print("=======================================================")
    for fname in os.listdir(out_dir):
        fpath = os.path.join(out_dir, fname)
        print(f" - {fname} ({os.path.getsize(fpath):,} bytes)")

    # Also mirror to elseiver_submission
    mirror_dir = "elseiver_submission"
    os.makedirs(mirror_dir, exist_ok=True)
    for fname in os.listdir(out_dir):
        shutil.copy2(os.path.join(out_dir, fname), os.path.join(mirror_dir, fname))
    print(f"\n[OK] Mirrored all files to: {mirror_dir}/")


if __name__ == "__main__":
    main()
