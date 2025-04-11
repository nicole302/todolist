import flet as ft
from view.home import main  # Importe a função main do arquivo home.py

def main(page: ft.Page):
    page.title = "Cadastro de Tarefa"
    page.bgcolor = ft.Colors.BLACK
    page.scroll = 'adaptive'

    def on_resize(e):
        page.update()  # Atualiza a página ao redimensionar

    page.on_resize = on_resize  # Adiciona o evento de redimensionamento

    # ...restante do código existente...

if __name__ == "__main__":
    ft.app(target=main)  # Executa o aplicativo Flet, passando a função main como alvo

