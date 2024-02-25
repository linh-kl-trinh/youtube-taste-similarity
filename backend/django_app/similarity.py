from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(playlist1_words, playlist2_words):
    """
    Calculate the cosine similarity between two playlists based on their word lists.

    Parameters:
    - playlist1_words: Dictionary containing word lists for playlist 1
    - playlist2_words: Dictionary containing word lists for playlist 2

    Returns:
    - similarity_score: Cosine similarity score between the two playlists
    """
    # Vectorize the playlists
    vectorizer = CountVectorizer()

    # Concatenate words from each category
    playlist1_text = playlist1_words["category_info"] * 3 + playlist1_words["channel_info"] * 2 + playlist1_words["video_info"]
    playlist2_text = playlist2_words["category_info"] * 3 + playlist2_words["channel_info"] * 2 + playlist2_words["video_info"]

    print(playlist1_words["category_info"])
    print(playlist2_words["category_info"])
    # Fit and transform the playlists
    X = vectorizer.fit_transform([playlist1_text, playlist2_text])

    # Calculate the cosine similarity
    similarity_matrix = cosine_similarity(X)

    # The cosine similarity matrix is a 2x2 matrix, and we are interested in the top-right element
    similarity_score = similarity_matrix[0][1]

    return similarity_score