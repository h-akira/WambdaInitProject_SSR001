from wambda.shortcuts import render

def home(master):
  context = {}
  return render(master, 'home.html', context)

def custom_not_found_view(master):
  """Custom 404 view using not_found.html template"""
  context = {}
  return render(master, 'not_found.html', context, code=404)
