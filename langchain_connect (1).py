from fastapi import FastAPI
from langchain import OpenAI, SQLDatabase
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from langchain.llms.openai import OpenAI
from langchain.chains import SQLDatabaseSequentialChain

app = FastAPI()

conversation = []

qa_prompt = '''You are an helpful assistant.Please provide the answer for the question in a friendly manner.Start answer with connection words.The interaction must be Conversational.
Format your responses as a friendly assistant would.Avoid the repeatation of connected words.Answer must be from the connected database.Your goal is to have a conversational interaction, answer user questions, and sometime inquire about their preferences.
Respond to user-specific questions. If any greetings message, respond with greetings.

{context} 

Question: {question}
Answer:'''
@app.post("/db_connectivity")
async def plan_details(user_question: str):
    try:
        engine = create_engine("postgresql+psycopg2://postgres:%s@3.238.31.101:5432/postgres" % quote_plus("password-pgadmin"))
        db = SQLDatabase(engine, include_tables=["price_plan_details","sign_up","chat_history_logs"])
        llm = OpenAI(temperature=0, openai_api_key="")
        db_chain = SQLDatabaseSequentialChain.from_llm(llm=llm, database=db, verbose=True)

        context = ""  # Remove conversation context if not needed
        prompt = qa_prompt.format(context=context, question=user_question)
        
        # response = db_chain.run(prompt)
        response_message = "Thank you for providing your details. Your bot will be ready within 24 hours."
        # return {"user_question": user_question, "response": str(response)}
        return {"user_question": user_question, "response": response_message}
    except Exception as e:
        return {"error": str(e)}


    #     
    #     response = db_chain.run(user_question)
    #     return {"response": str(response)}
    # except Exception as e:
    #         return {"error": str(e)}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)