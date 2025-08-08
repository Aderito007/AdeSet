# institucional/widgets/data/data_field.py
from widgets.calendariobase import CalendarioBase
from ttkbootstrap import ttk
import datetime

   

class DataField(ttk.Frame):
    def __init__(self, parent, titulo="Selecionar data", largura=30, formato="dd/MM/yyyy"):
        super().__init__(parent)
        self.formato = formato

        self.entry = ttk.Entry(self, width=largura)
        self.entry.grid(row=0, column=0, padx=(0, 5))

        self.btn = ttk.Button(self, text="📅", width=3, bootstyle="info",
                              command=self.abrir_calendario)
        self.btn.grid(row=0, column=1)

        self.entry.insert(0, datetime.date.today().strftime(self._conversor_format()))


    def abrir_calendario(self):
        CalendarioBase(
            parent=self,
            formato=self.formato,
            callback=lambda data: self.set(data),
            titulo="🗓️ " + self.entry.get()
        )


    def get(self):
        return self.entry.get()

    def set(self, data_str):
        self.entry.delete(0, "end")
        self.entry.insert(0, data_str)

    def _conversor_format(self):
        # Converte dd/MM/yyyy → %d/%m/%Y para strftime
        return self.formato.replace("dd", "%d").replace("MM", "%m").replace("yyyy", "%Y")