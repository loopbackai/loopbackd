import typer
from rich import print

app = typer.Typer(
    help="LoopbackAI CLI manage and run your loopback daemon",
    epilog="Find more help at https://www.loopback.ai",
)


@app.command()
def up():
    """
    Initalize the CLI and start the daemon if not already running
    """
    from loopbackd.auth import get_token

    print(
        f"""
    You're almost done :boom: Now talk with our [link=https://t.me/LoopbackAIBot]telegram bot t.me/LoopbackAIBot[/link] and paste your token there.
    Your token [bold blue]{get_token()}[/bold blue]
    """
    )


@app.command()
def status():
    """
    Show the daemon status
    """
    import subprocess

    subprocess.run("systemctl status loopbackd".split())


@app.command(rich_help_panel="Debug")
def daemon():
    """
    Run the daemon in foreground for debug purposes
    """
    import loopbackd.daemon as daemon
    import asyncio

    asyncio.run(daemon.handler())


if __name__ == "__main__":
    app()
