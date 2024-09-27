# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("yentinglin/Llama-3-Taiwan-8B-Instruct")
model = AutoModelForCausalLM.from_pretrained("yentinglin/Llama-3-Taiwan-8B-Instruct")