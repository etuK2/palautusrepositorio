from player_reader import PlayerReader
from player_stats import PlayerStats
from rich.console import Console
from rich.table import Table

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats"
    reader = PlayerReader(url)

    available_seasons = [
        "2018-19", "2019-20", "2020-21", 
        "2021-22", "2022-23", "2023-24", 
        "2024-25"
    ]
    console = Console()
    
    print("NHL statistics by nationality\n")

    season = input(f"Select season [2018-19/2019-20/2020-21/2021-22/2022-23/2023-24/2024-25/]: ")

    reader.get_players(season)
    stats = PlayerStats(reader)

    while True:
        nationality = input("\nSelect nationality [AUT/CZE/AUS/SWE/GER/DEN/SUI/SVK/NOR/RUS/CAN/LAT/BLR/SLO/USA/FIN/GBR/]: ").strip()

        players = stats.top_scorers_by_nationality(nationality)

        table = Table(title=f"Top scorers of {nationality} season {season}")

        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Team", style="purple")
        table.add_column("Goals", style="green")
        table.add_column("Assists", style="green")
        table.add_column("Points", style="green")

        if players:
            for player in players:
                table.add_row(player.name, player.team, str(player.goals), str(player.assists), str(player.points))
            console.print(table)
        else:
            break

if __name__ == "__main__":
    main()
