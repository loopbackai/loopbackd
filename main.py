from asyncio import subprocess
import typer
from rich import print

app = typer.Typer(help="LoopbackAI CLI manage and run your loopback daemon")


@app.command(help="Initalize the CLI and start the daemon if not already running")
def up():
    from loopbackd.auth import get_token

    print(
        f"""
    You're almost done :boom: Now talk with our telegram bot and paste your token there.
    Your token [bold blue]{get_token()}[/bold blue]
    """
    )


@app.command(help="Show the daemon status")
def status():
    import subprocess

    subprocess.run("systemctl status loopbackd".split())


@app.command(help="Run the daemon in foreground for debug purposes")
def daemon():
    import loopbackd.daemon as daemon
    import asyncio

    asyncio.run(daemon.handler())


if __name__ == "__main__":
    app()
