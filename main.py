import openai
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live

# 設定 OpenAI API 的基礎配置
openai.api_key = "EMPTY"
openai.base_url = "http://localhost:8000/v1/"
model = "Llama-3-Taiwan-8B-Instruct"

# 初始化 rich 的 Console
console = Console()

def generate_response(system, prompt):
    sys_prompt = f"""
        你是一個強大的{system}助手,你可以生成精確的程式碼以利使用者打開他們電腦上的任何應用。
        比如使用者輸入:「打開Google搜尋Machine Learning」
        你會自動生成對應的程式碼,以利{system}上的命令列執行命令。
        其中,程式碼的部分皆以"```"包住,且```會同時生成,不會分開生成。
        所有生成都會以Markdown格式呈現,且若前面或後面有程式碼(```)會自動換行，
        且不會重複生成意思相近的句子。
    """
    try:
        # 呼叫 OpenAI API，生成串流回應
        response = openai.chat.completions.create(
            model=model,    
            messages=[
                {"role":"system","content":sys_prompt},
                {"role":"user","content":prompt},
            ],
            temperature=0.7,
            top_p=0.8,
            max_tokens=512,
            stream=True  # 開啟串流模式
        )
        print("Reponse:") 
        
        buffer = ""


        # Using Live to handle dynamic updates
        with Live(console=console, refresh_per_second=10, transient=True) as live:
            for chunk in response:
                # Get the content from the chunk
                if chunk.choices[0].delta.content is not None:
                    chunk_message = chunk.choices[0].delta.content
                    #print(chunk_message, end='', flush=True)  # 即時輸出每個片段
                    buffer += chunk_message

                # Update the live display with the new content
                live.update(Markdown(buffer))

            # After the loop, print the final content
            console.print(Markdown(buffer))


    except Exception as e:
        buffer = f"Error: {str(e)}"


# 主程式
def main():
    system = input("請選擇使用系統:(L for Linux, W for Windows):")
    if(system == 'L'):
        system = "Linux"
    else:
        system = "Windows"
    print("請輸入指令 (輸入 'e' 來退出):")
    
    while True:
        # 嵌入你的範例內容到此處
        user_input = input(f"({system}) > ")
        if user_input == "e":
            print("Goodbye！")
            break
        
        generate_response(system, user_input)

if __name__ == "__main__":
    main()
