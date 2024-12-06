import sys
import re
import trafilatura
import httpx
import asyncio
from tqdm.asyncio import tqdm
from decouple import config
from app.ai.aigentext import generate
from loguru import logger


chunk_size = config('SCRAPECHUNKSIZE')

def split_user_input(text):
    # Split the input text into paragraphs
    paragraphs = text.split('\n')
    # Remove empty paragraphs and trim whitespace
    paragraphs = [paragraph.strip() for paragraph in paragraphs if paragraph.strip()]
    return paragraphs

def scrape_text_from_url(url):
    """
    Scrape the content from the URL
    """
    try:
        downloaded = trafilatura.fetch_url(url)
        text = trafilatura.extract(downloaded, include_formatting=True)
        if text is None:
            return []
        text_chunks = text.split("\n")
        article_content = [text for text in text_chunks if text]
        return article_content
    except Exception as e:
        logger.error('Ошибка:\n{e}')

async def call_gpt_api(prompt, additional_messages=[]):
    """
    Call GPT API asynchronously
    """
    messages = additional_messages + [{"role": "user", "content": prompt}]
    try:
        result = await generate(prompt, additional_messages)
        return result
    except Exception as e:
        logger.error(f'Ошибка:\n{e}')

async def summarize(text_array):
    """
    Summarize the text using GPT API asynchronously
    """
    def create_chunks(paragraphs):
        chunks = []
        chunk = ''
        for paragraph in paragraphs:
            if len(chunk) + len(paragraph) < chunk_size:
                chunk += paragraph + ' '
            else:
                chunks.append(chunk.strip())
                chunk = paragraph + ' '
        if chunk:
            chunks.append(chunk.strip())
        return chunks

    try:
        text_chunks = create_chunks(text_array)
        text_chunks = [chunk for chunk in text_chunks if chunk]  # Remove empty chunks

        # Call the GPT API in parallel to summarize the text chunks
        summaries = []
        system_messages = [
            {"role": "system", "content": "You are an expert in creating summaries that capture the main points and key details."},
            {"role": "system", "content": f"You will show the bulleted list content without translate any technical terms."},
            {"role": "system", "content": f"You will print all the content in {lang}."},
        ]

        async def summarize_chunk(chunk):
            return await call_gpt_api(f"Summary keypoints for the following text:\n{chunk}", system_messages)

        tasks = [summarize_chunk(chunk) for chunk in text_chunks]
        for task in tqdm.as_completed(tasks, total=len(text_chunks), desc="Summarizing"):
            summaries.append(await task)

        if len(summaries) <= 5:
            summary = ' '.join(summaries)
            async with tqdm.tqdm(total=1, desc="Final summarization") as progress_bar:
                final_summary = await call_gpt_api(f"Create a bulleted list using {lang} to show the key points of the following text:\n{summary}", system_messages)
                progress_bar.update(1)
            return final_summary
        else:
            return await summarize(summaries)
    except Exception as e:
        logger.error(f"Ошибка:\n{e}")
        


async def scrape_url(text):
    text_array = scrape_text_from_url(text)
    summary = await summarize(text_array)
    return summary

async def split_user_inp(text):
    text_array = split_user_input(text)
    summary = await summarize(text_array)
    return summary
