"""Application entry point."""
import webbrowser

from gui import create_app
import config as cfg

app = create_app()
app.jinja_env.auto_reload = True
app.config["TEMPLATES_AUTO_RELOAD"] = True


def run(suppress_output=False, override_host=False, override_port=False, serve=False):

    if suppress_output:
        import logging

        log = logging.getLogger("werkzeug")
        log.disabled = True
        app.logger.disabled = True

    host = override_host if override_host else cfg.DEFAULT_HOST
    port = override_port if override_port else cfg.DEFAULT_PORT
    if serve:
        print("Running on {}:{}".format(host, port))
        app.run(host=host, port=port, debug=True)
    else:
        app.run()


if __name__ == "__main__":
    import sys

    try:
        SERVE = sys.argv[1]
        if SERVE and SERVE.lower().startswith("s"):
            run(serve=True)
    except:
        run()
