from django.db import models

class Match(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    white = models.ForeignKey('auth.User', related_name='matches', on_delete=models.CASCADE)
    black = models.IntegerField(default=1)
    difficulty = models.IntegerField(default=0)
    board = models.TextField(default='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
    turn = models.CharField(max_length=1, default='w')
    castling = models.CharField(max_length=4, default='KQkq')
    enPassant = models.CharField(max_length=4, default='-')
    halfMove = models.IntegerField(default=0)
    fullMove = models.IntegerField(default=1)
    isOver = models.BooleanField(default=False)
    message = models.TextField(default='')

    class Meta:
        ordering = ('created',)
