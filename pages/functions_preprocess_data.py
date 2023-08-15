import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

nltk.data.path.append("asset/nltk_data/tokenizers")
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

def split_sentences(text):
  # Split the text into sentences based on '\n\n' pattern
  sentences = re.split(r'\n\n', text)

  # Clean up the sentences by removing leading/trailing whitespaces
  sentences = [sentence.lower().strip() for sentence in sentences]

  return sentences

def remove_punctuation(sentences):
  translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
  cleaned_sentences = []
  for sentence in sentences:
    cleaned_sentence = sentence.translate(translator)
    cleaned_sentences.append(cleaned_sentence)
  return cleaned_sentences

def remove_stopwords(sentences_list):
  # Download Indonesian stopwords list from NLTK
  stop_words = set(stopwords.words('indonesian'))

  # Tokenize each sentence and remove stopwords
  cleaned_sentences = []
  for sentence in sentences_list:
    words = word_tokenize(sentence)
    filtered_sentence = [word for word in words if word.lower() not in stop_words]
    cleaned_sentences.append(' '.join(filtered_sentence))

  return cleaned_sentences

def remove_pasal_sentences(text_list):
  # Define the regular expression pattern to match 'pasal' followed by a space and digits
  pattern = r'pasal\s\d+'
  # Filter out sentences that match the regular expression
  filtered_list = [sentence for sentence in text_list if not re.search(pattern, sentence)]
  return filtered_list

def remove_empty_text(sentences_list):
  non_empty_sentences = [[sentence for sentence in sentences if sentence.strip() != ""] for sentences in sentences_list]
  non_empty_sentences = [sentences for sentences in non_empty_sentences if sentences]  # Remove empty lists
  return non_empty_sentences

def remove_numbering(sentences_list):
  # Define the regular expression pattern to match numbering patterns
  pattern = r'\b[A-Za-z1-9]\.'
  # Remove the numbering pattern from each sentence in the list
  filtered_list = [re.sub(pattern, '', sentence) for sentence in sentences_list]
  return filtered_list

def remove_numbering_in_parentheses(sentences_list):
  # Define the regular expression pattern to match the numbering in parentheses at the start of the sentence
  pattern = r'\(\d+\)'

  # Remove the numbering pattern from each sentence in the list
  filtered_list = [re.sub(pattern, '', sentence) for sentence in sentences_list]

  return filtered_list

def remove_danatau(sentences):
  # Remove 'danatau' from the text
  cleaned_sentences = [sentence.replace('danatau', '') for sentence in sentences]
  return cleaned_sentences

def replace_newlines_with_spaces(sentences_list):
  # Replace '\n' with a space in each sentence
  cleaned_list = [sentence.replace('\n', ' ') for sentence in sentences_list]
  return cleaned_list

def delete_link(sentence_list):
  filtered_sentences = [sentence for sentence in sentence_list if 'www' not in sentence and 'bphn' not in sentence]
  return filtered_sentences

def filter_sentences(sentences_list):
  # Remove sentences that only have 1 word or include 'bab' or 'presiden'
  filtered_sentences = [sentence for sentence in sentences_list if len(sentence.split()) > 2 and 'bab' not in sentence and 'presiden' not in sentence]
  return filtered_sentences

def stem_text(sentences_list):
  # Create a StemmerFactory and get the default Indonesian stemmer
  stemmer = StemmerFactory().create_stemmer()
  # Stem each sentence in the list
  stemmed_sentences = [stemmer.stem(sentence) for sentence in sentences_list]
  return stemmed_sentences

def tfidf(text, max_feat = 1000):
  # Create the TfidfVectorizer with bigram and trigram
  vectorizer = TfidfVectorizer(analyzer = 'word', ngram_range = (2,3), max_features = max_feat)
  tfidf_matrix = vectorizer.fit_transform(text)
  feature_names = vectorizer.get_feature_names_out()
  return tfidf_matrix, feature_names