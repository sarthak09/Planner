from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from Logger import Logger
from custom_exception import CustomException
import os

load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")
if groq_key:
    os.environ["GROQ_API_KEY"] = groq_key

class AIPlanner:
    def __init__(self, logger, city: str = "India", interests: str = "art, history, food", model_name: str = "groq:llama-3.1-8b-instant"):
        self.logger = logger
        self.logger.info("Initializing TravelPlanner instance")
        self.city = city
        self.interests = interests
        self.llm = init_chat_model(model=model_name)
        self.logger.info("Initialized llm instance")
        
        # Create a prompt template with placeholders for dynamic city and interests
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful travel assistant. Create a day trip itinerary for {city} based on user's interests: {interests}. Provide a brief, bulleted itinerary with specific recommendations."),
            ("human", "Create an itinerary for my day trip to {city} focusing on {interests}.")
        ])
        self.logger.info("Initialized TravelPlanner instance")

    def printDetails(self):
        print(f"City: {self.city}")
        print(f"Interests: {self.interests}")
        print(f"Prompt template: {self.prompt_template}")

    def run_model(self):
        response = self.llm.invoke("How are you?")
        return response

    def generate_itinerary(self, city=None, interests=None):
        """Generate formatted prompt for given city and interests"""
        city = city or self.city
        interests = interests or self.interests
        return self.prompt_template.format(city=city, interests=interests)

    def runAi(self, city, interests):
        try:
            self.logger.info(f"Generating itinerary for {city} with interests: {interests}")
            
            # Format the prompt with the actual city and interests from the request
            formatted_prompt = self.prompt_template.format_messages(
                city=city,
                interests=interests
            )
            
            # Invoke the LLM with the formatted prompt
            response = self.llm.invoke(formatted_prompt)
            
            self.logger.info("Itinerary generated successfully")
            return response
            
        except Exception as e:
            self.logger.error(f"Error while creating itinerary: {e}")
            raise CustomException("Failed to create itinerary", e)


if __name__ == "__main__":
    from Logger import Logger
    logger = Logger.get_logger(__name__)
    planner = AIPlanner(logger=logger, city="India", interests="art, history, food", model_name="groq:llama-3.1-8b-instant")
    print(planner.printDetails())
    print(planner.run_model())
    itinerary = planner.generate_itinerary(city="Paris", interests="art, museums, food")
    print("Generated Itinerary:")
    print(itinerary)
    ai_response = planner.runAi(city="Paris", interests="art, history, food")
    print("AI Response:")
    print(ai_response.content)