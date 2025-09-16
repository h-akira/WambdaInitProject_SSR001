from wambda.shortcuts import render, redirect, login_required
from .forms import TodoForm, CategoryForm
from datetime import datetime, timezone
import uuid
import boto3
import os

# DynamoDB helper functions
def get_table():
    """DynamoDBテーブルを取得"""
    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-1')
    table_name = os.environ.get('DYNAMODB_TABLE', 'wambda-table-ssr001')
    return dynamodb.Table(table_name)

def get_data_by_pk(pk):
    """PKで複数のアイテムを取得"""
    table = get_table()
    response = table.query(KeyConditionExpression=boto3.dynamodb.conditions.Key('pk').eq(pk))
    return response['Items']

def get_data_by_pk_sk(pk, sk):
    """PKとSKで単一アイテムを取得"""
    table = get_table()
    response = table.get_item(Key={'pk': pk, 'sk': sk})
    return response.get('Item')

def put_data(item):
    """アイテムを保存"""
    table = get_table()
    table.put_item(Item=item)

def delete_data_by_pk_sk(pk, sk):
    """PKとSKでアイテムを削除"""
    table = get_table()
    table.delete_item(Key={'pk': pk, 'sk': sk})

@login_required
def dashboard(master, username):
    """ダッシュボードページ"""
    if master.request.username != username:
        return redirect(master, "accounts:login")
    
    # 最近のTodos取得
    all_todos = get_data_by_pk(f"user#{username}#todo")
    
    # 完了/未完了の統計
    total_todos = len(all_todos)
    completed_todos = len([t for t in all_todos if t.get('completed', False)])
    pending_todos = total_todos - completed_todos
    
    # 優先度別統計
    priority_stats = {"high": 0, "medium": 0, "low": 0}
    for todo in all_todos:
        priority = todo.get('priority', 'medium')
        priority_stats[priority] = priority_stats.get(priority, 0) + 1
    
    context = {
        'username': username,
        'total_todos': total_todos,
        'completed_todos': completed_todos,
        'pending_todos': pending_todos,
        'priority_stats': priority_stats,
        'recent_todos': all_todos[:5]  # 最新5件
    }
    
    return render(master, 'todo/dashboard.html', context)

@login_required
def todo_list(master, username):
    """Todo一覧ページ"""
    if master.request.username != username:
        return redirect(master, "accounts:login")
    
    todos = get_data_by_pk(f"user#{username}#todo")
    categories = get_data_by_pk(f"user#{username}#category")
    
    # フィルタリング
    query_params = master.event.get('queryStringParameters') or {}
    filter_status = query_params.get('status', 'all')
    filter_priority = query_params.get('priority', 'all')
    filter_category = query_params.get('category', 'all')
    
    if filter_status != 'all':
        completed = (filter_status == 'completed')
        todos = [t for t in todos if t.get('completed', False) == completed]
    
    if filter_priority != 'all':
        todos = [t for t in todos if t.get('priority') == filter_priority]
    
    if filter_category != 'all':
        todos = [t for t in todos if t.get('category_id') == filter_category]
    
    context = {
        'username': username,
        'todos': todos,
        'categories': categories,
        'filter_status': filter_status,
        'filter_priority': filter_priority,
        'filter_category': filter_category
    }
    
    return render(master, 'todo/todo_list.html', context)

@login_required
def todo_create(master, username):
    """Todo作成ページ"""
    if master.request.username != username:
        return redirect(master, "accounts:login")
    
    categories = get_data_by_pk(f"user#{username}#category")
    
    if master.request.method == "POST":
        form_data = master.request.get_form_data()
        form = TodoForm(form_data)
        if form.validate():
            now = datetime.now(timezone.utc)
            todo_id = str(uuid.uuid4())
            
            todo_data = {
                'pk': f"user#{username}#todo",
                'sk': todo_id,
                'title': form.data['title'],
                'description': form.data['description'],
                'priority': form.data['priority'],
                'completed': form.data.get('completed', False),
                'category_id': form_data.get('category_id', ''),
                'created_at': now.isoformat(),
                'updated_at': now.isoformat()
            }
            
            put_data(todo_data)
            return redirect(master, "todo:todo_list", username=username)
    else:
        form = TodoForm()
    
    context = {
        'username': username,
        'form': form,
        'categories': categories,
        'action': 'create'
    }
    
    return render(master, 'todo/todo_form.html', context)

