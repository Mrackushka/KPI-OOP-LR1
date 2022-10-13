from operator import methodcaller
from random import randint, choice
from uuid import uuid4


class GameAccount:
    
    def __init__(self, username):
        self.user_id = uuid4()
        self.username = username
        self.current_rating = 1
        self.games_count = 0
        self.game_list = []

    def win_game(self):
        game = self.__win_lose_common()
        game.winner = self
        self.current_rating += game.rating

    def lose_game(self):
        game = self.__win_lose_common()
        game.winner = game.player1 if game.player2 is self else game.player2
        self.current_rating -= game.rating
        if self.current_rating < 1:
            self.current_rating = 1

    def get_stats(self):
        print(f"{'Game ID': ^36}{'Opponent': ^12}{'Result': ^12}{'Rating': ^12}")
        for game in self.game_list:
            opponent = game.player2 if game.player1 is self else game.player1
            result = 'win' if game.winner is self else 'lose'
            rating = game.rating if result == 'win' else -game.rating
            print(f'{str(game.game_id): ^36}{opponent.username: ^12}{result: ^12}{rating: ^12}')

    def __win_lose_common(self):
        game = self.game_list[-1]
        if game.ended:
            raise Game.GameError(f'{self.username} is not playing any game.')
        for player in (game.player1, game.player2):
            player.games_count += 1
        game.ended = True
        return game


class Game:

    winner = None
    ended = False

    def __init__(self, player1, player2, rating):
        for player in (player1, player2):
            if player.game_list:
                if player.game_list[-1].ended:
                    continue
                raise Game.GameError(f'Player {player.username} is already in game.')

        if rating > 0:
            self.rating = rating
        else:
            raise ValueError('Rating must be bigger than 0.')

        self.game_id = uuid4()
        self.player1 = player1
        self.player2 = player2
        self.player1.game_list.append(self)
        self.player2.game_list.append(self)

    class GameError(Exception):
        ...


def main():
    account1 = GameAccount('Python')
    account2 = GameAccount('Csharp')
    accounts = account1, account2

    while True:
        try:
            i = int(input('Enter an amount of games to randomize everything: '))
            print()
            break
        except ValueError:
            print('Invalid number.')

    for _ in range(i):
        Game(*choice((accounts, reversed(accounts))), randint(1, 100))    # type: ignore
        methodcaller(choice(('win_game', 'lose_game')))(choice(accounts))

    for account in accounts:
        temp = f"{account.username}'s stats"
        print(f'{temp: ^72}\n')
        account.get_stats()
        print(f'\nOther account information:\n\n'
                f'\tAccount ID: {account.user_id}\n'
                f'\tCurrent rating: {account.current_rating}\n'
                f'\tGames count: {account.games_count}\n')


if __name__ == '__main__':
    main()

