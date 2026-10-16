from langgraph_sdk import get_client
import asyncio
# Va se connecter à l'agent en local
# Vous pouvez aussi tester avec l'adresse Render
import asyncio
# Va se connecter à l'agent en local
# Vous pouvez aussi tester avec l'adresse Render
client = get_client(
    #url="http://127.0.0.1:2024"
    url="https://raux-pascal-formation-langchain-j3.onrender.com"
    )
# Get stream
async def call():
    all_assistants = await client.assistants.search()
    print(
        "Available assistants: ", 
        "\n-".join(
            [""]
            + [f"{a.get("name", None)} ({a.get("graph_id", None)}):\n\t" 
            + ('\n\t'.join(f"{k}: {v}" for k, v in a.items()))
                for a in all_assistants
               ]
        )
        
        )
    async for chunk in client.runs.stream(
        None, # Threadless run
        "agent", # Name of assistant. Defined in langgraph.json.
        input={
            "messages": [{
                "role": "human",
                "content": "What is LangGraph?",
                }],
            },
        stream_mode="updates",
        ):
        print(f"Receiving chunk (type: {chunk.event}):")
        print(chunk.data)
        print("\n\n")

if __name__ == "__main__":
    asyncio.run(call())