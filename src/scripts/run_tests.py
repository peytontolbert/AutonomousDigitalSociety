import os
from dotenv import load_dotenv
import unittest

# Load environment variables from .env file
load_dotenv()

# Run the tests
if __name__ == "__main__":
    unittest.main(module="test_project")
