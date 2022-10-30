from operator import methodcaller
from random import randint, choice
from uuid import uuid4
from os import system, name


class GameAccount:
    
    def __init__(self, username):
        self.user_id = uuid4()
        self.username = username
        self.current_rating = 1
        self.games_count = 0
        self.game_list = []
        self.current_game = None

    def win_game(self):
        game, opponent = self.__win_lose_common()
        game.winner = self
        self.__calculate_rating(self, opponent, game.rating)

    def lose_game(self):
        game, opponent = self.__win_lose_common()
        game.winner = opponent
        self.__calculate_rating(opponent, self, game.rating)

    def get_stats(self):
        stats = f"{'Game ID': ^36}{'Opponent': ^12}{'Result': ^12}{'Rating': ^12}\n"
        for game in self.game_list:
            opponent = game.player2 if game.player1 is self else game.player1
            result = 'win' if game.winner is self else 'lose'
            rating = game.rating if result == 'win' else -game.rating
            stats += f'{str(game.game_id): ^36}{opponent.username: ^12}{result: ^12}{rating: ^12}\n'
        return stats

    def __win_lose_common(self):
        if not self.current_game:
            raise Game.GameError(f'{self.username} is not playing any game.')
        game = self.current_game
        opponent = game.player2 if game.player1 is self else game.player1
        for player in (game.player1, game.player2):
            player.games_count += 1
            player.current_game = None
        return game, opponent

    @staticmethod
    def __calculate_rating(winner, loser, rating):
        winner.current_rating += rating
        loser.current_rating -= rating
        if loser.current_rating < 1:
            loser.current_rating = 1

class Game:

    winner = None

    def __init__(self, player1, player2, rating):
        if self.__validate_players(player1, player2) and self.__validate_rating(rating):
            self.rating = rating
            self.game_id = uuid4()
            self.player1 = player1
            self.player2 = player2
            for player in (player1, player2):
                player.current_game = self
                player.game_list.append(self)

    @staticmethod
    def __validate_players(*players):
        for player in players:
            if player.current_game:
                raise Game.GameError(f'Player {player.username} is already in game.')
        return True

    @staticmethod
    def __validate_rating(rating):
        if rating < 0:
            raise ValueError('Rating must be bigger than 0.')
        return True

    class GameError(Exception):
        ...


def clear_terminal():
    system('cls' if name == 'nt' else 'clear')


def get_amount_of_games():
    while True:
        try:
            i = int(input('Enter an amount of games to randomize everything: '))
            if i <= 0:
                raise ValueError()
        except ValueError:
            print(end='Invalid number. ')
        else:
            return i
        finally:
            clear_terminal()


def play_random_games(accounts, games_amount):
    for _ in range(games_amount):
        Game(*choice((accounts, reversed(accounts))), randint(1, 100))    # type: ignore
        methodcaller(choice(('win_game', 'lose_game')))(choice(accounts))


def print_account_stats(account):
        header = f"{account.username}'s stats"
        print(f'{header: ^72}\n\n'
                f'{account.get_stats()}\n\n'
                f'Other account information:\n\n'
                f'\tAccount ID: {account.user_id}\n'
                f'\tCurrent rating: {account.current_rating}\n'
                f'\tGames count: {account.games_count}\n\n')
        input('Press Enter to continue')
        clear_terminal()


def main():
    game_accounts = GameAccount('Python'), GameAccount('Csharp')
    games_amount = get_amount_of_games()
    play_random_games(game_accounts, games_amount)
    for account in game_accounts:
        print_account_stats(account)


if __name__ == '__main__':
    main()

