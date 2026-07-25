import io
from xml.sax.saxutils import escape

from docx import Document
from docx.oxml.ns import qn
from docx.shared import Pt
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

# Same candidate paths share_card.py uses for Pillow — macOS locally,
# Debian's fonts-noto-cjk package (installed in the Dockerfile) in production.
CJK_FONT_CANDIDATES = [
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/Songti.ttc",
]


def _chapter_paragraphs(chapter):
    return [p for p in chapter["content"].split("\n") if p.strip()]


def _set_run_cjk_font(run, name="Microsoft YaHei"):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)


def build_novel_docx(novel, chapters):
    doc = Document()

    normal = doc.styles["Normal"]
    normal.font.name = "Microsoft YaHei"
    normal.font.size = Pt(12)
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), "Microsoft YaHei")

    title = doc.add_heading(novel["title"], level=0)
    for run in title.runs:
        _set_run_cjk_font(run)

    if novel["summary"]:
        p = doc.add_paragraph()
        run = p.add_run(novel["summary"])
        run.italic = True
        _set_run_cjk_font(run)

    for i, chapter in enumerate(chapters):
        if i > 0:
            doc.add_page_break()
        heading = doc.add_heading(f"第 {chapter['chapter_no']} 章 · {chapter['title']}", level=1)
        for run in heading.runs:
            _set_run_cjk_font(run)
        for para_text in _chapter_paragraphs(chapter):
            p = doc.add_paragraph()
            run = p.add_run(para_text)
            _set_run_cjk_font(run)

    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf


def _register_pdf_font():
    for path in CJK_FONT_CANDIDATES:
        try:
            pdfmetrics.registerFont(TTFont("NovelExportCJK", path, subfontIndex=0))
            return "NovelExportCJK"
        except Exception:
            continue
    return "Helvetica"


def build_novel_pdf(novel, chapters):
    font_name = _register_pdf_font()
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "NovelTitle", parent=styles["Title"], fontName=font_name, fontSize=22, leading=30
    )
    summary_style = ParagraphStyle(
        "NovelSummary", parent=styles["Normal"], fontName=font_name, fontSize=10.5,
        leading=18, textColor="#666666", spaceAfter=14,
    )
    heading_style = ParagraphStyle(
        "ChapterHeading", parent=styles["Heading1"], fontName=font_name, fontSize=15,
        leading=22, spaceBefore=18, spaceAfter=10,
    )
    body_style = ParagraphStyle(
        "ChapterBody", parent=styles["Normal"], fontName=font_name, fontSize=11,
        leading=20, spaceAfter=10, firstLineIndent=22,
    )

    story = [Paragraph(escape(novel["title"]), title_style), Spacer(1, 10)]
    if novel["summary"]:
        story.append(Paragraph(escape(novel["summary"]), summary_style))

    for i, chapter in enumerate(chapters):
        if i > 0:
            story.append(PageBreak())
        story.append(Paragraph(escape(f"第 {chapter['chapter_no']} 章 · {chapter['title']}"), heading_style))
        for para_text in _chapter_paragraphs(chapter):
            story.append(Paragraph(escape(para_text), body_style))

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4, topMargin=2.2 * cm, bottomMargin=2.2 * cm,
        leftMargin=2.2 * cm, rightMargin=2.2 * cm, title=novel["title"],
    )
    doc.build(story)
    buf.seek(0)
    return buf
