import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import pandas as pd
import matplotlib.pyplot as plt
from openpyxl import load_workbook
from openpyxl.drawing.image import Image as ExcelImage

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
            'Codigo': self.codigo,
            'Nombre': self.nombre,
            'Tipo': self.tipo,
            'Supervisor': self.supervisor,
            'FechaAdquisicion': self.fecha,
            'Estado': self.estado
        }

class RegistroOperacion:
    def __init__(self, codigo_equipo, fecha, horas, toneladas, incidente, observaciones):
        self.codigo_equipo = codigo_equipo
        self.fecha = fecha
        self.horas = horas
        self.toneladas = toneladas
        self.incidente = incidente
        self.observaciones = observaciones

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
        if not self.df.empty:
            self.df['Fecha'] = pd.to_datetime(self.df['Fecha'])
        else:
            self.df = pd.DataFrame(columns=[
                'CodigoEquipo', 'Fecha', 'Horas', 'Toneladas', 'Incidente', 'Observaciones'
            ])
    
    def filtrar(self, codigo_equipo, fecha_ini, fecha_fin):
        mask = (
            (self.df['CodigoEquipo'] == codigo_equipo) &
            (self.df['Fecha'] >= pd.to_datetime(fecha_ini)) &
            (self.df['Fecha'] <= pd.to_datetime(fecha_fin))
        )
        return self.df[mask]
    
    def horas_totales(self, codigo_equipo, fecha_ini, fecha_fin):
        return self.filtrar(codigo_equipo, fecha_ini, fecha_fin)['Horas'].sum()
    
    def promedio_toneladas(self, codigo_equipo, fecha_ini, fecha_fin):
        return self.filtrar(codigo_equipo, fecha_ini, fecha_fin)['Toneladas'].mean()
    
    def porcentaje_incidentes(self, codigo_equipo, fecha_ini, fecha_fin):
        df_filt = self.filtrar(codigo_equipo, fecha_ini, fecha_fin)
        if df_filt.empty:
            return 0.0
        return (df_filt['Incidente'].str.lower() == 'sí').mean() * 100
    
    def evolucion_toneladas(self, codigo_equipo, fecha_ini, fecha_fin):
        df_filt = self.filtrar(codigo_equipo, fecha_ini, fecha_fin)
        df_filt = df_filt.sort_values('Fecha')
        return df_filt[['Fecha', 'Toneladas']]

# ======== DATOS EN MEMORIA ========

equipos = []
registros = []

# ======== FUNCIONES TKINTER Y NEGOCIO ========

def guardar_equipo():
    codigo = entry_codigo.get().strip()
    nombre = entry_nombre.get().strip()
    tipo = combo_tipo.get()
    supervisor = entry_supervisor.get().strip()
    fecha = entry_fecha.get()
    estado = combo_estado.get()

    if entry_codigo['state'] == 'disabled':
        messagebox.showerror('Error', 'Para agregar un equipo nuevo, presiona "Limpiar" antes.')
        return

    if len(codigo) != 6 or not codigo.isalnum():
        messagebox.showerror('Error', 'Código: 6 caracteres alfanuméricos.')
        return
    if len(nombre) == 0 or len(nombre) > 30:
        messagebox.showerror('Error', 'Nombre: 1-30 caracteres.')
        return
    if not tipo:
        messagebox.showerror('Error', 'Seleccione tipo.')
        return
    if not supervisor:
        messagebox.showerror('Error', 'Ingrese supervisor.')
        return
    if not estado:
        messagebox.showerror('Error', 'Seleccione estado.')
        return
    if any(eq['Codigo'] == codigo for eq in equipos):
        messagebox.showerror('Error', 'Código de equipo duplicado.')
        return

    eq = Equipo(codigo, nombre, tipo, supervisor, fecha, estado)
    equipos.append(eq.to_dict())
    messagebox.showinfo('Guardado', 'Equipo registrado.')
    limpiar_equipo()
    actualizar_lista_equipos()

def limpiar_equipo():
    entry_codigo.config(state='normal')
    entry_codigo.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    combo_tipo.set('')
    entry_supervisor.delete(0, tk.END)
    entry_fecha.set_date(pd.Timestamp.now().date())
    combo_estado.set('')

