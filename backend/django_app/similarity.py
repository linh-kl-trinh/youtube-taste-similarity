from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Calculate the similarity between two playlists
async def calculate_similarity(playlist_words1, playlist_words2):
    # Combine the words into two strings
    playlist_text1 = " ".join(playlist_words1)
    playlist_text2 = " ".join(playlist_words2)

    # Create a TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Fit and transform the vectorizer on the playlist texts
    tfidf_matrix = vectorizer.fit_transform([playlist_text1, playlist_text2])

    # Calculate the cosine similarity between the playlists
    similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # The similarity value is in the top-right corner of the matrix
    playlist_similarity = similarity_matrix[0, 1]
    
    return playlist_similarity

if __name__ == '__main__':
    word_list1 = ['python', 'giraffe', 'ocean', 'umbrella', 'candle', 'keyboard', 'mountain', 'jazz', 'compass', 'telescope']
    word_list2 = ['coffee', 'sunset', 'guitar', 'moonlight', 'fireworks']
    word_list3 = ['coffee', 'sunset', 'guitar', 'moonlight', 'fireworks', 'sea']
    
    phrase_list1 = [
        'The quick brown fox jumps over the lazy dog.',
        'A watched pot never boils.',
        'Life is like a box of chocolates.',
        'Actions speak louder than words.',
        'Don\'t count your chickens before they hatch.',
        'When in Rome, do as the Romans do.',
        'All that glitters is not gold.',
        'An apple a day keeps the doctor away.',
        'Birds of a feather flock together.',
        'Every cloud has a silver lining.',
        'It takes two to tango.',
        'You can\'t have your cake and eat it too.',
        'Where there\'s smoke, there\'s fire.',
        'The early bird catches the worm.',
        'Don\'t put all your eggs in one basket.',
        'Easy come, easy go.',
        'Haste makes waste.',
        'Out of the frying pan and into the fire.',
        'Rome wasn\'t built in a day.',
        'When the going gets tough, the tough get going.'
    ]
    phrase_list2 = [
        'Where there is a will, there is a way.',
        'A picture is worth a thousand words.',
        'Laughter is the best medicine.',
        'Time flies when you\'re having fun.',
        'Beauty is in the eye of the beholder.',
        'Fortune favors the bold.',
        'The pen is mightier than the sword.',
        'Don\'t cry over spilled milk.',
        'Actions speak louder than words.',
        'You can\'t judge a book by its cover.'
    ]

    sentence_list1 = [
        'The sun sets behind the mountains, casting a warm glow over the landscape.',
        'She played a beautiful melody on the piano, capturing the hearts of everyone in the room.',
        'In the vast ocean, a pod of dolphins gracefully swims, leaping out of the water in joyful arcs.',
        'As the rain poured down, people hurriedly opened their umbrellas and scurried for cover.',
        'After a long day of hiking, they gathered around the campfire, sharing stories and roasting marshmallows.'
    ]
    sentence_list2 = [
        'The aroma of freshly brewed coffee filled the air as the sun rose in the distance.',
        'Under the moonlight, they danced to the soothing tunes of a guitar.',
        'As the clock struck midnight, fireworks illuminated the night sky in a dazzling display.',
        'The room echoed with laughter as friends gathered around, sharing stories and jokes.',
        'A sense of tranquility enveloped the scene as the sun dipped below the horizon during the sunset.',
        'In the quiet of the night, a gentle breeze rustled the leaves, creating a peaceful melody.'
    ]

    merged_list1 = word_list1 + phrase_list1 + sentence_list1
    merged_list2 = word_list2 + phrase_list2 + sentence_list2

    random.shuffle(merged_list1)
    random.shuffle(merged_list2)

    similarity_score = calculate_similarity(merged_list1, merged_list2)
    print(f"Similarity Score: {similarity_score}")
