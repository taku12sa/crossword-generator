from typing import IO, Union

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.pdfgen.canvas import Canvas

from model import EMPTY_STR, Puzzle, PuzzlePropertyManager as PPM


PAGE_W, PAGE_H = A4


# ===== Page margins =====
MARGIN_LEFT = 18 * mm
MARGIN_RIGHT = 18 * mm
MARGIN_TOP = 18 * mm
MARGIN_BOTTOM = 18 * mm


# ===== Grid =====
CELL_SIZE = 6 * mm
GRID_LINE_WIDTH = 0.8
GRID_TOP_OFFSET = 52 * mm
GRID_TO_CLUES_GAP = 16 * mm

GRID_NUMBER_FONT = "Helvetica"
GRID_NUMBER_FONT_SIZE = 6
GRID_NUMBER_X_OFFSET = 1.5 * mm
GRID_NUMBER_Y_OFFSET = 3.5 * mm


# ===== Header =====
TITLE_FONT = "Helvetica-Bold"
TITLE_FONT_SIZE = 16
TITLE_TOP_OFFSET = 22 * mm

SUBTITLE_FONT = "Helvetica"
SUBTITLE_FONT_SIZE = 9.5
SUBTITLE_TOP_Y = PAGE_H - MARGIN_TOP + 4 * mm

META_FONT = "Helvetica"
META_FONT_SIZE = 10
META_TOP_OFFSET = 36 * mm
META_LINE_Y_OFFSET = 1


# ===== Instruction box =====
INSTRUCTION_FONT = "Helvetica"
INSTRUCTION_FONT_SIZE = 9
INSTRUCTION_TOP_OFFSET = 47 * mm
INSTRUCTION_BOX_HEIGHT = 8 * mm
INSTRUCTION_BOX_RADIUS = 2.5 * mm
INSTRUCTION_TEXT_X_OFFSET = 3 * mm
INSTRUCTION_TEXT_Y_OFFSET = 2.7 * mm


# ===== Clue header =====
CLUES_HEADER_FONT = "Helvetica-Bold"
CLUES_HEADER_FONT_SIZE = 10
CLUES_HEADER_RULE_OFFSET = 4 * mm
CLUES_HEADER_TEXT_OFFSET = 6.5 * mm


# ===== Clue body =====
CLUE_SECTION_FONT = "Helvetica-Bold"
CLUE_SECTION_FONT_SIZE = 11
CLUE_SECTION_SPACE_BEFORE = 2
CLUE_SECTION_SPACE_AFTER = 5

CLUE_NUMBER_FONT = "Helvetica-Bold"
CLUE_NUMBER_FONT_SIZE = 9.3

CLUE_BODY_FONT = "Helvetica"
CLUE_BODY_FONT_SIZE = 9.3
CLUE_BODY_LEADING = 12

CLUE_ROW_BOTTOM_PADDING = 2
CLUES_INITIAL_SPACER = 2 * mm
CLUES_SECTION_GAP = 3 * mm


# ===== 2-column layout =====
CLUE_COLUMN_GAP = 8 * mm
CLUE_NUMBER_COL_WIDTH = 10 * mm


# ===== Later pages =====
LATER_TITLE_FONT = "Helvetica-Bold"
LATER_TITLE_FONT_SIZE = 14
LATER_TITLE_TOP_OFFSET = 20 * mm
LATER_RULE_TOP_OFFSET = 23 * mm
LATER_RESERVED_TOP = 10 * mm


# ===== Footer =====
PAGE_FONT = "Helvetica"
PAGE_FONT_SIZE = 8.5
PAGE_NUMBER_BOTTOM = 9 * mm


# ===== Colors =====
COLOR_TEXT = colors.black
COLOR_SUBTITLE = colors.HexColor("#444444")
COLOR_SECTION = colors.HexColor("#1f4e79")
COLOR_RULE = colors.HexColor("#d0d7de")
COLOR_INSTRUCTION_BG = colors.HexColor("#eef4fb")
COLOR_INSTRUCTION_BORDER = colors.HexColor("#b7cde6")
COLOR_BLACK_CELL = colors.gray
COLOR_WHITE_CELL = colors.white


# ===== Meta line positions =====
NAME_LABEL_X = MARGIN_LEFT
NAME_LINE_START_X = 30 * mm
NAME_LINE_END_X = 88 * mm

CLASS_LABEL_X = 100 * mm
CLASS_LINE_START_X = 113 * mm
CLASS_LINE_END_X = 148 * mm

DATE_LABEL_X = 158 * mm
DATE_LINE_START_X = 170 * mm


