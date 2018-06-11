from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from io import StringIO
import chess
import chess.uci
import chess.pgn

class Player(models.Model):
    user = models.OneToOneField(User, related_name='player', on_delete=models.CASCADE)
    current = models.ForeignKey('Match', on_delete=models.SET_NULL, null=True)
    wins = models.IntegerField(default=0)

    def move(self, uci):
        if self.current.board.turn == True:
            move = chess.Move.from_uci(uci)
            return self.current.update_pgn(move)
        else:
            return False

    def forfeit(self):
        if self == self.current.white:
            self.current.winner = 'Black'
        # Expand this when Black is its own User
        self.current.save()

class Match(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    white = models.ForeignKey(Player, related_name='match', on_delete=models.CASCADE)
    black = models.IntegerField(default=1)
    pgn = models.TextField(default='[Event "?"]\n[Site "?"]\n[Date "????.??.??"]\n[Round "?"]\n[White "?"]\n[Black "?"]\n[Result "*"]\n\n*')
    difficulty = models.IntegerField(default=0)
    winner = models.CharField(default='', max_length=5)
    detail = models.TextField(default='')

    @property
    def board(self):
        game = chess.pgn.read_game(StringIO(self.pgn))
        board = game.board()
        for move in game.main_line():
            board.push(move)
        return board

    def auto_move(self):
        # Improve this
        engine = chess.uci.popen_engine("/usr/games/stockfish")
        engine.uci()
        engine.position(self.board)
        move = engine.go(movetime=2000).bestmove
        engine.terminate()
        return move

    def bot_move(self):
        if self.board.turn == False:
            return self.update_pgn(self.auto_move())
        else:
            return False

    def check_for_win(self):
        if self.board.is_game_over():
            result = self.board.result
            if result == '1-0':
                self.winner = 'White'
            if result == '0-1':
                self.winner = 'Black'
            if result == '1/2-1/2' or self.board.is_fivefold_repetition():
                self.winner = 'Draw'
            self.save(update_fields=["winner"])

    def update_pgn(self, move):
        if move in self.board.legal_moves:
            game = chess.pgn.Game()
            for m in self.board.move_stack:
                game = game.add_variation(m)
            game.add_variation(move)
            self.pgn = str(game.root())
            self.save(update_fields=["pgn"])

            self.check_for_win()

            return True
        else:
            return False

    class Meta:
        ordering = ('created',)

@receiver(post_save, sender=Match)
def save_match(sender, instance, **kwargs):
    player = instance.white
    if instance.winner == "":
        player.current = instance
    else:
        player.current = None
    player.save()

@receiver(post_save, sender=User)
def create_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_player(sender, instance, **kwargs):
    instance.player.save()
