import random
import re
from fpdf import FPDF

class SupermarketBot:
    def __init__(self):
        self.exit_commands = ["exit", "quit", "bye", "goodbye", "leave", "stop"]
        self.greetings = [
            "Hello! How can I assist you with your shopping today?",
            "Hi there! Need help finding something in the supermarket?",
            "Hey! I'm here to help you locate items in the supermarket."
        ]
        self.responses = {
            "locate_item": "Sure, let me find that for you. The {item} is located at {location}.",
            "contact_info": {
                "customer service": "You can reach customer service at 123-456-7890.",
                "grocery department": "You can reach the grocery department at 987-654-3210.",
                "bakery": "You can reach the bakery at 555-555-5555.",
                "pharmacy": "You can reach the pharmacy at 444-444-4444."
            },
            "store_hours": "Our store is open from 8 AM to 10 PM, Monday to Sunday.",
            "special_offers": "We have various items on sale this week! Check the flyer at the entrance for the latest deals.",
            "store_location": "We are located at 123 Main Street, downtown. You can't miss us!",
            "product_availability": "Let me check the stock for you. Please wait a moment.",
            "thanks": "You're welcome! Is there anything else I can help you with today?",
            "goodbye": "Thank you for using Supermarket Bot. Have a great day!"
        }
        self.good_locations = {
            "bread": "Aisle 1, Shelf B",
            "milk": "Aisle 2, Shelf A",
            "eggs": "Aisle 2, Shelf B",
            "cheese": "Aisle 3, Shelf C",
            "vegetables": "Aisle 1, Shelf D",
            "fruits": "Aisle 1, Shelf E",
            "snacks": "Aisle 3, Shelf A"
        }
        self.intent_patterns = {
            'store_hours_intent': r'.*\b(store hours|opening hours)\b.*',
            'special_offers_intent': r'.*\b(special offers|sales)\b.*',
            'store_location_intent': r'.*\b(location|address|store located)\b.*',
            'product_availability_intent': r'.*\b(availability)\b.*',
            'thanks_intent': r'.*\b(thank you|thanks)\b.*',
            'goodbye_intent': r'.*\b(exit|quit|bye|goodbye|leave|stop)\b.*',
            'contact_info_intent': r'.*\b(contact|phone|number|call)\b.*'
        }
        self.pdf = FPDF()

    def greet(self):
        print(random.choice(self.greetings))

    def make_exit(self, reply):
        return reply.lower() in self.exit_commands

    def find_location(self, item):
        if item in self.good_locations:
            return f"The {item} is located at {self.good_locations[item]}"
        else:
            return f"Sorry, I couldn't find the location for {item}. Please check with our staff."

    def generate_pdf(self, items):
        self.pdf.add_page()
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(200, 10, txt="Supermarket Shopping List", ln=True, align='C')
        self.pdf.set_font('Arial', size=10)
        for item in items:
            location = self.find_location(item)
            self.pdf.cell(200, 10, txt=f"{item}: {location}", ln=True)

        self.pdf.output("shopping_list.pdf")

    def match_reply(self, reply):
        for key, value in self.intent_patterns.items():
            intent = key
            regex_pattern = value
            found_match = re.match(regex_pattern, reply)
            if found_match:
                if intent == 'store_hours_intent':
                    return self.store_hours_intent()
                elif intent == 'special_offers_intent':
                    return self.special_offers_intent()
                elif intent == 'store_location_intent':
                    return self.store_location_intent()
                elif intent == 'product_availability_intent':
                    return self.product_availability_intent()
                elif intent == 'thanks_intent':
                    return self.thanks_intent()
                elif intent == 'goodbye_intent':
                    return self.goodbye_intent()
                elif intent == 'contact_info_intent':
                    return self.contact_info_intent(reply)
        return None

    def store_hours_intent(self):
        return self.responses["store_hours"]

    def special_offers_intent(self):
        return self.responses["special_offers"]

    def store_location_intent(self):
        return self.responses["store_location"]

    def product_availability_intent(self):
        return self.responses["product_availability"]

    def thanks_intent(self):
        return self.responses["thanks"]

    def goodbye_intent(self):
        return self.responses["goodbye"]

    def contact_info_intent(self, reply):
        if 'customer service' in reply:
            return self.responses["contact_info"]["customer service"]
        elif 'grocery department' in reply:
            return self.responses["contact_info"]["grocery department"]
        elif 'bakery' in reply:
            return self.responses["contact_info"]["bakery"]
        elif 'pharmacy' in reply:
            return self.responses["contact_info"]["pharmacy"]
        else:
            return "Sorry, I couldn't find the contact information you're looking for. Please check with our staff."

    def no_match_intent(self):
        return "Sorry, I didn't understand that. Can you please rephrase?"

    def chat(self):
        self.greet()
        shopping_list = []
        while True:
            user_input = input("What do you need today? (Separate items with commas or type 'exit' to finish)\n").lower()
            if self.make_exit(user_input):
                print(self.goodbye_intent())
                break

            response = self.match_reply(user_input)
            if response:
                print(response)
                if response == self.responses["goodbye"]:
                    break
            else:
                items = [item.strip() for item in user_input.split(',')]
                for item in items:
                    location = self.find_location(item)
                    if "Sorry" not in location:
                        print(self.responses["locate_item"].format(item=item, location=self.good_locations[item]))
                        shopping_list.append(item)
                    else:
                        print(location)

        if shopping_list:
            print("Generating your shopping list PDF...")
            self.generate_pdf(shopping_list)


if __name__ == "__main__":
    supermarket_bot = SupermarketBot()
    supermarket_bot.chat()
