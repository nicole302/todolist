import flet as ft
from view.tarefa_view import on_add_tarefa_click, atualizar_lista_tarefas

def main(page: ft.Page):
    page.title = "Cadastro de Tarefa"
    page.bgcolor = ft.Colors.BLACK
    page.scroll = 'adaptive'  # Só quando for necessário a rolagem

    page.fonts = {
        "Nicole": "src/assets/fonts/sf_distant_galaxy/SF Distant Galaxy Outline Italic.ttf",
        "Nicole2": "src/assets/fonts/sf_distant_galaxy/SF Distant Galaxy Italic.ttf"
    }

    titulo = ft.Text(
        "To do List",
        font_family='Nicole2',
        text_align='center',
        size=50,
        color=ft.Colors.DEEP_ORANGE_900
    )

    descricao_input = ft.TextField(
        label="Descrição da Tarefa",
        autofocus=True,
        expand=True,  # Expande para ocupar o espaço disponível
        color=ft.Colors.DEEP_ORANGE_900,  # Cor do texto dentro do campo
        border_color=ft.Colors.DEEP_ORANGE_900,  # Define a cor da borda
        text_style=ft.TextStyle(color=ft.Colors.WHITE)  # Muda a cor do texto para branco
    )

    tarefas_column = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,  # Centraliza verticalmente
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centraliza horizontalmente
        expand=True  # Expande para ocupar o espaço disponível
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
            setattr(descricao_input, "value", ""),  # Limpa o campo após cadastrar
            descricao_input.update()  # Atualiza o componente
        ],
        color=ft.Colors.DEEP_ORANGE_900,
        bgcolor=ft.Colors.DEEP_ORANGE_100,
        opacity=0.8
    )

    result_text = ft.Text(
        color=ft.Colors.DEEP_ORANGE_900,
        font_family="Nicole2"
    )

    situacao_input = ft.Checkbox(
        label="Tarefa concluída",
        value=False,
        fill_color=ft.Colors.GREEN_100
    )

    refresh_page_button = ft.ElevatedButton(
        "Atualizar Página",
        on_click=lambda e: atualizar_lista_tarefas(tarefas_column, result_text),
        color=ft.Colors.DEEP_ORANGE_900,
        bgcolor=ft.Colors.DEEP_ORANGE_100,
        opacity=0.8
    )

    # Adiciona o plano de fundo como primeiro elemento da página
    page.add(
        ft.Stack(
            [
                ft.Container(
                    content=ft.Image(
                        src="src/assets/images/starwars_bg.jpg",
                        fit=ft.ImageFit.COVER
                    ),
                    expand=True,  # Expande o plano de fundo para ocupar toda a área da página
                    width=page.window.width,
                    height=page.window.height,
                    opacity=0.9  # Aumenta a opacidade do plano de fundo para 90%
                ),
                ft.Column(
                    [
                        titulo,
                        ft.Row(
                            [descricao_input, add_button],
                            alignment=ft.MainAxisAlignment.CENTER  # Centraliza o campo de descrição e botão
                        ),
                        tarefas_column,            
                        situacao_input,
                        result_text,
                        refresh_page_button
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza os elementos verticalmente
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centraliza os elementos horizontalmente
                    expand=True  # Expande os elementos para ocupar o espaço disponível
                )
            ]
        )
    )

    # Torna o plano de fundo responsivo ao redimensionamento da janela
    def on_resize(e):
        page.update()

    page.on_resize = on_resize

    # Inicializa a lista de tarefas
    atualizar_lista_tarefas(tarefas_column, result_text)

