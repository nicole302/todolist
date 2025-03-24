import flet as ft
from view.tarefa_view import on_add_tarefa_click, atualizar_lista_tarefas

def main(page: ft.Page):
    page.title = "Cadastro de Tarefa"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = ft.Colors.BLACK
    page.window.width = 400
    page.window.height = 600
    page.window.resizable = False
    page.window.always_on_top = True
    page.scroll = 'adptative' # Só quando for necessário

    page.fonts = {
        "Nicole": "src/assets/fonts/sf_distant_galaxy/SF Distant Galaxy Outline Italic.ttf"
    }

    titulo = ft.Text("To do List", font_family='Nicole', text_align='center', size = 50, color = ft.Colors.YELLOW_ACCENT_700)

    # Campo de entrada para a descrição da tarefa
    descricao_input = ft.TextField(label="Descrição da Tarefa", autofocus=True, width=300, color = ft.Colors.YELLOW_ACCENT_700)
    
    # Coluna para exibir a lista de tarefas
    tarefas_column = ft.Column()

    # Botão para adicionar a tarefa
    add_button = ft.ElevatedButton("Cadastrar Tarefa", on_click=lambda e: on_add_tarefa_click(e, descricao_input, situacao_input, result_text, tarefas_column))
    
    # Área de resultado (onde será mostrado se a tarefa foi cadastrada ou não)
    result_text = ft.Text()

    # Campo de entrada para a situação (Checkbox)
    situacao_input = ft.Checkbox(label="Tarefa concluída", value=False)
    
    # Adiciona todos os componentes na página
    page.add(titulo, descricao_input, add_button, result_text, tarefas_column, situacao_input)

    # Inicializa a lista de tarefas
    atualizar_lista_tarefas(tarefas_column)

