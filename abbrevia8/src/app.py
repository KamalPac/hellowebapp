!pip3 install  -r  requirements.txt
#imports
from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
import pandas as pd
import json
from llama_index.llms import LlamaCPP
from llama_index.llms.llama_utils import messages_to_prompt, completion_to_prompt
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from llama_index import LangchainEmbedding, ServiceContext, Document
from llama_index import set_global_service_context

#Constants and global variables
s3_input_file_path ='s3://abb8-ml-model/dailydownload/mailContents.json'
s3_output_file_path ='s3://abb8-ml-model/dailydownload/insights.json'
s3_prompt_questions_path='./data/questions.json'

#read the docs and questions
docs = pd.read_json(s3_input_file_path)
docs.insert(3,"insight_dates","")
docs.insert(4,"summary","")
questions=pd.read_json(s3_prompt_questions_path)
print(docs.head(1))
print(questions.head(1))

#define service context
def get_service_context():    
    llm = LlamaCPP(
        # You can pass in the URL to a GGML model to download it automatically
        model_url=None,
        # optionally, you can set the path to a pre-downloaded model instead of model_url
        model_path='./models/zephyr-7b-alpha.Q5_K_M.gguf',
        temperature=0.1,
        max_new_tokens=256,
        # llama2 has a context window of 4096 tokens, but we set it lower to allow for some wiggle room
        context_window=3900,
        # kwargs to pass to __call__()
        generate_kwargs={},
        # kwargs to pass to __init__()
        # set to at least 1 to use GPU
        model_kwargs={"n_gpu_layers": -1},
        # transform inputs into Llama2 format
        messages_to_prompt=messages_to_prompt,
        completion_to_prompt=completion_to_prompt,
        verbose=True,
    )
    embed_model = LangchainEmbedding(
      HuggingFaceEmbeddings(model_name="thenlper/gte-large")
    )
    service_context = ServiceContext.from_defaults(
        chunk_size=256,
        llm=llm,
        embed_model=embed_model
    )
    return service_context

#Get insights
for index,row in docs.iterrows():
    if index >= 1:
        documents = []
        thread_id=row["thread_id"]
        thread_text=row["mail_body"]
        thread_subject=row["mail_subject"]
        #document = Document(text=thread_text,id_=thread_id,metadata={"subject":thread_subject})
        documents.append(
            Document(text=thread_text,id_=thread_id,metadata={"subject":thread_subject})
        )
        #print(documents)
        service_context=get_service_context();
        llamaindex=VectorStoreIndex.from_documents(documents,service_context=service_context)
        ##print(index.ref_doc_info)
        query_engine = llamaindex.as_query_engine(response_mode="compact")
        response = query_engine.query('''Give me info on the following points in JSON format-
                              person
                              meeting_date
                              place
                              ''')
        docs.at[index,'summary']=response
        print(response)
        #index.delete(thread_id)
print(docs.head(2))    
docs.to_json('s3://abb8-ml-model/dailydownload/insights.json',orient='records')

