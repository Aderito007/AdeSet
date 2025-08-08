from tkcalendar import calendar_
import tkinter as tk
import tkinter.ttk as ttk_original  # ttk padrão
import datetime

# Força o tkcalendar usar o ttk original
calendar_.ttk = ttk_original
Calendar = calendar_.Calendar

class CalendarioBase:
    def __init__(self, parent, callback, formato="dd/MM/yyyy", titulo="Selecionar data"):
        self.callback = callback
        self.formato = formato

        self.popup = tk.Toplevel()
        self.popup.title(titulo)
        self.popup.geometry("280x300")
        self.popup.grab_set()

        hoje = datetime.date.today()

        self.cal = Calendar(self.popup,
                            selectmode="day",
                            date_pattern=formato,
                            year=hoje.year,
                            month=hoje.month,
                            day=hoje.day,
                            mindate=datetime.date(1900, 1, 1),
                            maxdate=hoje)
        self.cal.pack(pady=10)

        tk.Button(self.popup, text="✅ Confirmar",
                  command=self.confirmar).pack(pady=5)

    def confirmar(self):
        data = self.cal.get_date()
        self.callback(data)
        self.popup.destroy()