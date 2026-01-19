import threading
from __tests.utils import find_available_port
from instaui import ui

START_PORT, END_PORT = 40000, 40100


class TestServer:
    def __init__(self) -> None:
        self.connected = threading.Event()
        self._server = ui.server(debug=False)
        self.port = find_available_port(START_PORT, END_PORT)

        self._server.add_startup_hook(self.connected.set)

        self.server_thread = threading.Thread(
            target=self._server.run,
            kwargs={"port": self.port, "reload": False, "log_level": "warning"},
            daemon=True,
        )

        self._is_started = False

    @property
    def url(self) -> str:
        return f"http://localhost:{self.port}"

    def start(self) -> None:
        if self._is_started:
            return
        self._is_started = True
        self.server_thread.start()

    def wait_for_connection(self, timeout: float = 10) -> None:
        self.connected.wait(timeout=timeout)

    def stop(self) -> None:
        self._server._runtime.backend.try_close_server()
