# interfaces.py
'''
Holds user-defined interfaces
'''
from flask import flash, render_template, redirect, url_for, request
#from app import app
#import sqlalchemy as sa
#from app import db
#from app.models import User

def security():
    '''
    Webpage for the Security.
    Shows tasks and cameras
    '''
    return "Security Interface"

def communications():
    '''
    Webpage for the Communcations.
    Shows tasks and comms sabotage fix
    '''
    return "Comms Interface"

def admin():
    '''
    Webpage for Admin.
    Shows tasks and lights sabotage fix
    '''
    return "Admin Interface"

def reactor():
    '''
    The webpage for Reactor.
    This Interface shows tasks and an emergency sabotage fix
    '''
    return "Reactor Interface"

route = {
    "Security": security, 
    "Communications": communications, 
    "Admin": admin, 
    "Reactor": reactor
}