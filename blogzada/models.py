from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title
class User(models.Model):
    username = models.CharField(max_length=200, primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    posts = models.ManyToManyField(Post, related_name='users')
    
    def __str__(self):
        return self.username
    
    class Meta:
        ordering = ['username']
        
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"
    
    class Meta:
        ordering = ['-created_at']
        
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Like by {self.user.username} on {self.post.title}"
    
    class Meta:
        ordering = ['-created_at']
        
class Dislike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Dislike by {self.user.username} on {self.post.title}"
    
    class Meta:
        ordering = ['-created_at']
        
class Bookmark(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Bookmark by {self.user.username} on {self.post.title}"
    
    class Meta:
        ordering = ['-created_at']