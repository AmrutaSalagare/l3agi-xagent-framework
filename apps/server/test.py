import os
import sys
from langchain.smith import RunEvalConfig, run_on_dataset
from langchain_community.chat_models import ChatOpenAI
from langsmith import Client

# Add XAgent to Python path
xagent_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'XAgent')
if xagent_path not in sys.path:
    sys.path.insert(0, xagent_path)

from agents.xagent_integration import L3AGIXAgentAdapter

# TODO: refactor test to use new auth

# res = requests.post(
#     f"{Config.L3_AUTH_API_URL}/auth/login",
#     json={"email": Config.TEST_USER_EMAIL, "password": Config.TEST_USER_PASSWORD},
#     timeout=30,
# )

# auth_data = res.json()

# headers = {
#     "authorization": auth_data["access_token"],
#     "x-refresh-token": auth_data["refresh_token"],
# }


def agent_factory():
    """
    Factory function to create XAgent-based agent for testing
    """
    try:
        # Create XAgent adapter for testing
        xagent_adapter = L3AGIXAgentAdapter(
            config={
                "model_name": "gpt-3.5-turbo",
                "temperature": 0.0
            },
            tools=[],  # Add tools as needed for testing
            system_message="You are a helpful assistant that can answer questions and perform tasks.",
            memory=None
        )
        
        return xagent_adapter
    except Exception as e:
        print(f"Error creating XAgent: {e}")
        return None


agent = agent_factory()

client = Client()


eval_config = RunEvalConfig(
    evaluators=[
        "qa",
        RunEvalConfig.Criteria("helpfulness"),
        RunEvalConfig.Criteria("conciseness"),
    ],
    input_key="input",
    eval_llm=ChatOpenAI(temperature=0.5, model_name="gpt-3.5-turbo"),
)

chain_results = run_on_dataset(
    client,
    dataset_name="test-dataset",
    llm_or_chain_factory=agent_factory,
    evaluation=eval_config,
    concurrency_level=1,
    verbose=True,
)
