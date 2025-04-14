import flet as ft
from view.tarefa_view import on_add_tarefa_click, atualizar_lista_tarefas

def main(page: ft.Page):
    page.title = "Cadastro de Tarefa"
    page.bgcolor = ft.Colors.BLACK
    page.scroll = 'adaptive'

    # Registra as fontes personalizadas usando caminhos relativos corrigidos
    page.fonts = {
        "Nicole": "src/assets/fonts/sf_distant_galaxy/SF Distant Galaxy Outline Italic.ttf",
        "Nicole2": "src/assets/fonts/sf_distant_galaxy/SF Distant Galaxy Italic.ttf",
    }


    titulo = ft.Text(
        "To do List",
        font_family="Nicole2",
        text_align="center",
        size=50,
        color=ft.Colors.AMBER_500
    )

    descricao_input = ft.TextField(
        label="Descrição da Tarefa",
        label_style=ft.TextStyle(color=ft.Colors.AMBER_500),
        autofocus=True,
        expand=True,  # Expande para ocupar o espaço disponível
        bgcolor=ft.Colors.BLACK,
        color=ft.Colors.AMBER_500,
        border_color=ft.Colors.DEEP_ORANGE_900,
        text_style=ft.TextStyle(color=ft.Colors.AMBER_500),
        max_length=30
    )

    situacao_input = ft.Checkbox(
        label="Tarefa concluída",
        value=False,
        fill_color=ft.Colors.GREEN_100,
        label_style=ft.TextStyle(color=ft.Colors.AMBER_500)
    )

    add_button = ft.ElevatedButton(
        "Cadastrar Tarefa",
        on_click=lambda e: [
            on_add_tarefa_click(
                e,
                descricao_input,
                situacao_input,
                result_text,
                tarefas_column
            ),
            setattr(descricao_input, "value", ""),
            descricao_input.update()
        ],
        color=ft.Colors.DEEP_ORANGE_900,
        bgcolor=ft.Colors.DEEP_ORANGE_100,
        opacity=0.8
    )

    tarefas_column = ft.Column(
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        expand=True,  # Expande para ocupar o espaço vertical disponível
        scroll=ft.ScrollMode.AUTO
    )

    result_text = ft.Text(
        color=ft.Colors.AMBER_500,
        font_family="Nicole2",
        expand=True  # Expande para ocupar o espaço horizontal disponível
    )

    refresh_page_button = ft.ElevatedButton(
        "Atualizar Página",
        on_click=lambda e: atualizar_lista_tarefas(tarefas_column, result_text),
        color=ft.Colors.DEEP_ORANGE_900,
        bgcolor=ft.Colors.DEEP_ORANGE_100,
        opacity=0.8
    )

    # Imagem de fundo via ft.Image
    fundo = ft.Container(
        content=ft.Image(
            src="https://i.postimg.cc/FHtV5J9S/system.jpg",
            fit=ft.ImageFit.COVER,  # Ajusta a imagem para cobrir toda a área
            width=page.width,       # Define a largura como a largura da página
            height=page.height,     # Define a altura como a altura da página
        ),
        expand=True
    )

    conteudo = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [titulo],
                    alignment=ft.MainAxisAlignment.CENTER  # Alinha o título ao centro
                ),
                descricao_input,
                ft.Row(
                    [situacao_input, add_button],  # Checkbox e botão alinhados à esquerda
                    alignment=ft.MainAxisAlignment.START
                ),
                tarefas_column,
                ft.Row(
                    [refresh_page_button],
                    alignment=ft.MainAxisAlignment.CENTER  # Alinha o botão "Atualizar Página" ao centro
                ),
                result_text
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            expand=True  # Expande para ocupar o espaço vertical disponível
        ),
        margin=ft.Margin(20, 20, 20, 20)
    )

    page.add(
        ft.Stack(
            controls=[fundo, conteudo]
        )
    )

    def on_resize(e):
        # Atualiza o tamanho da imagem ao redimensionar a página
        fundo.content.width = page.width
        fundo.content.height = page.height
        page.update()

    page.on_resize = on_resize
    atualizar_lista_tarefas(tarefas_column, result_text)

