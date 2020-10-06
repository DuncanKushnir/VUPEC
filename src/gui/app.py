"""Application entry point."""
import webbrowser

from gui import create_app
import config as cfg

def run(suppress_output = False):
    app = create_app()
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    if suppress_output:
        import logging
        log = logging.getLogger('werkzeug')
        log.disabled = True
        app.logger.disabled = True
    webbrowser.open(f"{cfg.DEFAULT_HOST}:{cfg.DEFAULT_PORT}", new=1)
    print('Running on http:/127.0.0.1:5000')
    app.run(host=cfg.DEFAULT_HOST, port=cfg.DEFAULT_PORT, debug=True)



if __name__ == "__main__":
    run()
