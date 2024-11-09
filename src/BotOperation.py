import os
import google.generativeai as genai
from User import User
generation_config = {
  "temperature": 0.95,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

prompts = [
  "input: @kaithia create a new group with the group name MyGroup and Add user @mayur",
  "output: {\n    \"operation\": \"group\",\n    \"data\": {\n        \"group_name\": \"MyGroup\",\n        \"user_to_add\": [\"mayur\"]\n    }\n}",
  "input: @kaithia (Translate in Japanese) My Name is Mayur and I am a boy. i am creating this chatbot for myself",
  "output: {\n    \"operation\": \"translation\",\n    \"data\": {\n        \"original_message\": \"My Name is Mayur and I am a boy. i am creating this chatbot for myself\",\n        \"translated_message\": \"私の名前はマユールです。私は男の子です。私は自分のためにこのチャットボットを作っています。\"\n    }\n}",
  "input: @kathia Write a message to Hannah, telling her that I will attend tomorrow's prom night with her.",
  "output: { \"operation\": \"Generate-text\",\n    \"message\": \"Hey Hannah, just wanted to let you know that I’ll be attending tomorrow's prom night with you! Looking forward to it! 😊\"\n}",
  "input: @kaithia Summarise chat for me - {the chat is - {\n  \"chat_id\": 987654321,\n  \"participants\": [\n    { \"username\": \"@john\", \"name\": \"John\" },\n    { \"username\": \"@hannah\", \"name\": \"Hannah\" },\n    { \"username\": \"@mayur\", \"name\": \"Mayur\" },\n    { \"username\": \"@sarah\", \"name\": \"Sarah\" }\n  ],\n  \"messages\": [\n    {\n      \"sender\": \"@john\",\n      \"timestamp\": \"2024-10-18T09:30:00Z\",\n      \"message\": \"Hey everyone! With summer around the corner, I was wondering what the best places to visit are. Any suggestions?\"\n    },\n    {\n      \"sender\": \"@hannah\",\n      \"timestamp\": \"2024-10-18T09:32:00Z\",\n      \"message\": \"I think Bali is one of the best options! The beaches are stunning, and the culture is rich.\"\n    },\n    {\n      \"sender\": \"@mayur\",\n      \"timestamp\": \"2024-10-18T09:34:00Z\",\n      \"message\": \"Bali is amazing! I loved the Ubud area with all the rice terraces and the beautiful waterfalls.\"\n    },\n    {\n      \"sender\": \"@sarah\",\n      \"timestamp\": \"2024-10-18T09:35:00Z\",\n      \"message\": \"Don't forget about the food! Bali has some of the most delicious dishes. I could eat Nasi Goreng every day!\"\n    },\n    {\n      \"sender\": \"@john\",\n      \"timestamp\": \"2024-10-18T09:40:00Z\",\n      \"message\": \"Totally! The food scene in Bali is vibrant. But what do you guys think about Santorini? The sunsets there are breathtaking.\"\n    },\n    {\n      \"sender\": \"@hannah\",\n      \"timestamp\": \"2024-10-18T09:42:00Z\",\n      \"message\": \"Santorini is beautiful! But it can get super crowded in the summer. You have to plan ahead for the best spots!\"\n    },\n    {\n      \"sender\": \"@mayur\",\n      \"timestamp\": \"2024-10-18T09:45:00Z\",\n      \"message\": \"Good point! How about the Amalfi Coast in Italy? The views are stunning, and the food is top-notch.\"\n    },\n    {\n      \"sender\": \"@sarah\",\n      \"timestamp\": \"2024-10-18T09:48:00Z\",\n      \"message\": \"I love the Amalfi Coast! Positano is so picturesque. Perfect for a summer getaway!\"\n    },\n    {\n      \"sender\": \"@john\",\n      \"timestamp\": \"2024-10-18T09:50:00Z\",\n      \"message\": \"I've also heard great things about the beaches in Thailand. What do you think?\"\n    },\n    {\n      \"sender\": \"@hannah\",\n      \"timestamp\": \"2024-10-18T09:52:00Z\",\n      \"message\": \"Thailand is fantastic! Phuket is beautiful, but I really loved my time in Chiang Mai. It's a different vibe.\"\n    },\n    {\n      \"sender\": \"@mayur\",\n      \"timestamp\": \"2024-10-18T09:55:00Z\",\n      \"message\": \"Chiang Mai has such a rich culture. Plus, the temples are breathtaking. We should definitely consider it!\"\n    },\n    {\n      \"sender\": \"@sarah\",\n      \"timestamp\": \"2024-10-18T09:57:00Z\",\n      \"message\": \"And let's not forget the great street food in Thailand! You can get amazing meals at such low prices.\"\n    },\n    {\n      \"sender\": \"@john\",\n      \"timestamp\": \"2024-10-18T10:00:00Z\",\n      \"message\": \"So many options! What about a road trip along the California coast? The views are incredible!\"\n    },\n    {\n      \"sender\": \"@hannah\",\n      \"timestamp\": \"2024-10-18T10:02:00Z\",\n      \"message\": \"That sounds fun! The Pacific Coast Highway has some of the best scenery. We could hit up San Francisco and LA!\"\n    },\n    {\n      \"sender\": \"@mayur\",\n      \"timestamp\": \"2024-10-18T10:05:00Z\",\n      \"message\": \"And we could stop by some beaches along the way. It’s a great mix of city and nature.\"\n    },\n    {\n      \"sender\": \"@sarah\",\n      \"timestamp\": \"2024-10-18T10:07:00Z\",\n      \"message\": \"Definitely! We could even camp along the coast. Summer nights by the beach sound perfect!\"\n    },\n    {\n      \"sender\": \"@john\",\n      \"timestamp\": \"2024-10-18T10:10:00Z\",\n      \"message\": \"That would be an unforgettable trip! Let's keep all these ideas in mind. We can plan something together!\"\n    },\n    {\n      \"sender\": \"@hannah\",\n      \"timestamp\": \"2024-10-18T10:12:00Z\",\n      \"message\": \"For sure! I'm excited about all the possibilities. Let's make it happen!\"\n    },\n    {\n      \"sender\": \"@mayur\",\n      \"timestamp\": \"2024-10-18T10:15:00Z\",\n      \"message\": \"Agreed! Can’t wait for summer adventures! 🌞\"\n    }\n  ]\n}\n\n}",
  "output: {\"operation\": \"Summary\",\n  \"summary\": \"John, Hannah, Mayur, and Sarah discussed various summer travel destinations, highlighting Bali for its beaches and culture, Santorini for its sunsets (albeit crowded), the Amalfi Coast for its picturesque views, and Thailand for its rich culture and affordable street food. They also considered a road trip along the California coast, appreciating the scenic views and the idea of camping along the beaches. Overall, they expressed excitement about planning a memorable summer adventure together.\"\n}",
  "input: Hey guys, I was thinking that we should of gone to the beach this weekend, it would of been so fun. Also, I seen a great deal on some beach towels that we should buy. Let me know what you guys think! @kaithia Fix my text ,check grammar and wording",
  "output: {\n\"operation\": \"grammer\",\n  \"original_message\": \"Hey guys, I was thinking that we should of gone to the beach this weekend, it would of been so fun. Also, I seen a great deal on some beach towels that we should buy. Let me know what you guys think!\",\n  \"fixed_message\": \"Hey guys, I was thinking that we should have gone to the beach this weekend; it would have been so much fun. Also, I saw a great deal on some beach towels that we should buy. Let me know what you guys think!\"\n}",
 ]



def append_prompt(text, type="input"):
    prompts.append(f"{type}: {text}")

class BotOperation:
    def __init__(self, id, username):
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        self.user = User(id, username)
    
    def Generative(self, message):
        append_prompt(message, "input")
        response = model.generate_content(prompts)
        if response.status_code != 200:
            return "An error occurred while processing the request."
        
        append_prompt(response.text, "output")
        self.user.calculate_user_score(response.text.operation)
        return response.text
    
    def send_automated_message(self):
        pass
    
    def operation_type(self):
        pass
    
    def ImageGeneration(self):
        pass
    
    def ImageSummary(self):
        pass
    
    def other(self):
        pass