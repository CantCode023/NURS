from rich import print

class Logger:
    def log(self, message):
        print(f"[bold][-] {message}[/bold]")

    def error(self, message):
        print(f"[bold][red][!] {message}[/red][/bold]")

    def success(self, message):
        print(f"[bold][green][+] {message}[/green][/bold]")

    def warn(self, message):
        print(f"[bold][dark_orange][!] {message}[/dark_orange][/bold]")

    def info(self, message):
        print(f"[italic][bright_black][-] {message}[/bright_black][/italic]")