"""Application entry point."""
import webbrowser

from gui import create_app
import gui.config as cfg

app = create_app()

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(host=cfg.DEFAULT_HOST, port=cfg.DEFAULT_PORT, debug=True)
    webbrowser.open(f"{cfg.DEFAULT_HOST}:{cfg.DEFAULT_PORT}", new=2)
