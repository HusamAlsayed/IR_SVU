from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import numpy as np
from numpy.linalg import norm
from logic.models import QuestionRecord


terms_idf = {}


def calculate_idf_for_words(words, vectors):
    for word in words:
        terms_idf[word] = calculate_idf(word, vectors)


def calculate_idf(query_word, vectors):
    ans = 0
    for vector in vectors:
        new_vector = vector.split()
        if query_word in new_vector:
            ans += 1
    # print(f'the ans is {ans}')
    return len(vectors)/np.log2(ans + 1.1)


class Retrieve:
    def __init__(self):
        self.term_idf = {}
        self.records = list(QuestionRecord.objects.all().values())
        self.questions = [record['question'] for record in self.records ]
        self.answers = [record['answer'] for record in self.records ]
        self.all_words = list(set(" ".join([x for x in self.answers]).split()))
        calculate_idf_for_words(self.all_words, self.answers)
        self.count_vectorizer = CountVectorizer(binary=True)
        self.vectorizer = self.count_vectorizer.fit_transform(self.answers)

        self.tfidf_vectorizer = TfidfVectorizer()
        self.tf_vectorizer = self.tfidf_vectorizer.fit_transform(self.answers)

    def get_binary_closest_answer(self, query):
        query = query.strip().lower()
        transformed_query = self.count_vectorizer.transform([query])[0]
        transformed_query_array = transformed_query.toarray()
        best_value, best_index = -1, -1
        for index, vector in enumerate(self.vectorizer):
            value = (vector.toarray() & transformed_query_array).sum()
            if value > best_value:
                best_index = index
                best_value = value
        # print(f'the value is {self.records[best_index]}')
        return self.records[best_index]
        # return best_index, best_value

    def get_vectorized_closest_answer(self, query):
        transformed_query = self.tfidf_vectorizer.transform([query])[0]
        transformed_query_array = transformed_query.toarray()
        best_index, best_value = -100, -100
        for index, vector in enumerate(self.tf_vectorizer):
            vector_array = vector.toarray()[0]
            cosine = np.dot(transformed_query_array, vector_array)/(norm(transformed_query_array)*norm(vector_array))
            # print(f'the cosine is {cosine}')
            if cosine[0] > best_value:
                best_value = cosine[0]
                best_index = index
        # print(f'the value is {self.records[best_index]}')
        return self.records[best_index]
        # return best_index, best_value

    def get_extended_boolean_closest_answer(self, query):
        transformed_query = self.tfidf_vectorizer.transform([query])[0]
        transformed_query_array = transformed_query.toarray()
        max_idf = max(terms_idf.get(word, 0) for word in query.strip().split())
        best_index, best_value = -100, -100
        for index, vector in enumerate(self.tf_vectorizer):
            vector_array = vector.toarray()[0]
            cosine = np.dot(transformed_query_array, vector_array) / (
                        norm(transformed_query_array) * norm(vector_array)) / max_idf
            # print(f'the cosine is {cosine}')
            if cosine[0] > best_value:
                best_value = cosine[0]
                best_index = index

        print(f'the value is {self.records[best_index]}')
        return self.records[best_index]
        # return best_index, best_value


