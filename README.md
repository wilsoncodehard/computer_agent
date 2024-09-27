# computer_agent
## 簡介
使用LLM跟命令列指令，使電腦可自動新增資料夾、打開軟體...之類的


## Code
### 架Server
使用 **Fastchat**，結合**OpenAI API**。
```
pip install fastchat accelerate
```
1.Run the controller ( on port 21001 )
```
python -m fastchat.serve.controller --host 0.0.0.0 --port 21001
```
![image](https://hackmd.io/_uploads/Skb-2wbT0.png)

>[!Tip]
>這些port好像都不能亂調的樣子，原本改為3001但request還是發到21001...Weird LoL

2.Run the worker  ( on port 21002 )
```
python3 -m fastchat.serve.model_worker \
    --model-names YOUR_MODELS_NAME \
    --model-path YOUR_MODELS_PATH \
    --worker-address http://localhost:21002 \
    --controller-address http://localhost:21001 \
    --host 0.0.0.0 --num-gpus 2
```
![image](https://hackmd.io/_uploads/ByLQ2D-6A.png)

>[!Note]
>--num-gpus 2: Using 2 GPUs to run the whole model

>[!Tip]
>
3. OpenAI API Server
```
python3 -m fastchat.serve.openai_api_server --host localhost --port 8000
```
![image](https://hackmd.io/_uploads/Hy4rhPZT0.png)
當今天送出一個問題後他並不會有動作，只有在回答完成後會顯示POST ... 200 OK
![image](https://hackmd.io/_uploads/S1wJjdbaA.png)

架設完畢，接下來設定模型的部分。

### Setting model
自己本地端的:
```
python3 -m fastchat.serve.model_worker \
    --model-names Meta-Llama-3-8B-Instruct \
    --model-path /media/hdd/wilson/.cache/huggingface/hub/models--meta-llama--Meta-Llama-3-8B-Instruct/snapshots/e1945c40cd546c78e41f1151f4db032b271faeaa \
    --worker-address http://localhost:21002 \
    --controller-address http://localhost:21001 \
    --host 0.0.0.0 --num-gpus 2
```
目前已使用
- [x] llama3-8b
- [x] llama3-8b-Instruct
- [ ] Llama-3-Taiwan-70B-Instruct 

目前前兩個效果顯著不彰。即使用英文也不行，重複內容且無法完全理解文體。

在生成部分已完成可以將回答一個字一個字生出來的stream。
```
def generate_response(prompt):
    try:
        # 呼叫 OpenAI API，生成串流回應
        response = openai.chat.completions.create(
            model=model,    
            messages=prompt,
            temperature=0.7,
            top_p=1,
            max_tokens=512,
            stream=True  # 開啟串流模式
        )
        reply = ""
        print(f"ANS:{reply}")

        # 逐步處理和顯示回應
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                chunk_message = chunk.choices[0].delta.content
                print(chunk_message, end='', flush=True)  # 即時輸出每個片段
                reply += chunk_message
        
```