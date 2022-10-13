GameAccount Account1 = new GameAccount("Python");
GameAccount Account2 = new GameAccount("Csharp");
List<GameAccount> Accounts = new List<GameAccount>() { Account1, Account2 };
int i;

while (true)
{
    try
    {
        Console.Write("Enter an amount of games to randomize everything: ");
        string? Answer = Console.ReadLine();
        if (Answer != null)
        {
            i = Int32.Parse(Answer);
            Console.WriteLine();
            break;
        }
        else
        {
            throw new FormatException();
        }
    }
    catch (FormatException)
    {
        Console.WriteLine("Invalid number.");
    }
}
for (int j = 0; j < i; j++)
{
    Random Rnd = new Random();
    int a = Rnd.Next(1, 101);
    int b = Rnd.Next(1, 3);
    Game CurrentGame;
    if (b == 1)
    {
        CurrentGame = new Game(Account1, Account2, a);
    }
    else
    {
        CurrentGame = new Game(Account2, Account1, a);
    }
    if (a < 50)
    {
        if (a < 25)
        {
            Account1.WinGame();
        }
        else
        {
            Account1.LoseGame();
        }
    }
    else
    {
        if (a < 75)
        {
            Account2.WinGame();
        }
        else
        {
            Account2.LoseGame();
        }
    }
}
foreach (GameAccount Account in Accounts)
{
    string str = $"{Account.UserName}'s stats";
    Console.WriteLine($"{str,43}\n");
    Account.GetStats();
    Console.WriteLine($@"
Other account information:

        Account ID: {Account.UserID}
        Current rating: {Account.CurrentRating}
        Games count: {Account.GamesCount}
");
}
