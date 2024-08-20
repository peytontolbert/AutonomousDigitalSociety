import logging

# Set up basic logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def example_function(x):
    try:
        logging.info("example_function called with argument: %s", x)
        result = 10 / x
        logging.info("Result of division: %s", result)
        return result
    except ZeroDivisionError as e:
        logging.error("Error: Division by zero")
        return None
    except Exception as e:
        logging.error("An unexpected error occurred: %s", e)
        return None

# Example usage
example_function(5)
example_function(0)
