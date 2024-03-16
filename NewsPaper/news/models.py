from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    AuthorRating = models.SmallIntegerField(default = 0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    name = models.CharField(max_lenght = 128, unique = True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    News = 'NW'
    Article = 'AR'
    Category_Choices = [
        (News, 'Новость'),
        (Article, 'Статья')
    ]
    categoryType = models.CharField(max_lenght = 2, choices = Category_Choices, default = Article)
    dataCreate = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, trought='PostCategory')
    title = models.CharField(max_lenght = 128)
    text = models.TextField()
    rating = models.SmallIntegerField(default = 0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default = 0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
