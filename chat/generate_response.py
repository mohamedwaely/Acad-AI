from app.models import User
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os
from together import AsyncTogether
load_dotenv()

# client = ChatCompletionsClient(
#     endpoint=os.getenv("endpoint"),
#     credential=AzureKeyCredential(os.getenv("token")),
# )

client = AsyncTogether(
    api_key=os.getenv("togetherAPI")
)

system_prompt = """
You are a helpful assistant that provides information about graduation projects. Follow these steps for every user question:

1. -Understand the Question: Analyze the user's question to identify their perspective (e.g., investor, student, general user) and intent (e.g., seeking info, asking for suggestions).
2. -Provide Context-Based Response: First, provide relevant information from the given context about existing graduation projects. Summarize key details that relate to the question, such as project goals, technologies, or outcomes.
3. -Offer Suggestions (if applicable): If the user is asking for suggestions (e.g., project ideas), *after* providing the context-based response, generate tailored project ideas inspired by the context. Clearly separate this section with a header like "### Suggested Project Ideas".

Guidelines:
- For investors: Focus on business potential, market opportunities, and ROI.
- For students: Provide technical details and learning insights.
- For general users: Explain in accessible terms with practical applications.
- If unsure of the user type, provide a balanced response.
- If the question is unrelated to the context, respond: "I don't have information about that." only
- Do not skip the context-based response unless no relevant context or question is provided.
- If the question started with welcoming words, respond with a welcoming message and then provide the response.
"""


from fastapi import HTTPException
async def llm_response(query: str, projects: list) -> str:
    try:
        if not query:
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        if not projects:
            raise HTTPException(status_code=400, detail="No projects provided")

        context = "\n".join(
            f"- title: {proj.title}, description: {proj.description}, "
            f"supervisor: {proj.supervisor}, tools: {proj.tools}, "
            f"Year: {proj.year}"
            for proj in projects
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Question: {query}\nContext: {context}"}
        ]

        # response = client.complete(
        #     messages=messages,
        #     model=os.getenv("model_name"),
        # )

        stream = await client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            messages=messages,
            stream=True
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

        yield "[DONE]"
        # if not response or not response.choices:
        #     raise HTTPException(status_code=500, detail="No response received from LLM")

        # return response.choices[0].message.content

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

