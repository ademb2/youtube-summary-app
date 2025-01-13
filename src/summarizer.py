from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

# Initialize the language model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Custom prompts
custom_stuff_prompt = PromptTemplate(
    input_variables=["text"],
    template=(
        "Summarize the main ideas from the following text using clear markdown formatting.  "
        "Include arguments that support the ideas and only relevant examples to illustrate key points and avoid filler or redundant phrases:\n\n"
        "{text}\n\n"
        "**Summary:**"
    )
)

custom_map_prompt = PromptTemplate(
    input_variables=["text"],
    template=(
        "Summarize the main ideas from the following text using clear markdown formatting.  "
        "Include arguments that support the ideas and only relevant examples to illustrate key points and avoid filler or redundant phrases:\n\n"
        "{text}\n\n"
        "**Summary:**"
    )
)

custom_combine_prompt = PromptTemplate(
    input_variables=["text"],
    template=(
        "Combine the following summaries of different parts of the same document ensure all informations are retained and ensure proper markdown formatting. "
        "Include all examples cited to illustrate each idea and ensure theres no redundancy:\n\n"
        "{text}\n\n"
        "**Summary:**"
    )
)

custom_refine_initial_prompt = PromptTemplate(
    input_variables=["text"],
    template=(
        "Summarize the main ideas from the following text using clear markdown formatting.  "
        "Include arguments that support the ideas and only relevant examples to illustrate key points and avoid filler or redundant phrases:\n\n"
        "{text}\n\n"
        "**Summary:**"
    )
)

custom_refine_refinement_prompt = PromptTemplate(
    input_variables=["existing_answer", "text"],
    template=(
        "Given the existing summary: \n\n"
        "{existing_answer}\n\n"
        "Refine it by incorporating the main ideas from the following text. "
        "Ensure proper markdown formatting and Include arguments that support the ideas and only relevant examples to illustrate key points and avoid filler or redundant phrases:\n\n"
        "{text}\n\n"
        "**Refined Summary:**"
    )
)

def generate_summary(transcript_text, method='map_reduce', detail_level=3, verbose=False, token_max=500000):
    """Generate a summary using LangChain."""
    token_count = llm.get_num_tokens(custom_stuff_prompt.format(text=transcript_text))
    
    chunk_size_map = {1: 4, 2: 8, 3: 14}
    if detail_level == 3:
        chunk_size = token_count // 14
    else:
        chunk_size = token_count // chunk_size_map.get(detail_level, 14)
    chunk_overlap = chunk_size // 10

    if token_count < 1000 or method == 'stuff':
        docs = [Document(page_content=transcript_text)]
        chain = load_summarize_chain(llm, 
                                     chain_type="stuff",
                                     verbose=verbose,
                                     prompt=custom_stuff_prompt)
        summary = chain.invoke(docs)
    else:
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        texts = text_splitter.split_text(transcript_text)
        docs = [Document(page_content=t) for t in texts]

        if method not in ['map_reduce', 'iterative_refinement']:
            method = 'map_reduce'

        if method == 'map_reduce':
            chain = load_summarize_chain(llm, 
                                         chain_type="map_reduce",
                                         verbose=verbose,
                                         map_prompt=custom_map_prompt,
                                         combine_prompt=custom_combine_prompt,
                                         token_max=token_max)
            summary = chain.invoke(docs)
        elif method == 'iterative_refinement':
            chain = load_summarize_chain(llm, 
                                         chain_type="refine",
                                         verbose=verbose,
                                         question_prompt=custom_refine_initial_prompt,
                                         refine_prompt=custom_refine_refinement_prompt)
            summary = chain.invoke(docs)
    
    return summary