def cargar_equipo():
    codigo_sel = combo_codigo_buscar.get()
    if not codigo_sel:
        messagebox.showerror('Error', 'Seleccione un código de equipo para modificar.')
        return
    for eq in equipos:
        if eq['Codigo'] == codigo_sel:
            entry_codigo.delete(0, tk.END)
            entry_codigo.insert(0, eq['Codigo'])
            entry_nombre.delete(0, tk.END)
            entry_nombre.insert(0, eq['Nombre'])
            combo_tipo.set(eq['Tipo'])
            entry_supervisor.delete(0, tk.END)
            entry_supervisor.insert(0, eq['Supervisor'])
            entry_fecha.set_date(eq['FechaAdquisicion'])
            combo_estado.set(eq['Estado'])
            entry_codigo.config(state='disabled')
            return

def guardar_modificacion():
    codigo = entry_codigo.get().strip()
    nombre = entry_nombre.get().strip()
    tipo = combo_tipo.get()
    supervisor = entry_supervisor.get().strip()
    fecha = entry_fecha.get()
    estado = combo_estado.get()
    # Validaciones igual que antes, menos código
    if len(nombre) == 0 or len(nombre) > 30:
        messagebox.showerror('Error', 'Nombre: 1-30 caracteres.')
        return
    if not tipo:
        messagebox.showerror('Error', 'Seleccione tipo.')
        return
    if not supervisor:
        messagebox.showerror('Error', 'Ingrese supervisor.')
        return
    if not estado:
        messagebox.showerror('Error', 'Seleccione estado.')
        return
    for eq in equipos:
        if eq['Codigo'] == codigo:
            eq['Nombre'] = nombre
            eq['Tipo'] = tipo
            eq['Supervisor'] = supervisor
            eq['FechaAdquisicion'] = fecha
            eq['Estado'] = estado
            messagebox.showinfo('Modificado', 'Equipo modificado correctamente.')
            limpiar_equipo()
            actualizar_lista_equipos()
            return
    messagebox.showerror('Error', 'No se encontró el equipo a modificar.')

def guardar_registro():
    codigo_equipo = combo_equipo_registro.get()
    fecha = entry_fecha_registro.get()
    try:
        horas = float(entry_horas.get())
        if not (0 <= horas <= 24):
            raise ValueError
    except:
        messagebox.showerror('Error', 'Horas: valor entre 0 y 24.')
        return
    try:
        toneladas = float(entry_toneladas.get())
    except:
        messagebox.showerror('Error', 'Toneladas: valor real.')
        return
    incidente = combo_incidente.get()
    obs = entry_observaciones.get()
    if not codigo_equipo:
        messagebox.showerror('Error', 'Seleccione código de equipo.')
        return
    if len(obs) > 256:
        messagebox.showerror('Error', 'Observaciones: máximo 256 caracteres.')
        return
    reg = RegistroOperacion(
        codigo_equipo, fecha, horas, toneladas, incidente, obs
    )
    registros.append(reg.to_dict())
    messagebox.showinfo('Guardado', 'Registro diario guardado.')
    limpiar_registro()

def limpiar_registro():
    combo_equipo_registro.set('')
    entry_fecha_registro.set_date(pd.Timestamp.now().date())
    entry_horas.delete(0, tk.END)
    entry_toneladas.delete(0, tk.END)
    combo_incidente.set('')
    entry_observaciones.delete(0, tk.END)

def exportar():
    if not equipos:
        messagebox.showwarning('Aviso', 'No hay equipos registrados.')
        return
    df_eq = pd.DataFrame(equipos)
    df_reg = pd.DataFrame(registros)
    with pd.ExcelWriter('equipos_mineria.xlsx') as writer:
        df_eq.to_excel(writer, sheet_name='equipos', index=False)
        df_reg.to_excel(writer, sheet_name='registros', index=False)
    # Gráfico: equipos por tipo
    if not df_eq.empty:
        plt.figure()
        df_eq['Tipo'].value_counts().plot.bar(color='lightsteelblue')
        plt.title('Cantidad de equipos por tipo')
        plt.tight_layout()
        plt.savefig('grafico_equipos.png')
        plt.close()
        wb = load_workbook('equipos_mineria.xlsx')
        ws = wb['equipos']
        img = ExcelImage('grafico_equipos.png')
        img.anchor = 'H2'
        ws.add_image(img)
        wb.save('equipos_mineria.xlsx')
    messagebox.showinfo('Exportado', 'Datos exportados a Excel (equipos y registros)')

