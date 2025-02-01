import json
import pytest
import logging
from duauto.web_driver_manager import WebDriverManager
from duauto.actions import Actions
from duauto.assertions import Assertions

print("hello")
# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@pytest.fixture(scope="module")
def setup_driver():
    """
    Initializes the WebDriver and provides it to the test.
    Closes the WebDriver instance after the test module completes.
    """
    logging.info("Initializing WebDriver...")
    driver = WebDriverManager.create_driver(headless=True)
    yield driver
    logging.info("Closing WebDriver...")
    driver.quit()

@pytest.mark.parametrize("config_file", ["test.json"])  # Run tests for each JSON file
def test_run_test_from_config(setup_driver, config_file):
    """
    Runs the test based on the configuration from the given JSON file.

    :param config_file: Path to the JSON configuration file.
    :param setup_driver: Pytest fixture providing the WebDriver instance.
    """
    logging.info(f"Running test using config file: {config_file}")

    with open(config_file) as file:
        config = json.load(file)

    driver = setup_driver
    driver.get(config["url"])
    logging.info(f"Navigated to URL: {config['url']}")

    # Initialize Actions and Assertions
    actions = Actions(driver)
    assertions = Assertions(driver)

    # Perform actions
    for action in config["actions"]:
        locator_type = action["locator_type"]
        locator = action["locator"]

        if action["action"] == "input_text":
            actions.input_text(locator_type, locator, action["value"])
            logging.info(f"Entered text: {action['value']} into {locator}")
        elif action["action"] == "click_element":
            actions.click_element(locator_type, locator)
            logging.info(f"Clicked element: {locator}")
        elif action["action"] == "find_elements_and_click":
            index = int(action.get("index", 0))
            actions.find_elements_and_click(locator_type, locator, index)
            logging.info(f"Clicked element at index {index} for {locator}")
        elif action["action"] == "send_keys":
            input_key = action["value"]
            actions.send_keys(locator_type, locator, input_key)
            logging.info(f"Sent keys: {input_key} to {locator}")
        elif action["action"] == "switch_to_iframe_by_element":
            actions.switch_to_iframe_by_element(locator_type, locator)
            logging.info(f"Switched to iframe: {locator}")

    # Perform assertions
    for assertion in config["assertions"]:
        locator_type = assertion.get("locator_type")
        locator = assertion.get("locator")
        expected = assertion.get("expected")

        if assertion["action"] == "assert_title":
            assertions.assert_title(expected)
            logging.info(f"Title assertion passed: {expected}")
        elif assertion["action"] == "assert_element_text":
            assertions.assert_element_text(locator_type, locator, expected)
            logging.info(f"Text assertion passed: {expected}")
        elif assertion["action"] == "assert_element_visible":
            assertions.assert_element_visible(locator_type, locator)
            logging.info(f"Visibility assertion passed: {locator}")
        elif assertion["action"] == "assert_element_exists":
            assertions.assert_element_is_present(locator_type, locator)
            logging.info(f"Element existence assertion passed: {locator}")
        elif assertion["action"] == "assert_element_attribute":
            attribute = assertion.get("attribute")
            assertions.assert_element_attribute(locator_type, locator, attribute, expected)
            logging.info(f"Attribute assertion passed: {locator} {attribute}={expected}")
        elif assertion["action"] == "assert_url":
            assertions.assert_url(expected)
            logging.info(f"URL assertion passed: {expected}")
        elif assertion["action"] == "assert_element_not_visible":
            assertions.assert_element_not_visible(locator_type, locator)
            logging.info(f"Element not visible assertion passed: {locator}")
        elif assertion["action"] == "assert_element_not_present":
            assertions.assert_element_not_present(locator_type, locator)
            logging.info(f"Element not present assertion passed: {locator}")

    logging.info("Test completed successfully.")
