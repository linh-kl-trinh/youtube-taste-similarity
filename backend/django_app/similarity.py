import spacy
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(words1, words2):
    nlp = spacy.load("en_core_web_md")

    doc1 = nlp(" ".join(words1))
    doc2 = nlp(" ".join(words2))

    vec1 = doc1.vector.reshape(1, -1)
    vec2 = doc2.vector.reshape(1, -1)

    similarity_score = cosine_similarity(vec1, vec2)[0][0]

    return similarity_score

if __name__ == '__main__':
    playlist1_words = ['ocean', 'xylophone', 'cucumber', 'jazz', 'kangaroo', 'guitar', 'quasar', 'paradox', 'umbrella', 'whisper', 'hologram', 'penguin', 'tornado', 'illusion', 'bubble']
    playlist2_words = ['mermaid', 'saxophone', 'quantum', 'marvel', 'butterfly', 'jungle', 'robotics', 'velvet', 'disco', 'albatross', 'whistle', 'puzzle', 'fireworks', 'zenith', 'carousel', 'nectar']

    similarity_score = calculate_similarity(playlist1_words, playlist2_words)
    print(f"Similarity Score: {similarity_score}")
