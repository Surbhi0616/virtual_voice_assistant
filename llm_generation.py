import os
from groq import Groq
from rag_backend import query_knowledge_base

# Initialize the Groq Client with your actual API key
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "PLACEHOLDER_KEY")
client = Groq(api_key=GROQ_API_KEY)

def generate_voice_response(user_question):
    print("⏳ Step 1: Retrieving relevant documents from database...")
    matched_docs = query_knowledge_base(user_question)
    
    # Combine the top matching text pieces into a single context string
    context_text = ""
    if matched_docs:
        context_text = "\n\n".join([doc.page_content for doc in matched_docs])
    
    print("⏳ Step 2: Prompting cloud LLM (Llama 3 via Groq)...")
    
    # We are keeping your excellent system prompt exactly the same!
    system_prompt = f"""
    You are an advanced automated Voice Claims Assistant for an insurance provider.
    Your tone is warm, polite, empathetic, and highly professional.
    You have two modes of thinking: Chitchat Mode and Document Mode.
    
    MODE 1: CHITCHAT / GREETINGS
    If the user says something conversational (e.g., "hello", "how are you", "thank you", "okay", "goodbye"), 
    respond naturally, politely, and briefly using your own general knowledge. Do NOT use the policy context for greetings.
    
    MODE 2: POLICY QUESTIONS
    If the user asks a specific question about claims, coverage, forms, or rules, use the provided POLICY CONTEXT below.
    - Start your answer with a helpful, conversational opening sentence, then explain the rule.
    - Keep your entire response brief, natural, and conversational (2-4 sentences max).
    - Do NOT use bullet points, asterisks, formatting tags, or markdown symbols. Spell out numbers if necessary.
    - If the context completely lacks the answer to a specific policy question, say: "I am happy to help, but I am unable to locate that specific coverage rule in your policy files."
    
    POLICY CONTEXT FROM DOCUMENTS (Use ONLY for specific domain questions):
    {context_text}
    """
    
    # Call the lightning-fast cloud model using your API key
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_question}
        ],
        temperature=0.3,
        max_tokens=200
    )
    
    return completion.choices[0].message.content.strip()

if __name__ == "__main__":
    # Test conversational fallback
    print("\n--- RUNNING LOCAL TEST ---")
    print(generate_voice_response("how are you doing today?"))