@login_required
def todo_edit(master, username, todo_id):
    """Todo編集ページ"""
    if master.request.username != username:
        return redirect(master, "accounts:login")
    
    todo = get_data_by_pk_sk(f"user#{username}#todo", todo_id)
    if not todo:
        return render(master, 'not_found.html', {}, code=404)
    
    categories = get_data_by_pk(f"user#{username}#category")
    
    if master.request.method == "POST":
        form_data = master.request.get_form_data()
        form = TodoForm(form_data)
        if form.validate():
            now = datetime.now(timezone.utc)
            
            todo['title'] = form.data['title']
            todo['description'] = form.data['description']
            todo['priority'] = form.data['priority']
            todo['completed'] = form.data.get('completed', False)
            todo['category_id'] = form_data.get('category_id', '')
            todo['updated_at'] = now.isoformat()
            
            put_data(todo)
            return redirect(master, "todo:todo_list", username=username)
    else:
        form = TodoForm({
            'title': todo.get('title', ''),
            'description': todo.get('description', ''),
            'priority': todo.get('priority', 'medium'),
            'completed': todo.get('completed', False)
        })
    
    context = {
        'username': username,
        'form': form,
        'todo': todo,
        'categories': categories,
        'action': 'edit'
    }
    
    return render(master, 'todo/todo_form.html', context)

@login_required
def todo_delete(master, username, todo_id):
    """Todo削除"""
    if master.request.username != username:
        return redirect(master, "accounts:login")
    
    todo = get_data_by_pk_sk(f"user#{username}#todo", todo_id)
    if not todo:
        return render(master, 'not_found.html', {}, code=404)
    
    delete_data_by_pk_sk(f"user#{username}#todo", todo_id)
    return redirect(master, "todo:todo_list", username=username)

@login_required
def todo_toggle_complete(master, username, todo_id):
    """Todo完了状態の切り替え"""
    if master.request.username != username:
        return redirect(master, "accounts:login")
    
    todo = get_data_by_pk_sk(f"user#{username}#todo", todo_id)
    if todo:
        todo['completed'] = not todo.get('completed', False)
        todo['updated_at'] = datetime.now(timezone.utc).isoformat()
        put_data(todo)
    
    return redirect(master, "todo:todo_list", username=username)

@login_required
def category_list(master, username):
    """カテゴリー一覧ページ"""
    if master.request.username != username:
        return redirect(master, "accounts:login")
    
    categories = get_data_by_pk(f"user#{username}#category")
    
    context = {
        'username': username,
        'categories': categories
    }
    
    return render(master, 'todo/category_list.html', context)

@login_required
def category_create(master, username):
    """カテゴリー作成ページ"""
    if master.request.username != username:
        return redirect(master, "accounts:login")
    
    if master.request.method == "POST":
        form = CategoryForm(master.request.get_form_data())
        if form.validate():
            now = datetime.now(timezone.utc)
            category_id = str(uuid.uuid4())
            
            category_data = {
                'pk': f"user#{username}#category",
                'sk': category_id,
                'name': form.data['name'],
                'color': form.data['color'],
                'created_at': now.isoformat(),
                'updated_at': now.isoformat()
            }
            
            put_data(category_data)
            return redirect(master, "todo:category_list", username=username)
    else:
        form = CategoryForm()
    
    context = {
        'username': username,
        'form': form,
        'action': 'create'
    }
    
    return render(master, 'todo/category_form.html', context)

@login_required
def category_edit(master, username, category_id):
    """カテゴリー編集ページ"""
    if master.request.username != username:
        return redirect(master, "accounts:login")
    
    category = get_data_by_pk_sk(f"user#{username}#category", category_id)
    if not category:
        return render(master, 'not_found.html', {}, code=404)
    
    if master.request.method == "POST":
        form = CategoryForm(master.request.get_form_data())
        if form.validate():
            now = datetime.now(timezone.utc)
            
            category['name'] = form.data['name']
            category['color'] = form.data['color']
            category['updated_at'] = now.isoformat()
            
            put_data(category)
            return redirect(master, "todo:category_list", username=username)
    else:
        form = CategoryForm({
            'name': category.get('name', ''),
            'color': category.get('color', 'blue')
        })
    
    context = {
        'username': username,
        'form': form,
        'category': category,
        'action': 'edit'
    }
    
    return render(master, 'todo/category_form.html', context)

@login_required
def category_delete(master, username, category_id):
    """カテゴリー削除"""
    if master.request.username != username:
        return redirect(master, "accounts:login")
    
    category = get_data_by_pk_sk(f"user#{username}#category", category_id)
    if not category:
        return render(master, 'not_found.html', {}, code=404)
    
    delete_data_by_pk_sk(f"user#{username}#category", category_id)
    return redirect(master, "todo:category_list", username=username)