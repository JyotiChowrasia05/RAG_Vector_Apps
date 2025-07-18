import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

def get_pdf_text(pdf_docs):
  text = ''
  for pdf in pdf_docs:
    pdf_reader = PdfReader(pdf)
    for page in pdf_reader.pages:
      text += page.extract_text()
  return text

def get_text_chunks(raw_text):
  text_splitter = CharacterTextSplitter(
    separator = '\n',
    chunk_size = 1000,
    chunk_overlap = 200,
    length_function = len
  )
  chunks = text_splitter.split_text(raw_text)
  return chunks

def get_vector_store(chunk_text):
  text_embeddings = OpenAIEmbeddings()
  text_vector_store = FAISS.from_texts(texts=chunk_text, embedding=text_embeddings)
  return text_vector_store  

def main():
 load_dotenv()
 st.set_page_config(page_title='Chat with Multiple pdfs', page_icon=':books:')
 st.header('Chat with Multiple pdfs:books:')
 st.text_input('Ask a question about your document')

 with st.sidebar:
  st.subheader('Your documents')
  pdf_docs = st.file_uploader('Upload your pdfs here and click on Process',accept_multiple_files=True)
  if st.button('Process'):
    with st.spinner('Processing'):      
      # get pdf text
      raw_text = get_pdf_text(pdf_docs)
      #st.write(raw_text)
      
      # get pdf chunks
      chunk_text = get_text_chunks(raw_text)
      #st.write(chunk_text)

      # create vector store
      vector_store = get_vector_store(chunk_text)
      st.write(vector_store)

if __name__ == '__main__':
 main()