def actualizar_lista_equipos():
    codigos = [eq['Codigo'] for eq in equipos]
    combo_equipo_registro['values'] = codigos
    combo_codigo_buscar['values'] = codigos
    # Limpiar y llenar listbox (para análisis)
    listbox_equipo_analisis.delete(0, tk.END)
    for c in codigos:
        listbox_equipo_analisis.insert(tk.END, c)

def mostrar_analisis():
    seleccion = listbox_equipo_analisis.curselection()
    cods = [listbox_equipo_analisis.get(i) for i in seleccion]
    f1 = entry_fecha_ini.get()
    f2 = entry_fecha_fin.get()
    if not cods or not f1 or not f2:
        messagebox.showerror('Error', 'Complete selección.')
        return
    analizador = AnalizadorOperacion(registros)
    if len(cods) == 1:
        cod = cods[0]
        total_horas = analizador.horas_totales(cod, f1, f2)
        prom_ton = analizador.promedio_toneladas(cod, f1, f2)
        porc_inc = analizador.porcentaje_incidentes(cod, f1, f2)
        df_evo = analizador.evolucion_toneladas(cod, f1, f2)

        if df_evo.empty:
            messagebox.showinfo('Sin datos', 'No hay registros en el rango.')
            lbl_horas.config(text='Horas totales:')
            lbl_toneladas.config(text='Promedio toneladas:')
            lbl_incidentes.config(text='% días con incidente:')
            return

        lbl_horas.config(text=f'Horas totales: {total_horas:.2f}')
        lbl_toneladas.config(text=f'Promedio toneladas: {prom_ton:.2f}')
        lbl_incidentes.config(text=f'% días con incidente: {porc_inc:.1f}%')

        plt.figure()
        plt.plot(df_evo['Fecha'], df_evo['Toneladas'], marker='o')
        plt.title(f'Evolución toneladas movidas - {cod}')
        plt.xlabel('Fecha')
        plt.ylabel('Toneladas')
        plt.tight_layout()
        plt.savefig('grafico_analisis.png')
        plt.close()
        img_ventana = tk.Toplevel(ventana)
        img_ventana.title('Gráfico evolución toneladas')
        img = tk.PhotoImage(file='grafico_analisis.png')
        label_img = tk.Label(img_ventana, image=img)
        label_img.image = img
        label_img.pack()
    elif len(cods) > 1:
        # Comparación múltiple
        promedios = []
        for cod in cods:
            prom = analizador.promedio_toneladas(cod, f1, f2)
            if not pd.isna(prom):
                promedios.append(prom)
            else:
                promedios.append(0)
        plt.figure()
        plt.bar(cods, promedios, color='mediumslateblue')
        plt.title('Comparación de promedio de toneladas movidas')
        plt.xlabel('Equipo')
        plt.ylabel('Promedio toneladas')
        plt.tight_layout()
        plt.savefig('grafico_comparacion.png')
        plt.close()
        img_ventana = tk.Toplevel(ventana)
        img_ventana.title('Comparación de equipos')
        img = tk.PhotoImage(file='grafico_comparacion.png')
        label_img = tk.Label(img_ventana, image=img)
        label_img.image = img
        label_img.pack()
        lbl_horas.config(text='Horas totales:')
        lbl_toneladas.config(text='Promedio toneladas:')
        lbl_incidentes.config(text='% días con incidente:')
    else:
        messagebox.showinfo('Sin datos', 'No hay equipos seleccionados.')

# ======== INTERFAZ TKINTER ========

ventana = tk.Tk()
ventana.title('Gestión de Equipos y Operaciones Mineras')

# --- Sección equipos ---
frame_eq = tk.LabelFrame(ventana, text='Registro de Equipos')
frame_eq.grid(row=0, column=0, padx=10, pady=10)

tk.Label(frame_eq, text='Código (6 caracteres)').grid(row=0, column=0)
entry_codigo = tk.Entry(frame_eq)
entry_codigo.grid(row=0, column=1)

tk.Label(frame_eq, text='Seleccionar código').grid(row=0, column=2)
combo_codigo_buscar = ttk.Combobox(frame_eq, state='readonly')
combo_codigo_buscar.grid(row=0, column=3)
tk.Button(frame_eq, text='Cargar datos', command=cargar_equipo).grid(row=1, column=3)

tk.Label(frame_eq, text='Nombre equipo').grid(row=1, column=0)
entry_nombre = tk.Entry(frame_eq)
entry_nombre.grid(row=1, column=1)

tk.Label(frame_eq, text='Tipo').grid(row=2, column=0)
combo_tipo = ttk.Combobox(frame_eq, values=['Perforadora', 'Cargador', 'Volquete', 'Otro'], state='readonly')
combo_tipo.grid(row=2, column=1)

