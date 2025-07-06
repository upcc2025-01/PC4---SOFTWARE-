import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import pandas as pd
import matplotlib.pyplot as plt
from openpyxl import load_workbook
from openpyxl.drawing.image import Image as Excellmage

# ======== CLASES ========

class Equipo:
    def __init__(self, codigo, nombre, tipo, supervisor, fecha, estado):
        self.codigo = codigo
        self.nombre = nombre
        self.tipo = tipo
        self.supervisor = supervisor
        self.fecha = fecha 
        self.estado = estado
        
    def to_dict(self):
        return {
            'codigo': self.codigo,
            'Nombre': sel.nombre,
            'Tipo': selelftipo,
            'Supervisor': sellfupervisor,
            'FechaAdquisición': self.fecha,
            'Estado': self.estado
        }

class RegistroOperacion:
    def __init__(self,codigo_equipo, fecha, horas, toneladas, incidente, observaciones):
        self.codigo_equipo: codigo_equipo
        self.fecha: fecha
        self.horas: horas
        self.toneladas: toneladas
        self.incidente: incidente
        self.observaciones: observaciones

    def to_dict(self):
        return {
            'CodigoEquipo': self.codigo_equipo,
            'Fecha': self.fecha,
            'Horas': self.horas,
            'Toneladas': self.toneladas,
            'Incidente': self.incidente,
            'Observaciones': self.observaciones            
        }         

class AnalizadorOperacion:
    def __init__(self, registros):
        self.df = pd.DataFrame(registros)
        if not self.dt .empty:
            self.df['Fecha'] =pd.to_datetime(self.df['Fecha'])
        else:
            self.df = pd.DataFrame( columns) 
    
    def filtrar(self, codigo_equipo, fecha_ini, fecha_fin):
        mask = (
            (self.df['Codig'Equipo"] == codigo_equipo)&
            (self.df['Fecha'] >= pd.to_datatime(fecha_ini)) &   
                return self.df[mask] 
                )
    

    def

