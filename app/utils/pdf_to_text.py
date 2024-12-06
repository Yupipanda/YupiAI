from PyPDF2 import PdfReader
from loguru import logger

async def extract_text_from_pdf(pdf_filename: str) -> str:
	try:
		text_output = ''
		images = None
		reader = PdfReader(pdf_filename)
		number_of_pages = len(reader.pages)
		for i in range(number_of_pages):
			page = reader.pages[i]
			text_output += page.extract_text() + '\n'
		return text_output
	except Exception as ex:
		logger.error(f'Ошибка:\n{ex}')