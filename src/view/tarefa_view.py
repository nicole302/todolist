import flet as ft
from services.tarefa_service import cadastrar_tarefa, excluir_tarefas, listar_tarefas, editar_tarefa
from connection import Session
from model.tarefa_model import Tarefa  # Certifique-se de que o modelo se chama Tarefa
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import text  # Importa text para consultas SQL textuais

# Widget customizado para representar uma tarefa
class Task(ft.Row):
    def __init__(self, task: Tarefa):
        super().__init__()
        self.task = task
        #  status da tarefa
        self.checkbox = ft.Row(
            controls=[
                ft.Checkbox(value=task.situacao, on_change=self.on_checkbox_change, fill_color=ft.Colors.GREEN_100),
            ]
        )
        # Text para exibir a descrição com limite de 30 caracteres
        descricao_limitada = task.descricao if len(task.descricao) <= 30 else task.descricao[:30] + "..."
        self.text_view = ft.Text(descricao_limitada, color=ft.Colors.AMBER_500)  # Muda a cor do texto para AMBER_500
        # TextField para edição (inicialmente invisível)
        self.text_edit = ft.TextField(value=task.descricao, visible=False, color=ft.Colors.DEEP_ORANGE_900)
        # Botão para iniciar a edição
        self.edit_button = ft.IconButton(icon=ft.Icons.EDIT, on_click=self.edit, icon_color=ft.Colors.AMBER_900)
        # Botão para salvar a edição (inicialmente invisível)
        self.save_button = ft.IconButton(icon=ft.Icons.SAVE, visible=False, on_click=self.save, icon_color=ft.Colors.GREEN_ACCENT_700)
        # Botão para excluir a tarefa
        self.delete_button = ft.IconButton(icon=ft.Icons.DELETE, on_click=self.delete, icon_color=ft.Colors.RED_ACCENT_700)
        # Botão para atualizar a lista de tarefas
        #self.atualizar_listar_tarefas_button = ft.IconButton(icon=ft.Icons.REFRESH, on_click=self.listar_tarefas, icon_color=ft.Colors.YELLOW_700)
        
        self.controls = [
            self.checkbox,
            self.text_view,
            self.text_edit,
            self.edit_button,
            self.save_button,
            self.delete_button,
        ]
    
    def edit(self, e):
        # Ativa o modo edição: oculta o texto e mostra o campo de edição
        self.edit_button.visible = False
        self.save_button.visible = True
        self.text_view.visible = False
        self.text_edit.visible = True
        self.update()
    
    def save(self, e):
        # Ao salvar, atualiza a tarefa no banco e na interface
        new_text = self.text_edit.value
        checkbox_value = self.checkbox.controls[0].value  # Acessa o valor do Checkbox
        result = editar_tarefa(self.task.id, new_text, checkbox_value)
        if "editada com sucesso" in result:
            self.task.descricao = new_text
            self.text_view.value = new_text
        self.edit_button.visible = True
        self.save_button.visible = False
        self.text_view.visible = True
        self.text_edit.visible = False
        self.update()
    
    def delete(self, e):
        # Exclui a tarefa do banco e oculta o widget
        excluir_tarefas(self.task.id)
        self.visible = False
        self.update()
    
    def on_checkbox_change(self, e):
        # Atualiza o status da tarefa (checkbox)
        checkbox_value = self.checkbox.controls[0].value  # Acessa o valor do Checkbox
        result = editar_tarefa(self.task.id, self.task.descricao, checkbox_value)
        self.task.situacao = checkbox_value
        self.update()

    background_image = ft.Image(
        src="src/assets/images/starwars_bg.jpg",
        fit=ft.ImageFit.COVER,
        expand=True,)
    

# Função para verificar o estado das tarefas e exibir mensagens
def verificar_estado_tarefas(tasks_column, result_text):
    if not tasks_column.controls:
        result_text.value = "Você não tem tarefas. Adicione para que a Força esteja com você."
        result_text.font_family = "Nicole2"  # Define a fonte
        result_text.color = ft.Colors.YELLOW
    elif all(isinstance(control, Task) and control.checkbox.controls[0].value for control in tasks_column.controls):
        result_text.value = "Parabéns você concluiu todas as suas tarefas!"
        result_text.font_family = "Nicole2"  # Define a fonte
        result_text.color = ft.Colors.GREEN
    else:
        result_text.value = ""
    result_text.update()

# Função para gerenciar a sessão do banco de dados
def get_session():
    try:
        session = Session()
        # Testa a conexão executando uma consulta simples
        session.execute(text("SELECT 1"))  # Usa text para a consulta
        return session
    except OperationalError:
        # Fecha a sessão e cria uma nova em caso de erro
        session.close()
        return Session()

# Função para atualizar a lista de tarefas na interface
def atualizar_lista_tarefas(tasks_column, result_text=None):
    session = get_session()  # Usa a função para obter a sessão
    try:
        tasks_column.controls.clear()
        todas_tarefas = session.query(Tarefa).all()
        for task in todas_tarefas:
            tasks_column.controls.append(Task(task))
        tasks_column.update()
        if result_text:
            verificar_estado_tarefas(tasks_column, result_text)
    finally:
        session.close()


# Função acionada ao clicar no botão de adicionar tarefa
def on_add_tarefa_click(e, descricao_input, situacao_input, result_text, tasks_column):
    descricao = descricao_input.value.strip()  # Remove espaços em branco
    situacao = situacao_input.value  # Acessa o valor do Checkbox diretamente

    if not descricao:  # Verifica se a descrição está vazia
        result_text.value = "Erro: A descrição da tarefa não pode estar vazia."
        result_text.color = ft.Colors.RED
        result_text.update()
        return

    session = get_session()  # Usa a função para obter a sessão
    try:
        tarefa_id = cadastrar_tarefa(descricao, situacao)
        if tarefa_id:
            result_text.value = f"Tarefa cadastrada com sucesso!"
            result_text.color = ft.Colors.AMBER_500
            atualizar_lista_tarefas(tasks_column, result_text)  # Atualiza a lista de tarefas e verifica estado
        else:
            result_text.value = "Erro ao cadastrar a tarefa"
            result_text.color = ft.Colors.AMBER_500
    except OperationalError as e:
        result_text.value = f"Erro ao cadastrar tarefa: {str(e)}"
        result_text.color = ft.Colors.RED
    finally:
        session.close()
    result_text.update()


def main(page: ft.Page):
    page.title = "Task Manager"
    
    # Coluna para exibir as tarefas
    tasks_column = ft.Column()
    
    # Componentes para cadastro de nova tarefa
    new_task_desc = ft.TextField(label="Descrição da Tarefa", color=ft.Colors.DEEP_ORANGE_900)
    new_task_status = ft.Row(
        controls=[
            ft.Checkbox(label="", value=False),
    
        ]
    )
    result_text = ft.Text(color=ft.Colors.ORANGE)
    
    add_button = ft.ElevatedButton(
        text="Adicionar Tarefa",
        on_click=lambda e: on_add_tarefa_click(e, new_task_desc, new_task_status, result_text, tasks_column)
    )
    
    refresh_button = ft.ElevatedButton(
        text="Atualizar Lista",
        on_click=lambda e: atualizar_lista_tarefas(tasks_column, result_text)
    )
    
    # Monta a interface
    page.add(
        ft.Row([new_task_desc, new_task_status, add_button]),
        result_text,
        refresh_button,
        ft.Divider(),
        tasks_column
    )
    
    # Carrega as tarefas existentes
    atualizar_lista_tarefas(tasks_column, result_text)

