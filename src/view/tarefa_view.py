import flet as ft
from services.tarefa_service import cadastrar_tarefa, excluir_tarefas, listar_tarefas, editar_tarefa
from connection import Session
from model.tarefa_model import Tarefa  # Certifique-se de que o modelo se chama Tarefa

# Widget customizado para representar uma tarefa
class Task(ft.Row):
    def __init__(self, task: Tarefa):
        super().__init__()
        self.task = task
        #  status da tarefa
        self.checkbox = ft.Checkbox(value=task.situacao, on_change=self.on_checkbox_change)
        # Text para exibir a descrição
        self.text_view = ft.Text(task.descricao)
        # TextField para edição (inicialmente invisível)
        self.text_edit = ft.TextField(value=task.descricao, visible=False)
        # Botão para iniciar a edição
        self.edit_button = ft.IconButton(icon=ft.Icons.EDIT, on_click=self.edit)
        # Botão para salvar a edição (inicialmente invisível)
        self.save_button = ft.IconButton(icon=ft.Icons.SAVE, visible=False, on_click=self.save)
        # Botão para excluir a tarefa
        self.delete_button = ft.IconButton(icon=ft.Icons.DELETE, on_click=self.delete)
        
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
        result = editar_tarefa(self.task.id, new_text, self.checkbox.value)
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
        result = editar_tarefa(self.task.id, self.task.descricao, self.checkbox.value)
        self.task.situacao = self.checkbox.value
        self.update()


# Função para atualizar a lista de tarefas na interface
def atualizar_lista_tarefas(tasks_column):
    session = Session()
    try:
        tasks_column.controls.clear()
        todas_tarefas = session.query(Tarefa).all()
        for task in todas_tarefas:
            tasks_column.controls.append(Task(task))
        tasks_column.update()
    finally:
        session.close()


# Função acionada ao clicar no botão de adicionar tarefa
def on_add_tarefa_click(e, descricao_input, situacao_input, result_text, tasks_column):
    descricao = descricao_input.value
    situacao = situacao_input.value
    tarefa_id = cadastrar_tarefa(descricao, situacao)
    if tarefa_id:
        result_text.value = f"Tarefa cadastrada com sucesso! ID: {tarefa_id}"
        atualizar_lista_tarefas(tasks_column)  # Atualiza a lista de tarefas
    else:
        result_text.value = "Erro ao cadastrar a tarefa"
    result_text.update()


def main(page: ft.Page):
    page.title = "Task Manager"
    
    # Coluna para exibir as tarefas
    tasks_column = ft.Column()
    
    # Componentes para cadastro de nova tarefa
    new_task_desc = ft.TextField(label="Descrição da Tarefa")
    new_task_status = ft.Checkbox(label="Concluída")
    result_text = ft.Text()
    
    add_button = ft.ElevatedButton(
        text="Adicionar Tarefa",
        on_click=lambda e: on_add_tarefa_click(e, new_task_desc, new_task_status, result_text, tasks_column)
    )
    
    refresh_button = ft.ElevatedButton(
        text="Atualizar Lista",
        on_click=lambda e: atualizar_lista_tarefas(tasks_column)
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
    atualizar_lista_tarefas(tasks_column)

