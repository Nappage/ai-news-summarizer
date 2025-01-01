# Security Policy

## API Keys and Sensitive Data

1. **Environment Variables**
   - Never commit `.env` files to the repository
   - Use `.env.example` as a template for required environment variables
   - When using Google Colab, use the built-in Secrets management

2. **Output Directory**
   - The `output/` directory is git-ignored except for `.gitkeep`
   - Regularly review generated content for sensitive information
   - Do not commit any generated files

3. **API Key Management**
   - Store the API key as `GOOGLE_API_KEY` in your environment
   - Never hard-code API keys in the source code
   - Regularly rotate API keys for security

4. **Local Development**
   - Copy `.env.example` to `.env` and add your API key
   - Ensure `.env` is in `.gitignore`
   - Use virtual environment to isolate dependencies

5. **Colab Environment**
   - Use Colab's Secrets management for API keys
   - Clear output cells before sharing notebooks
   - Do not store API keys in notebook cells

## Reporting Security Issues

If you discover a security vulnerability, please report it via email or GitHub security advisories. Do not create public issues for security vulnerabilities.