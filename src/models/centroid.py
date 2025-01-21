class Centroid:
  def __init__(self, word_frequencies=None):
    """
    Initialize a centroid with given word frequencies.
    :param word_frequencies: A dictionary (set of key value pairs) representing the word frequencies for the centroid.
    """
    self.word_frequencies = word_frequencies or {}

  def update(self, blogs):
    """
    Update the centroid to be the average of the word frequencies of the assigned blogs.
    :param blogs: A list of Blog objects assigned to this centroid.
    """
    if not blogs:
      return

    # Initialize a dictionary to accumulate word frequencies
    new_frequencies = {}

    # Sum up the word frequencies for all blogs
    for blog in blogs:
      for word, freq in blog.word_frequencies.items():
        new_frequencies[word] = new_frequencies.get(word, 0) + freq

    # Calculate the average word frequencies
    self.word_frequencies = {
      word: total_freq / len(blogs) for word, total_freq in new_frequencies.items()
    }