tk.Label(frame_eq, text='Supervisor').grid(row=3, column=0)
entry_supervisor = tk.Entry(frame_eq)
entry_supervisor.grid(row=3, column=1)

tk.Label(frame_eq, text='Fecha adquisición').grid(row=4, column=0)
entry_fecha = DateEntry(frame_eq, date_pattern='yyyy-mm-dd')
entry_fecha.grid(row=4, column=1)

tk.Label(frame_eq, text='Estado').grid(row=5, column=0)
combo_estado = ttk.Combobox(frame_eq, values=['Activo', 'Inactivo'], state='readonly')
combo_estado.grid(row=5, column=1)

tk.Button(frame_eq, text='Guardar equipo', command=guardar_equipo).grid(row=6, column=0, columnspan=2)
tk.Button(frame_eq, text='Guardar cambios', command=guardar_modificacion).grid(row=7, column=0, columnspan=2)
tk.Button(frame_eq, text='Limpiar', command=limpiar_equipo).grid(row=8, column=0, columnspan=2)

# --- Sección registros ---
frame_reg = tk.LabelFrame(ventana, text='Registro operativo diario')
frame_reg.grid(row=1, column=0, padx=10, pady=10)

tk.Label(frame_reg, text='Código equipo').grid(row=0, column=0)
combo_equipo_registro = ttk.Combobox(frame_reg, state='readonly')
combo_equipo_registro.grid(row=0, column=1)

tk.Label(frame_reg, text='Fecha').grid(row=1, column=0)
entry_fecha_registro = DateEntry(frame_reg, date_pattern='yyyy-mm-dd')
entry_fecha_registro.grid(row=1, column=1)

tk.Label(frame_reg, text='Horas operación').grid(row=2, column=0)
entry_horas = tk.Entry(frame_reg)
entry_horas.grid(row=2, column=1)

tk.Label(frame_reg, text='Toneladas movidas').grid(row=3, column=0)
entry_toneladas = tk.Entry(frame_reg)
entry_toneladas.grid(row=3, column=1)

tk.Label(frame_reg, text='Incidente (Sí/No)').grid(row=4, column=0)
combo_incidente = ttk.Combobox(frame_reg, values=['Sí', 'No'], state='readonly')
combo_incidente.grid(row=4, column=1)

tk.Label(frame_reg, text='Observaciones').grid(row=5, column=0)
entry_observaciones = tk.Entry(frame_reg)
entry_observaciones.grid(row=5, column=1)

tk.Button(frame_reg, text='Guardar registro', command=guardar_registro).grid(row=6, column=0, columnspan=2)

# --- Sección exportar ---
tk.Button(ventana, text='Exportar Excel', command=exportar).grid(row=2, column=0, pady=10)

# --- Sección análisis ---
frame_an = tk.LabelFrame(ventana, text='Análisis Operativo por Equipo')
frame_an.grid(row=0, column=1, rowspan=3, padx=10, pady=10)

tk.Label(frame_an, text='Equipos').grid(row=0, column=0)
listbox_equipo_analisis = tk.Listbox(frame_an, selectmode='multiple', height=5, exportselection=0)
listbox_equipo_analisis.grid(row=0, column=1)

tk.Label(frame_an, text='Fecha inicio').grid(row=1, column=0)
entry_fecha_ini = DateEntry(frame_an, date_pattern='yyyy-mm-dd')
entry_fecha_ini.grid(row=1, column=1)

tk.Label(frame_an, text='Fecha fin').grid(row=2, column=0)
entry_fecha_fin = DateEntry(frame_an, date_pattern='yyyy-mm-dd')
entry_fecha_fin.grid(row=2, column=1)

tk.Button(frame_an, text='Mostrar análisis', command=mostrar_analisis).grid(row=3, column=0, columnspan=2, pady=5)

lbl_horas = tk.Label(frame_an, text='Horas totales:')
lbl_horas.grid(row=4, column=0, columnspan=2)
lbl_toneladas = tk.Label(frame_an, text='Promedio toneladas:')
lbl_toneladas.grid(row=5, column=0, columnspan=2)
lbl_incidentes = tk.Label(frame_an, text='% días con incidente:')
lbl_incidentes.grid(row=6, column=0, columnspan=2)

# ======== Inicializa combos y listas ========
actualizar_lista_equipos()

ventana.mainloop()
