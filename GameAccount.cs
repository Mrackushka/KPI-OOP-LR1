public class GameAccount
{
    public Guid UserID;
    public string UserName;
    public int CurrentRating = 1;
    public int GamesCount = 0;
    public List<Game> GameList;

    public GameAccount(string UserName)
    {
        this.UserID = Guid.NewGuid();
        this.UserName = UserName;
        this.GameList = new List<Game>();
    }

    public void WinGame()
    {
        var CurrentGame = this.WinLoseCommon();
        CurrentGame.Winner = this;
        this.CurrentRating += CurrentGame.Rating;
    }

    public void LoseGame()
    {
        Game CurrentGame = this.WinLoseCommon();
        if (CurrentGame.Player2 == this)
        {
            CurrentGame.Winner = CurrentGame.Player1;
        }
        else
        {
            CurrentGame.Winner = CurrentGame.Player2;
        }
        this.CurrentRating -= CurrentGame.Rating;
        if (this.CurrentRating < 1)
        {
            this.CurrentRating = 1;
        }
    }

    public void GetStats()
    {
        string GameIDstr = "Game ID";
        string Opponentstr = "Opponent";
        string Resultstr = "Result";
        string Ratingstr = "Rating";
        Console.WriteLine($"{GameIDstr,21}{Opponentstr,25}{Resultstr,11}{Ratingstr,12}");
        foreach (Game CurrentGame in this.GameList)
        {
            GameAccount Opponent;
            if (CurrentGame.Player1 == this)
            {
                Opponent = CurrentGame.Player2;
            }
            else
            {
                Opponent = CurrentGame.Player1;
            }
            string Result;
            if (CurrentGame.Winner == this)
            {
                Result = "win";
            }
            else
            {
                Result = "lose";
            }
            int Rating;
            if (Result == "win")
            {
                Rating = CurrentGame.Rating;
            }
            else
            {
                Rating = -CurrentGame.Rating;
            }
            Console.WriteLine($"{CurrentGame.GameID}{Opponent.UserName,9}{Result,11}{Rating,11}");
        }
    }

    Game WinLoseCommon()
    {
        Game CurrentGame = this.GameList.Last();
        if (CurrentGame.Ended)
        {
            throw new ArgumentException($"{this.UserName} is not playing any game.");
        }
        CurrentGame.Player1.GamesCount += 1;
        CurrentGame.Player2.GamesCount += 1;
        CurrentGame.Ended = true;
        return CurrentGame;
    }
}
