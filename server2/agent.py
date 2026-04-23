# from langchain_ollama import ChatOllama
# from langchain_core.messages import HumanMessage, SystemMessage
# import pyomo.environ as pyo
# import io
# import contextlib

# Configuração do LLM
def orquestrador_po(prompt_problema: str):
    return "ola mundo"
    # llm = ChatOllama(model="tinyllama", base_url="http://ollama:11434", request_timeout=60.0)
    
    # system_prompt = "..." # (seu prompt original)
    
    # print(f"--- DEBUG: Enviando prompt para LLM ---")
    # response = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=prompt_problema)])
    
    # codigo = response.content.replace("```python", "").replace("```", "").strip()
    # print(f"--- DEBUG: Código gerado pelo LLM ---")
    # print(codigo) # Se isso estiver vazio, o LLM falhou
    
    # if not codigo:
    #     return "Erro: O LLM não gerou nenhum código."

    # output_capture = io.StringIO()
    # with contextlib.redirect_stdout(output_capture):
    #     try:
    #         namespace = {'pyo': pyo}
    #         # Adicionamos um print aqui para confirmar que o exec() começou
    #         print("Executando código...") 
    #         exec(codigo, namespace)
    #     except Exception as e:
    #         # Captura erros de sintaxe ou execução do Pyomo
    #         return f"Erro na execução do modelo: {str(e)}"
            
    # return output_capture.getvalue()

