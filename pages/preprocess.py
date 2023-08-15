from pages.functions_preprocess_data import *
import pandas as pd
import json

def preprocessing_text(df):
    df['cleaned_text'] = df['ExtractedText'].apply(split_sentences)
    df['cleaned_text'] = df['cleaned_text'].apply(replace_newlines_with_spaces)
    df['cleaned_text'] = df['cleaned_text'].apply(remove_pasal_sentences)
    df['cleaned_text'] = df['cleaned_text'].apply(remove_numbering)
    df['cleaned_text'] = df['cleaned_text'].apply(remove_numbering_in_parentheses)
    df['cleaned_text'] = df['cleaned_text'].apply(remove_punctuation)
    df['cleaned_text'] = df['cleaned_text'].apply(remove_danatau)
    df['cleaned_text'] = df['cleaned_text'].apply(delete_link)
    df['cleaned_text'] = df['cleaned_text'].apply(remove_stopwords)
    df['cleaned_text'] = df['cleaned_text'].apply(filter_sentences)
    df['cleaned_text'] = df['cleaned_text'].apply(stem_text)

    def combine_sentences(sentences_list):
        # Combine the list of sentences into one text
        combined_text = ' '.join(sentences_list)

        return combined_text

    df['final_text'] = df['cleaned_text'].apply(combine_sentences)
    return df
