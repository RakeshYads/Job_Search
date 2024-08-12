# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import Restarted, AllSlotsReset
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class ActionGreet(Action):
    def name(self) -> Text:
        return "action_greet"

    def run(self, dispatcher: CollectingDispatcher,
                        tracker: Tracker,
                        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if (user := tracker.get_slot("user")):
            dispatcher.utter_message(f"Hey {user}! How are you?")
        else:
            dispatcher.utter_message("Hi, How are you?")

        return []

class EndChat(Action):
    def name(self) -> Text:
        return "action_end_chat"

    async def run(self, dispatcher: CollectingDispatcher,
                        tracker: Tracker,
                        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if (user := tracker.get_slot("user")):

            dispatcher.utter_message(f"Goodbye {user}! It was nice talking with you")
        else:
            dispatcher.utter_message("Goodbye! It was nice talking with you")

        # Reset the tracker
        # tracker.reset()

        return [AllSlotsReset(),Restarted()]

class JobLocation(Action):
    def name(self) -> Text:
        return "action_job_location"

    async def run(self, dispatcher: CollectingDispatcher,
                        tracker: Tracker,
                        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        location = tracker.get_slot("location")
        jobtitle = tracker.get_slot("job_title")
        if (location != None or jobtitle != None):
            # data = {"location" : location, "jobtitle" : jobtitle}
            # dispatcher.utter_message(data)
            dispatcher.utter_message(
                template = "utter_job_details",
                jobtitle = jobtitle,
                location = location
            )
        else:
            dispatcher.utter_message("Required data point is not provided.")

        return []

