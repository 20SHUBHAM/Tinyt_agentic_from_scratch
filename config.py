import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4')
    
    # TinyTroupe Configuration
    TINYTROUPE_CACHE_DIR = os.getenv('TINYTROUPE_CACHE_DIR', './cache')
    
    # Flask Configuration
    FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-key-change-in-production')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
    
    # Agent Configuration
    MAX_PERSONAS = int(os.getenv('MAX_PERSONAS', 8))
    MAX_DISCUSSION_ROUNDS = int(os.getenv('MAX_DISCUSSION_ROUNDS', 10))
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        return True