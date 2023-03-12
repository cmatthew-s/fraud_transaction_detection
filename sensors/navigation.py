
import js
from js import document, console, alert

def click(event):
    target = event.target
    item_active = document.querySelector('.items.active')
    panel_active = document.querySelector('.panel.active')
    panels = document.querySelectorAll('.panel')

    item = target.className
    item_id = target.id
    item_target = document.getElementById(item_id)
    
    if 'active' not in item:
        item_active.classList.remove('active')
        item_target.classList.add('active')
        item_active = item_target

        panel_active.classList.remove('active')
        panels[int(item_id)].classList.add('active')
        panel_active = panels[int(item_id)]

    console.log(panel_active)

def nav_setup():
    items = document.querySelectorAll('.bar')
    clicked = create_proxy(click)
    for item in items:
        item.addEventListener('click', clicked)


   