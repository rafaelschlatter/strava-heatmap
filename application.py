from app import create_app


app = create_app()


if __name__ == "__main__":
    if app.config["ENV"] == "dev":
        host = "localhost"
        port = 5000
        debug = True
    elif app.config["ENV"] == "prod":
        host = "0.0.0.0"
        port = 80
        debug = False

    app.run(host=host, port=port, debug=debug)
