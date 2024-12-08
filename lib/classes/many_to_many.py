class Article:
    all = []

    def __init__(self, author, magazine, title):
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise ValueError("Title must be a string between 5 and 50 characters.")
        if not isinstance(author, Author):
            raise ValueError("Author must be an instance of Author.")
        if not isinstance(magazine, Magazine):
            raise ValueError("Magazine must be an instance of Magazine.")
        
        self._author = author
        self._magazine = magazine
        self._title = title

        # Add article to all articles list
        Article.all.append(self)
        
        # Add article to the author's article list
        author._articles.append(self)

        # Add article to magazine's list of articles
        magazine.add_article(self)

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, new_author):
        if not isinstance(new_author, Author):
            raise ValueError("New author must be an instance of Author.")
        self._author = new_author  # Allow author to be reassigned

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, new_magazine):
        if not isinstance(new_magazine, Magazine):
            raise ValueError("New magazine must be an instance of Magazine.")
        self._magazine = new_magazine  # Allow magazine to be reassigned


class Author:
    def __init__(self, name):
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("Name must be a non-empty string.")
        self._name = name
        self._articles = []

    @property
    def name(self):
        return self._name

    def articles(self):
        return self._articles

    def magazines(self):
        return list(set(article.magazine for article in self._articles))

    def add_article(self, magazine, title):
        """Creates and returns a new Article given a magazine and title"""
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise ValueError("Title must be a string between 5 and 50 characters.")
        
        # Create a new Article
        article = Article(self, magazine, title)
        
        # Return the newly created article
        return article

    def topic_areas(self):
        """Returns a list of unique topic areas (magazine categories) for all articles by the author."""
        if not self._articles:
          return None
        return list(set(article.magazine.category for article in self._articles))



class Magazine:
    def __init__(self, name, category):
        if not isinstance(name, str) or not (2 <= len(name) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters.")
        if not isinstance(category, str) or len(category) == 0:
            raise ValueError("Category must be a non-empty string.")
        self._name = name
        self._category = category
        self._articles = []
        self._authors = set()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not (2 <= len(value) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters.")
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Category must be a non-empty string.")
        self._category = value

    def articles(self):
        return self._articles

    def contributors(self):
        return list(self._authors)

    def article_titles(self):
        if not self._articles:
            return None
        return [article.title for article in self._articles]

    def contributing_authors(self):
        contributors = [author for author in self._authors if sum(1 for article in author.articles() if article.magazine == self) > 2]
        return contributors if contributors else None

    @classmethod
    def top_publisher(cls):
      if not hasattr(cls, 'all') or not cls.all:
        return None
      top_magazine = None
      max_articles = 0
      for magazine in cls.all:
        article_count = len(magazine.articles())
        if article_count > max_articles:
            top_magazine = magazine
            max_articles = article_count
      return top_magazine


    def add_article(self, article):
        self._articles.append(article)
        self._authors.add(article.author)
        if not hasattr(Magazine, 'all'):
            Magazine.all = []
        if self not in Magazine.all:
            Magazine.all.append(self)
