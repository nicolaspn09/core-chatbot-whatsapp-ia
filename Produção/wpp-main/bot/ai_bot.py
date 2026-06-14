import os
from decouple import config # Busca a variável de ambiente
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq # Busca os modelos do groq
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage, AIMessage
from langchain_huggingface import HuggingFaceEmbeddings

# Comunica com o groq
os.environ["GROQ_API_KEY"] = config("GROQ_API_KEY")

# Classe do bot
class AIBot():    
    # Inicializador
    def __init__(self):
        # Cria o modelo do Groq
        self.__chat = ChatGroq(model="llama-3.1-70b-versatile")
        # Cria um retriever, uma instância do banco de dadosd
        self.__retriever = self.__build_retriever()

    # Localiza o banco de dados e busca as informações conforme o prompt
    def __build_retriever(self):
        # Informa o local do banco de dados
        # persist_directory = "/ChatBotWhats/chroma_data"
        persist_directory = "/ChatBotWhats/chroma_data_invest"
        # Busca as informações relevantes
        embedding = HuggingFaceEmbeddings()

        vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=embedding,
        )

        return vector_store.as_retriever(
            search_kwargs={"k": 30}, # Busca até 30 resultados no máximo
        )

    def __build_messages(self, history_messages, question):
        # Garantir que history_messages não seja None
        if history_messages is None:
            history_messages = []

        messages = []

        # Construir a lista de mensagens a partir do histórico
        for message in history_messages:
            # Verifica se a chave 'fromMe' está presente no dicionário
            message_class = HumanMessage if message.get("fromMe") else AIMessage
            messages.append(message_class(content=message.get("body", "")))

        # Adiciona a mensagem atual (pergunta)
        messages.append(HumanMessage(content=question))

        return messages

    # Recebe a mensagem do usuário e processa a partir de um prompt
    def invoke(self, history_messages, question):
        # VIÉS DO PDF DA IDEIA COMPANY_NAME
        # SYSTEM_TEMPLATE = """
        # Responda as perguntas do usuário conforme o contexto abaixo:
        # Você é um assistente especializado para tirar dúvidas sobre uma ideia de automação.
        # Tire as possíveis dúvidas das pessoas que entrarem em contato conosco.
        # Responda de forma natural, agradável e respeitosa. Seja objetivo nas respostas, com informações claras e diretas. Foque em ser natural e humanizado, como um diálogo comum entre duas pessoas.
        # Leve em consideração também o histórico de mensagens de conversa com o usuário.
        # Responda sempre em português brasileiro.

        # <context>
        # {context}
        # </context>
        # """

        # VIÉS DE INVESTIMENTOS
        # SYSTEM_TEMPLATE = """
        # Você é um assistente especializado em investimentos financeiros. Seu objetivo é ajudar os usuários com perguntas sobre reserva de emergência, perfis de risco e carteiras de investimentos. Responda com base no contexto a seguir.

        # Caso a pergunta seja sobre reserva de emergência, forneça a recomendação de cálculo de acordo com os seguintes passos:
        # - Pergunte sobre os gastos fixos mensais.
        # - Se o usuário já possui reserva de emergência, informe que o valor da reserva deve ser 5 vezes os gastos fixos mensais.

        # Caso a pergunta seja sobre perfil de risco, forneça a recomendação conforme a seguinte lógica:
        # - Se o usuário disser que "tiraria tudo", recomende **somente renda fixa**.
        # - Se o usuário disser "não mexer", recomende **ações**.
        # - Se o usuário disser "apostar mais", recomende **ações e criptomoedas**.

        # Caso a pergunta seja sobre carteiras de investimento, forneça a recomendação de acordo com o perfil do usuário:
        # - **Carteira Conservadora**: 85% Renda Fixa, 15% Ações (IVVB11 e BOVA11)
        # - **Carteira Moderada**: 65% Renda Fixa, 30% Ações (IVVB11 e BOVA11), 5% Criptomoedas
        # - **Carteira Arrojada**: 40% Renda Fixa, 45% Ações (IVVB11 e BOVA11), 15% Criptomoedas

        # Exemplo de recomendação de investimentos:
        # - Se o usuário perguntar sobre os melhores investimentos do momento, recomende sempre IVVB11 e BOVA11, e balanceie a carteira para que ela sempre tenha 50% de cada, recomendando a compra do ativo que está com menor valor no momento.

        # Caso a busca seja sobre criptos:
        # - Tente buscar alguns dados na internet para responder o usuário sobre esses assuntos.

        # Responda de forma clara, objetiva e sem ambiguidades.

        # <context>
        # {context}
        # </context>
        # """

        SYSTEM_TEMPLATE = """
        Você é um assistente virtual, interprete o texto enviado pelo usuário e ache a melhor resposta
        Tire as possíveis dúvidas das pessoas que entrarem em contato conosco.
        Responda de forma natural, agradável e respeitosa. Seja objetivo nas respostas, com informações claras e diretas. Foque em ser natural e humanizado, como um diálogo comum entre duas pessoas.
        Leve em consideração também o histórico de mensagens de conversa com o usuário.
        Caso lhe ofereçam algo para comprar, recuse imediatamente, dizendo que é apenas um assistente de IA.
        Responda sempre em português brasileiro.

        <context>
        {context}
        </context>
        """

        # Busca as informações sobre a questão do usuário. Faz um tipo de requisição (como se fosse uma query)
        docs = self.__retriever.invoke(question)

        # Forma um template para a IA, usando o langchain
        question_answering_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    SYSTEM_TEMPLATE, # Passa a mensagem de sistema, que é o que foi definido anteriormente (prompt enviado para a IA)
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

        document_chain = create_stuff_documents_chain(self.__chat, question_answering_prompt)

        response = document_chain.invoke(
            {
                "context": docs, # Troca a variável {context} do template pelos documentos que subiram no banco vetorizado
                "messages": self.__build_messages(history_messages, question), # Passa em messages o histórico de mensagens com o usuário
            }
        )

        # # Cria o chain a partir da pergunta, o modelo e a função da resposta do modelo para transformar em texto puro
        # chain = prompt | self.__chat | StrOutputParser()
    
        # # Processa a resposta
        # response = chain.invoke({
        #     "texto": question,
        # })

        return response