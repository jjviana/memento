# Import the unittest module and the IncludeTemplate class
import sys
sys.path.append('.')
import os
import unittest
from template import IncludeTemplate

# Define a test case class that inherits from unittest.TestCase
class TestIncludeTemplate(unittest.TestCase):

    # Define a setup method that runs before each test
    def setUp(self):
        # Create some sample templates and mappings for testing
        self.template1 = IncludeTemplate("Hello, ${name}!")
        self.mapping1 = {"name": "Alice"}
        self.template2 = IncludeTemplate("This is a ${include:test.txt} template.")
        self.mapping2 = {"foo": "bar"}
        # Create a file named test.txt with some content
        os.makedirs("templates",exist_ok=True)
        with open("templates/test.txt", "w") as f:
            f.write("nested ${foo}")

    # Define a teardown method that runs after each test
    def tearDown(self):
        # Delete the file named test.txt
        import os
        os.remove("templates/test.txt")

    # Define a test method that checks the basic functionality of the substitute method
    def test_substitute_basic(self):
        # Call the substitute method on the first template and mapping
        result = self.template1.substitute(self.mapping1)
        # Assert that the result is equal to the expected string
        self.assertEqual(result, "Hello, Alice!")

    # Define a test method that checks the include functionality of the substitute method
    def test_substitute_include(self):
        # Call the substitute method on the second template and mapping
        result = self.template2.substitute(self.mapping2)
        # Assert that the result is equal to the expected string
        self.assertEqual(result, "This is a nested bar template.")

# Run the tests if this file is executed as a script
if __name__ == "__main__":
    unittest.main()
