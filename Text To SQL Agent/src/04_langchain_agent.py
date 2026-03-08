import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, pipeline
from peft import PeftModel
from langchain_huggingface import HuggingFacePipeline
from langchain_community.utilities import SQLDatabase
from langchain_classic.chains import create_sql_query_chain
from langchain_core.prompts import PromptTemplate

# 1. Setup Exact Paths
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = f"sqlite:///{os.path.join(script_dir, '..', 'data', 'company_data.db')}"
adapter_path = os.path.join(script_dir, "..", "models", "qlora_adapters")

print("Loading Base Model & Weights...")

# 2. Load 4-bit Model
bnb_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16)

tokenizer = AutoTokenizer.from_pretrained(adapter_path)
base_model = AutoModelForCausalLM.from_pretrained(
    "unsloth/llama-3-8b-bnb-4bit",
    quantization_config=bnb_config,
    device_map="auto" 
)

print("Attaching Your Custom QLoRA Adapters...")
model = PeftModel.from_pretrained(base_model, adapter_path)

# 3. Setup LangChain Pipeline
print("Setting up LangChain Agent...")
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=50,
    temperature=0.1,  
    return_full_text=False
)
llm = HuggingFacePipeline(pipeline=pipe)

# 4. Connect to Local SQLite Database
db = SQLDatabase.from_uri(db_path)

# 5. Create Custom Prompt (Fixed for LangChain's strict variable requirements)
template = """### Instruction:
You are a SQL expert. Write a SQL query to answer the user's question based on the schema: {table_info}.
Limit your query to {top_k} results.

### Input:
{input}

### Response:
"""
prompt = PromptTemplate.from_template(template)

# 6. Create the autonomous chain
chain = create_sql_query_chain(llm, db, prompt=prompt)

print("\n" + "="*40)
print("🤖 AI SQL AGENT IS READY")
print("="*40)

# 7. Test the Agent
test_question = "What is the total sales amount for the North region?"
print(f"[User Query]: {test_question}\n")

try:
    print("Thinking & Generating SQL... (Might take 1-2 minutes on local hardware)")
    # Agent generates the query
    generated_sql = chain.invoke({"question": test_question})
    
    # Clean up formatting (Strips out English explanation so Database doesn't crash)
    clean_sql = generated_sql.replace("```sql", "").replace("```", "").strip()
    clean_sql = clean_sql.split("###")[0].strip() 
    
    print(f"[Agent Wrote SQL]: {clean_sql}")
    
    # Agent executes the query on the real database
    result = db.run(clean_sql)
    print(f"[Database Returned]: {result}")
    
except Exception as e:
    print(f"Error occurred: {e}")