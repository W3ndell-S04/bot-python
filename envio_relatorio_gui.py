import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import tkinter as tk
from tkinter import filedialog, messagebox

# Variável global para armazenar o caminho do arquivo de relatório
attachment_path = None

# Função para selecionar o arquivo de relatório
def select_file():
    global attachment_path
    attachment_path = filedialog.askopenfilename(title="Selecione o arquivo de relatório", filetypes=[("PDF files", "*.pdf")])
    if attachment_path:
        file_label.config(text=f"Arquivo selecionado: {os.path.basename(attachment_path)}")
    else:
        file_label.config(text="Nenhum arquivo selecionado")

# Função para enviar o e-mail
def send_email():
    smtp_server = 'smtp.seu-servidor.com'
    smtp_port = 587
    smtp_user = 'seu-email@exemplo.com'
    smtp_password = 'sua-senha'
    from_addr = 'seu-email@exemplo.com'
    to_addr = to_entry.get()
    subject = 'Relatório Diário'
    body = body_entry.get("1.0", tk.END).strip()

    if not attachment_path:
        messagebox.showerror("Erro", "Nenhum arquivo selecionado!")
        return

    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    filename = os.path.basename(attachment_path)
    with open(attachment_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {filename}')
        msg.attach(part)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        text = msg.as_string()
        server.sendmail(from_addr, to_addr, text)
        server.quit()
        messagebox.showinfo("Sucesso", "E-mail enviado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao enviar o e-mail: {str(e)}")

# Configurar a interface gráfica
root = tk.Tk()
root.title("Envio de Relatório Diário")

# Label e entry para o e-mail do destinatário
tk.Label(root, text="E-mail do destinatário:").grid(row=0, column=0, padx=10, pady=10)
to_entry = tk.Entry(root, width=50)
to_entry.grid(row=0, column=1, padx=10, pady=10)

# Label e entry para o corpo do e-mail
tk.Label(root, text="Corpo do e-mail:").grid(row=1, column=0, padx=10, pady=10)
body_entry = tk.Text(root, height=10, width=50)
body_entry.grid(row=1, column=1, padx=10, pady=10)

# Botão para selecionar o arquivo de relatório
select_button = tk.Button(root, text="Selecionar Arquivo", command=select_file)
select_button.grid(row=2, column=0, padx=10, pady=10)

# Label para mostrar o arquivo selecionado
file_label = tk.Label(root, text="Nenhum arquivo selecionado")
file_label.grid(row=2, column=1, padx=10, pady=10)

# Botão para enviar o e-mail
send_button = tk.Button(root, text="Enviar", command=send_email)
send_button.grid(row=3, column=1, padx=10, pady=10)

# Iniciar a interface gráfica
root.mainloop()
