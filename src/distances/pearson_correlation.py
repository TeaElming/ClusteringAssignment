from math import sqrt

class PearsonCorrelation:
  def pearson_correlation(self, blogA, blogB) -> float:
    word_categories = list(blogA.word_frequencies.keys()) # Getting the words from Blog A since tke keys are the same for all blogs
    numberOfWords = len(word_categories) # So that we know how many to go through

    if (numberOfWords == 0):
      raise ValueError("Number of words (categories) must be greater than zero.")

    sumA = sum(blogA.get_word_frequency(word) for word in word_categories)
    sumB = sum(blogB.get_word_frequency(word) for word in word_categories)

    sumAsqr = sum(blogA.get_word_frequency(word) ** 2 for word in word_categories)
    sumBsqr = sum(blogB.get_word_frequency(word) ** 2 for word in word_categories)

    pSum = sum(blogA.get_word_frequency(word) * blogB.get_word_frequency(word) for word in word_categories)

    num = pSum - ((sumA * sumB) / numberOfWords)
    den = sqrt((sumAsqr - (sumA ** 2) / numberOfWords) * (sumBsqr - (sumB ** 2) / numberOfWords))

    if den == 0:
      return 0  # Avoid null div

    return 1.0 - (num/den)