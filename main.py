# -*- coding: utf-8 -*-

import openai
import config
import typer
from datetime import datetime
from rich import print
from rich.table import Table


def main():

    openai.api_key = config.api_key

    print("💬 [bold green]Bienvenido a la API de ChatGPT en Python[/bold green] 💬")

    help()

    messages = [context()]

    while True:

        content = __prompt()

        if content == "new":
            print("[bold cyan]Nueva conversación[/bold cyan]\n")
            messages = [context()]
            content = __prompt()

        elif content == "help":
            help()

        elif content == "context":
            messages = [context()]

        messages.append({"role": "user", "content": content})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages)

        response_content = response.choices[0].message.content

        messages.append({"role": "assistant", "content": response_content})

        print(f"🕒[yellow]{datetime.now().time().strftime('%H:%M:%S')}...[/yellow] {response_content}")


def help():
    table = Table("Comando", "Descripción")
    table.add_row("new", "Nueva conversación")
    table.add_row("context", "Dar un contexto a Chat GPT")
    table.add_row("help", "Tabla de comandos")
    table.add_row("exit", "Finalizar chat")

    print(table)


def context():
    context = {"role": "system",
               "content": typer.prompt("Cómo quieres que me comporte")}
    return context


def __prompt() -> str:
    prompt = typer.prompt("\n¿En qué puedo ayudarte? ")

    if prompt == "exit":
        exit = typer.confirm("⚠️ ¿Seguro que deseas salir del chat?")
        if exit:
            print("¡Hasta luego!🖐️")
            raise typer.Abort()
        return __prompt()

    return prompt


if __name__ == "__main__":
    typer.run(main)