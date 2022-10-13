public class Game
{
    public GameAccount? Winner;
    public bool Ended = false;
    public int Rating;
    public Guid GameID;
    public GameAccount Player1;
    public GameAccount Player2;

    public Game(GameAccount Player1, GameAccount Player2, int Rating)
    {
        List<GameAccount> Players = new List<GameAccount> {Player1, Player2};
        foreach (GameAccount Player in Players)
        {
            if (Player.GameList.Any())
            {
                if (Player.GameList.Last().Ended)
                {
                    continue;
                }
                throw new ArgumentException($"Player {Player.UserName} is already in game.");
            }
        }
        if (Rating > 0)
        {
            this.Rating = Rating;
        }
        else
        {
            throw new ArgumentException($"Rating must be bigger than 0.");
        }
        this.GameID = Guid.NewGuid();
        this.Player1 = Player1;
        this.Player2 = Player2;
        this.Player1.GameList.Add(this);
        this.Player2.GameList.Add(this);
    }
}
