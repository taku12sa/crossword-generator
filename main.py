from picker import pick_puzzles
from renderer import export_single_puzzle_pdf
from renderer import DEFAULT_THEME_COLOR, INSTRUCTION_LAYOUT_VERSION
from io import BytesIO
from pypdf import PdfReader, PdfWriter


def pdf_writer(
		infileobj,
		max_grid_size, 
		n_variants, 
		pdf_title, 
		pdf_instruction, 
		delimiter = ",",
		theme_color = DEFAULT_THEME_COLOR,
		rendering_message = "PDF rendering...", 
		print_interval = 100, 
		random_seed = 0
):
	writer = PdfWriter()
	for idx, puzzle in enumerate(
			pick_puzzles(
				fileobj = infileobj,
				grid_size_leq = max_grid_size,
				stop_picking_at = n_variants,
				random_seed = random_seed,
				print_interval = print_interval,
				delimiter = delimiter,
			)
		):
		buffer = BytesIO()
		export_single_puzzle_pdf(
			puzzle = puzzle,
			title = pdf_title,
			subtitle = f"variant: {idx+1} | {INSTRUCTION_LAYOUT_VERSION}",
			instruction = pdf_instruction,
			output_path = buffer,
			theme_color = theme_color,
		)
		buffer.seek(0)
		reader = PdfReader(stream=buffer)
		writer.append(reader)
		if len(reader.pages)%2==1:
			writer.add_blank_page(
				width = reader.pages[0].mediabox.width,
				height = reader.pages[0].mediabox.height,
			)
		print(f"[{idx}] {puzzle}\n{rendering_message}")
	return writer