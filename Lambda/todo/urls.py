from wambda.urls import Path
from .views import (
    todo_create, todo_edit, todo_delete, todo_toggle_complete,
    category_list, category_create, category_edit, category_delete,
    dashboard
)

urlpatterns = [
    # Dashboard (統合Todo管理)
    Path("{username}/dashboard", dashboard, name="dashboard"),
    
    # Todo management
    Path("{username}/todos/create", todo_create, name="todo_create"),
    Path("{username}/todos/{todo_id}/edit", todo_edit, name="todo_edit"),
    Path("{username}/todos/{todo_id}/delete", todo_delete, name="todo_delete"),
    Path("{username}/todos/{todo_id}/toggle", todo_toggle_complete, name="todo_toggle"),
    
    # Category management
    Path("{username}/categories", category_list, name="category_list"),
    Path("{username}/categories/create", category_create, name="category_create"),
    Path("{username}/categories/{category_id}/edit", category_edit, name="category_edit"),
    Path("{username}/categories/{category_id}/delete", category_delete, name="category_delete"),
]