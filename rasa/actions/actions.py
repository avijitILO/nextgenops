from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests
import json

class ActionCreateTicket(Action):
    def name(self) -> Text:
        return "action_create_ticket"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get user information from slots
        name = tracker.get_slot("name")
        email = tracker.get_slot("email")
        issue_type = tracker.get_slot("issue_type")
        
        # Create ticket in Zammad
        ticket_data = {
            "title": f"New ticket from {name}",
            "article": {
                "subject": f"Issue: {issue_type}",
                "body": f"Ticket created by chatbot for user: {name} ({email})",
                "type": "note",
                "internal": False
            },
            "customer": email,
            "group": "Users",
            "priority": "2 normal",
            "state": "new"
        }
        
        try:
            # Make API call to Zammad
            response = requests.post(
                "http://zammad-nginx:80/api/v1/tickets",
                json=ticket_data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Token YOUR_ZAMMAD_API_TOKEN"
                }
            )
            
            if response.status_code == 201:
                ticket_id = response.json()["id"]
                dispatcher.utter_message(
                    text=f"Ticket #{ticket_id} has been created successfully! We'll get back to you soon."
                )
            else:
                dispatcher.utter_message(
                    text="Sorry, there was an error creating your ticket. Please try again."
                )
                
        except Exception as e:
            dispatcher.utter_message(
                text="Sorry, I'm having trouble creating your ticket right now."
            )
        
        return []

class ActionSearchKnowledge(Action):
    def name(self) -> Text:
        return "action_search_knowledge"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get the user's question
        user_message = tracker.latest_message.get("text")
        
        try:
            # Search in Haystack
            search_data = {
                "query": user_message,
                "params": {
                    "Retriever": {
                        "top_k": 3
                    }
                }
            }
            
            response = requests.post(
                "http://haystack:8001/query",
                json=search_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                results = response.json()
                if results.get("answers"):
                    answer = results["answers"][0]["answer"]
                    dispatcher.utter_message(text=f"I found this information: {answer}")
                else:
                    dispatcher.utter_message(
                        text="I couldn't find specific information about that. Would you like me to create a ticket for you?"
                    )
            else:
                dispatcher.utter_message(
                    text="Sorry, I'm having trouble searching right now."
                )
                
        except Exception as e:
            dispatcher.utter_message(
                text="I'm having trouble accessing the knowledge base right now."
            )
        
        return []
