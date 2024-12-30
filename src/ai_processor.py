import google.generativeai as genai
from .config import Config

class AIProcessor:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
    
    async def summarize(self, text):
        """Summarize the given text using Gemini"""
        prompt = f"""
        Please summarize the following text in approximately {Config.MAX_SUMMARY_LENGTH} characters,
        maintaining all key technical details and main points:

        {text}
        """
        response = await self.model.generate_content(prompt)
        return response.text
    
    async def translate(self, text):
        """Translate the given text to Japanese using Gemini"""
        prompt = f"""
        Please translate the following English text to Japanese.
        Maintain technical terms accuracy and natural Japanese flow:

        {text}
        """
        response = await self.model.generate_content(prompt)
        return response.text