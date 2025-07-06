import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import pandas as pd
import matplotlib.pyplot as plt
from openpyxl import load_workbook
from openpyxl.drawing.image import Image
image as Excellmage
# ======== CLASES ========

class Equipo:
    def__init__(self, codigo, nombre, tipo, supervisor, fecha, estado):
        self.codigo = codigo
        self.nombre = nombre
        self.tipo = tipo
        self.supervisor = supervisor
        self.fecha = fecha 
        self.estado = estado
        
    def to_dict(self):
        return{
            'codigo': self.codigo,
            'Nombre': sel.nombre,
            'Tipo': selelftipo,
            'Supervisor': sellfupervisor
            'FechaAdquisición': self.fecha
            'Estado':




            