class AutoCorrect:
    def __init__(self, collection):
        self.collection = collection

    def create_pairs(self, word):
        if len(word) == 1:
            return word
        pairs = [word[i] + word[i+1] for i in range(len(word)-1)]
        return pairs

    def pairs_ratio(self, word1, word2):
        common_pairs = []
        pair1, pair2 = self.create_pairs(word1), self.create_pairs(word2)
        for pair in pair1:
            try:
                pair2.index(pair)
                common_pairs.append(pair)
            except ValueError:
                continue
        try:
            ratio = len(common_pairs)/max(len(pair1),len(pair2))
        except ZeroDivisionError:
            ratio = 0
        return ratio

    def correctWord(self, word, threshold=0.45):
        word = word.lower()
        maxSimilarity = 0.0
        mostSimilarWord = word
        for data in self.collection:
            curSim = self.pairs_ratio(word,data)
            if curSim > maxSimilarity:
                maxSimilarity = curSim
                mostSimilarWord = data
        if maxSimilarity > threshold:
            return mostSimilarWord
        else:
            return word