def export_single_puzzle_pdf(
    puzzle: Puzzle,
    title: str,
    subtitle: str,
    instruction: str,
    output_path: Union[str, IO[bytes]],
) -> None:

    ppm = PPM(puzzle)
    grid_rows, grid_cols = puzzle.grid.shape

    grid_x = (PAGE_W - grid_cols * CELL_SIZE) / 2
    grid_y = PAGE_H - GRID_TOP_OFFSET - grid_rows * CELL_SIZE
    meta_y = PAGE_H - META_TOP_OFFSET
    instruction_box_y = PAGE_H - INSTRUCTION_TOP_OFFSET
    first_frame_top = grid_y - GRID_TO_CLUES_GAP

    clue_column_width = (
        PAGE_W - MARGIN_LEFT - MARGIN_RIGHT - CLUE_COLUMN_GAP
    ) / 2

    later_frame_height = PAGE_H - MARGIN_TOP - MARGIN_BOTTOM - LATER_RESERVED_TOP

    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="ClueBody",
            fontName=CLUE_BODY_FONT,
            fontSize=CLUE_BODY_FONT_SIZE,
            leading=CLUE_BODY_LEADING,
            textColor=COLOR_TEXT,
        )
    )

    styles.add(
        ParagraphStyle(
            name="ClueNumber",
            fontName=CLUE_NUMBER_FONT,
            fontSize=CLUE_NUMBER_FONT_SIZE,
            leading=CLUE_BODY_LEADING,
            textColor=COLOR_TEXT,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SectionHead",
            fontName=CLUE_SECTION_FONT,
            fontSize=CLUE_SECTION_FONT_SIZE,
            textColor=COLOR_SECTION,
            spaceBefore=CLUE_SECTION_SPACE_BEFORE,
            spaceAfter=CLUE_SECTION_SPACE_AFTER,
        )
    )

    def draw_grid(canv: Canvas) -> None:

        for r, row in enumerate(puzzle.grid):
            for c, cell in enumerate(row):

                x = grid_x + c * CELL_SIZE
                y = grid_y + (grid_rows - 1 - r) * CELL_SIZE

                canv.setStrokeColor(COLOR_TEXT)
                canv.setLineWidth(GRID_LINE_WIDTH)

                if cell == EMPTY_STR:

                    canv.setFillColor(COLOR_BLACK_CELL)
                    canv.rect(
                        x=x,
                        y=y,
                        width=CELL_SIZE,
                        height=CELL_SIZE,
                        stroke=1,
                        fill=1,
                    )

                else:

                    canv.setFillColor(COLOR_WHITE_CELL)
                    canv.rect(
                        x=x,
                        y=y,
                        width=CELL_SIZE,
                        height=CELL_SIZE,
                        stroke=1,
                        fill=1,
                    )

                    num = ppm.address2num(row_idx=r, col_idx=c)

                    if num is not None:

                        canv.setFont(
                            psfontname=GRID_NUMBER_FONT,
                            size=GRID_NUMBER_FONT_SIZE,
                        )

                        canv.setFillColor(COLOR_TEXT)

                        canv.drawString(
                            x=x + GRID_NUMBER_X_OFFSET,
                            y=y + CELL_SIZE - GRID_NUMBER_Y_OFFSET,
                            text=str(num),
                        )

    def draw_first_page(canv: Canvas, doc) -> None:

        canv.saveState()

        canv.setFont(psfontname=TITLE_FONT, size=TITLE_FONT_SIZE)
        canv.setFillColor(COLOR_TEXT)

        canv.drawCentredString(
            x=PAGE_W / 2,
            y=PAGE_H - TITLE_TOP_OFFSET,
            text=title,
        )

        if subtitle:

            canv.setFont(psfontname=SUBTITLE_FONT, size=SUBTITLE_FONT_SIZE)
            canv.setFillColor(COLOR_SUBTITLE)

            canv.drawRightString(
                x=PAGE_W - MARGIN_RIGHT,
                y=SUBTITLE_TOP_Y,
                text=subtitle,
            )

        canv.setFillColor(COLOR_TEXT)
        canv.setFont(psfontname=META_FONT, size=META_FONT_SIZE)

        canv.drawString(x=NAME_LABEL_X, y=meta_y, text="Name:")
        canv.line(
            x1=NAME_LINE_START_X,
            y1=meta_y - META_LINE_Y_OFFSET,
            x2=NAME_LINE_END_X,
            y2=meta_y - META_LINE_Y_OFFSET,
        )

        canv.drawString(x=CLASS_LABEL_X, y=meta_y, text="Class:")
        canv.line(
            x1=CLASS_LINE_START_X,
            y1=meta_y - META_LINE_Y_OFFSET,
            x2=CLASS_LINE_END_X,
            y2=meta_y - META_LINE_Y_OFFSET,
        )

        canv.drawString(x=DATE_LABEL_X, y=meta_y, text="Date:")
        canv.line(
            x1=DATE_LINE_START_X,
            y1=meta_y - META_LINE_Y_OFFSET,
            x2=PAGE_W - MARGIN_RIGHT,
            y2=meta_y - META_LINE_Y_OFFSET,
        )

        canv.setFillColor(COLOR_INSTRUCTION_BG)
        canv.setStrokeColor(COLOR_INSTRUCTION_BORDER)

        canv.roundRect(
            x=MARGIN_LEFT,
            y=instruction_box_y,
            width=PAGE_W - MARGIN_LEFT - MARGIN_RIGHT,
            height=INSTRUCTION_BOX_HEIGHT,
            radius=INSTRUCTION_BOX_RADIUS,
            stroke=1,
            fill=1,
        )

        canv.setFillColor(COLOR_TEXT)
        canv.setFont(psfontname=INSTRUCTION_FONT, size=INSTRUCTION_FONT_SIZE)

        canv.drawString(
            x=MARGIN_LEFT + INSTRUCTION_TEXT_X_OFFSET,
            y=instruction_box_y + INSTRUCTION_TEXT_Y_OFFSET,
            text=instruction,
        )

        draw_grid(canv)

        canv.setStrokeColor(COLOR_RULE)

        canv.line(
            x1=MARGIN_LEFT,
            y1=first_frame_top + CLUES_HEADER_RULE_OFFSET,
            x2=PAGE_W - MARGIN_RIGHT,
            y2=first_frame_top + CLUES_HEADER_RULE_OFFSET,
        )

        canv.setFont(psfontname=CLUES_HEADER_FONT, size=CLUES_HEADER_FONT_SIZE)
        canv.setFillColor(COLOR_SECTION)

        canv.drawString(
            x=MARGIN_LEFT,
            y=first_frame_top + CLUES_HEADER_TEXT_OFFSET,
            text="Clues",
        )

        canv.setFillColor(COLOR_TEXT)
        canv.setFont(psfontname=PAGE_FONT, size=PAGE_FONT_SIZE)

        canv.drawRightString(
            x=PAGE_W - MARGIN_RIGHT,
            y=PAGE_NUMBER_BOTTOM,
            text=f"Page {doc.page}",
        )

        canv.restoreState()

    def draw_later_pages(canv: Canvas, doc) -> None:

        canv.saveState()

        canv.setFont(psfontname=LATER_TITLE_FONT, size=LATER_TITLE_FONT_SIZE)
        canv.setFillColor(COLOR_TEXT)

        canv.drawString(
            x=MARGIN_LEFT,
            y=PAGE_H - LATER_TITLE_TOP_OFFSET,
            text=f"{title} - Continued Clues",
        )

        canv.setStrokeColor(COLOR_RULE)

        canv.line(
            x1=MARGIN_LEFT,
            y1=PAGE_H - LATER_RULE_TOP_OFFSET,
            x2=PAGE_W - MARGIN_RIGHT,
            y2=PAGE_H - LATER_RULE_TOP_OFFSET,
        )

        canv.setFont(psfontname=PAGE_FONT, size=PAGE_FONT_SIZE)
        canv.setFillColor(COLOR_TEXT)

        canv.drawRightString(
            x=PAGE_W - MARGIN_RIGHT,
            y=PAGE_NUMBER_BOTTOM,
            text=f"Page {doc.page}",
        )

        canv.restoreState()

    def make_clue(number: int, text: str) -> Table:

        table = Table(
            [
                [
                    Paragraph(f"{number}.", styles["ClueNumber"]),
                    Paragraph(text, styles["ClueBody"]),
                ]
            ],
            colWidths=[
                CLUE_NUMBER_COL_WIDTH,
                clue_column_width - CLUE_NUMBER_COL_WIDTH,
            ],
        )

        table.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                    ("TOPPADDING", (0, 0), (-1, -1), 0),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), CLUE_ROW_BOTTOM_PADDING),
                ]
            )
        )

        return table

    doc = BaseDocTemplate(
        filename=output_path,
        pagesize=A4,
        leftMargin=MARGIN_LEFT,
        rightMargin=MARGIN_RIGHT,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM,
    )

    doc.addPageTemplates(
        [
            PageTemplate(
                id="first",
                frames=[
                    Frame(
                        MARGIN_LEFT,
                        MARGIN_BOTTOM,
                        clue_column_width,
                        first_frame_top - MARGIN_BOTTOM,
                        id="first_left",
                    ),
                    Frame(
                        MARGIN_LEFT + clue_column_width + CLUE_COLUMN_GAP,
                        MARGIN_BOTTOM,
                        clue_column_width,
                        first_frame_top - MARGIN_BOTTOM,
                        id="first_right",
                    ),
                ],
                onPage=draw_first_page,
                autoNextPageTemplate="later",
            ),
            PageTemplate(
                id="later",
                frames=[
                    Frame(
                        MARGIN_LEFT,
                        MARGIN_BOTTOM,
                        clue_column_width,
                        later_frame_height,
                        id="later_left",
                    ),
                    Frame(
                        MARGIN_LEFT + clue_column_width + CLUE_COLUMN_GAP,
                        MARGIN_BOTTOM,
                        clue_column_width,
                        later_frame_height,
                        id="later_right",
                    ),
                ],
                onPage=draw_later_pages,
            ),
        ]
    )

    story = [Spacer(0, CLUES_INITIAL_SPACER)]

    story.append(Paragraph("Across", styles["SectionHead"]))

    for clue in ppm.get_clues(False):
        story.append(make_clue(clue.number, clue.text))

    story.append(Spacer(0, CLUES_SECTION_GAP))

    story.append(Paragraph("Down", styles["SectionHead"]))

    for clue in ppm.get_clues(True):
        story.append(make_clue(clue.number, clue.text))

    doc.build(story)