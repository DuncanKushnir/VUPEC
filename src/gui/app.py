"""Application entry point."""
import webbrowser

from gui import create_app
import config as cfg


def run(suppress_output=False, override_host=False, override_port=False):
    app = create_app()
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    if suppress_output:
        import logging

        log = logging.getLogger("werkzeug")
        log.disabled = True
        app.logger.disabled = True
    print("Running on http:/127.0.0.1:5000")
    host = override_host if override_host else cfg.DEFAULT_HOST
    port = override_port if override_port else cfg.DEFAULT_PORT
    app.run(host=host, port=port, debug=True)


if __name__ == "__main__":
    run()
