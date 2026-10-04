import socket
import threading
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime


# =========================
# Configuration
# =========================

PORT = 5000
BUFFER_SIZE = 4096

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ChatApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Mesh Wi-Fi Chat")
        self.root.geometry("400x250")
        self.root.resizable(False, False)

        self.server_socket = None
        self.client_socket = None
        self.running = True
        self.chat_window = None

        self.build_connection_window()

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close
        )

    # ==================================================
    # CONNECTION WINDOW
    # ==================================================

    def build_connection_window(self):

        title = ctk.CTkLabel(
            self.root,
            text="Mesh Wi-Fi Chat",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=(25, 5))

        subtitle = ctk.CTkLabel(
            self.root,
            text="Connect to another computer",
            text_color="gray"
        )
        subtitle.pack(pady=(0, 15))

        # IP
        ip_frame = ctk.CTkFrame(
            self.root,
            fg_color="transparent"
        )
        ip_frame.pack(fill="x", padx=30)

        ctk.CTkLabel(
            ip_frame,
            text="IP Address:"
        ).pack(side="left", padx=(0, 10))

        self.ip_entry = ctk.CTkEntry(
            ip_frame,
            width=200,
            placeholder_text="192.168.1.10"
        )
        self.ip_entry.pack(side="left")

        # Buttons
        button_frame = ctk.CTkFrame(
            self.root,
            fg_color="transparent"
        )
        button_frame.pack(pady=25)

        self.server_button = ctk.CTkButton(
            button_frame,
            text="Create Server",
            width=130,
            command=self.start_server
        )
        self.server_button.pack(
            side="left",
            padx=5
        )

        self.connect_button = ctk.CTkButton(
            button_frame,
            text="Connect",
            width=130,
            command=self.connect_to_server
        )
        self.connect_button.pack(
            side="left",
            padx=5
        )

        self.status_label = ctk.CTkLabel(
            self.root,
            text="Status: Not connected",
            text_color="gray"
        )
        self.status_label.pack()

    # ==================================================
    # CHAT WINDOW
    # ==================================================

    def open_chat_window(self):

        # Prevent opening twice
        if self.chat_window is not None:
            try:
                if self.chat_window.winfo_exists():
                    self.chat_window.deiconify()
                    return
            except:
                pass

        self.chat_window = ctk.CTkToplevel(self.root)

        self.chat_window.title("Chat")
        self.chat_window.geometry("600x500")
        self.chat_window.minsize(450, 350)

        self.chat_window.protocol(
            "WM_DELETE_WINDOW",
            self.close
        )

        # Header
        header = ctk.CTkFrame(
            self.chat_window
        )
        header.pack(
            fill="x",
            padx=10,
            pady=10
        )

        title = ctk.CTkLabel(
            header,
            text="Mesh Wi-Fi Chat",
            font=("Arial", 20, "bold")
        )
        title.pack(
            side="left",
            padx=10,
            pady=8
        )

        # Chat box
        self.chat_box = ctk.CTkTextbox(
            self.chat_window,
            font=("Arial", 15),
            state="disabled"
        )

        self.chat_box.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

        # Message frame
        message_frame = ctk.CTkFrame(
            self.chat_window
        )

        message_frame.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )

        self.message_entry = ctk.CTkEntry(
            message_frame,
            placeholder_text="Type your message..."
        )

        self.message_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5,
            pady=10
        )

        self.message_entry.bind(
            "<Return>",
            lambda event: self.send_message()
        )

        self.send_button = ctk.CTkButton(
            message_frame,
            text="SEND",
            width=90,
            command=self.send_message
        )

        self.send_button.pack(
            side="right",
            padx=5
        )

        self.message_entry.focus()

    # ==================================================
    # CHAT DISPLAY
    # ==================================================

    def add_message(self, message):

        # GUI updates should happen on the Tkinter thread
        self.root.after(
            0,
            self._add_message,
            message
        )

    def _add_message(self, message):

        if self.chat_window is None:
            return

        try:

            if not self.chat_window.winfo_exists():
                return

            self.chat_box.configure(
                state="normal"
            )

            self.chat_box.insert(
                "end",
                message + "\n"
            )

            self.chat_box.see("end")

            self.chat_box.configure(
                state="disabled"
            )

        except:
            pass

    # ==================================================
    # SERVER
    # ==================================================

    def start_server(self):

        try:

            self.server_socket = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            self.server_socket.setsockopt(
                socket.SOL_SOCKET,
                socket.SO_REUSEADDR,
                1
            )

            self.server_socket.bind(
                ("0.0.0.0", PORT)
            )

            self.server_socket.listen(1)

            self.server_button.configure(
                state="disabled"
            )

            self.connect_button.configure(
                state="disabled"
            )

            self.status_label.configure(
                text=f"Waiting for connection on port {PORT}..."
            )

            threading.Thread(
                target=self.accept_connection,
                daemon=True
            ).start()

        except Exception as e:

            messagebox.showerror(
                "Server Error",
                str(e)
            )

            if self.server_socket:
                try:
                    self.server_socket.close()
                except:
                    pass

            self.server_socket = None

    def accept_connection(self):

        try:

            client, address = (
                self.server_socket.accept()
            )

            self.client_socket = client

            self.root.after(
                0,
                self.connection_success,
                address[0]
            )

            threading.Thread(
                target=self.receive_messages,
                daemon=True
            ).start()

        except Exception as e:

            if self.running:

                self.root.after(
                    0,
                    lambda: self.status_label.configure(
                        text="Status: Disconnected"
                    )
                )

    # ==================================================
    # CLIENT CONNECTION
    # ==================================================

    def connect_to_server(self):

        ip = self.ip_entry.get().strip()

        if not ip:

            messagebox.showwarning(
                "IP Address",
                "Enter the remote computer IP address."
            )

            return

        try:

            self.client_socket = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            self.client_socket.settimeout(5)

            self.client_socket.connect(
                (ip, PORT)
            )

            self.client_socket.settimeout(None)

            self.connection_success(ip)

            threading.Thread(
                target=self.receive_messages,
                daemon=True
            ).start()

        except Exception as e:

            if self.client_socket:

                try:
                    self.client_socket.close()
                except:
                    pass

            self.client_socket = None

            messagebox.showerror(
                "Connection Error",
                str(e)
            )

    # ==================================================
    # CONNECTION SUCCESS
    # ==================================================

    def connection_success(self, ip):

        self.status_label.configure(
            text=f"Connected to {ip}"
        )

        self.open_chat_window()

        self.add_message(
            f"[SYSTEM] Connected to {ip}"
        )

        # Hide connection window
        self.root.withdraw()

    # ==================================================
    # SEND MESSAGE
    # ==================================================

    def send_message(self):

        if not self.client_socket:

            messagebox.showwarning(
                "Not Connected",
                "You are not connected."
            )

            return

        message = self.message_entry.get().strip()

        if not message:
            return

        timestamp = datetime.now().strftime(
            "%H:%M"
        )

        try:

            self.client_socket.sendall(
                message.encode("utf-8")
            )

            self.add_message(
                f"[{timestamp}] You: {message}"
            )

            self.message_entry.delete(
                0,
                "end"
            )

        except Exception as e:

            self.add_message(
                f"[ERROR] {e}"
            )

    # ==================================================
    # RECEIVE MESSAGE
    # ==================================================

    def receive_messages(self):

        while self.running:

            try:

                data = self.client_socket.recv(
                    BUFFER_SIZE
                )

                if not data:
                    break

                message = data.decode(
                    "utf-8",
                    errors="replace"
                )

                timestamp = datetime.now().strftime(
                    "%H:%M"
                )

                self.add_message(
                    f"[{timestamp}] Other: {message}"
                )

            except:

                break

        if self.running:

            self.root.after(
                0,
                self.connection_lost
            )

    # ==================================================
    # CONNECTION LOST
    # ==================================================

    def connection_lost(self):

        self.status_label.configure(
            text="Status: Disconnected"
        )

        self.add_message(
            "[SYSTEM] Connection closed."
        )

    # ==================================================
    # CLOSE APPLICATION
    # ==================================================

    def close(self):

        self.running = False

        try:

            if self.client_socket:
                self.client_socket.shutdown(
                    socket.SHUT_RDWR
                )

        except:
            pass

        try:

            if self.client_socket:
                self.client_socket.close()

        except:
            pass

        try:

            if self.server_socket:
                self.server_socket.close()

        except:
            pass

        try:

            if self.chat_window:
                self.chat_window.destroy()

        except:
            pass

        self.root.destroy()


# ==================================================
# START APPLICATION
# ==================================================

if __name__ == "__main__":

    root = ctk.CTk()

    app = ChatApp(root)

    root.mainloop()
