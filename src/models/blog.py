class Blog:
  def __init__(self, blog_name: str, word_frequencies: dict):
    """
    Initialise a Blog instance.
    :param blog_name: Name of the blog
    :param word_frequencies: A dictionary where keys are word categories and values are their counts
    """
    self.blog_name = blog_name
    self.word_frequencies = word_frequencies

  def get_word_frequency(self, word: str) -> int:
    """
    Get the frequency of a specific word in the blog.
    :param word: The word/category to look for
    :return: Frequency of the word
    """
    return self.word_frequencies.get(word, 0)