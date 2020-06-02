from app import create_app


app = create_app()


# Only for debugging purposes
if __name__ == "__main__":
    host = "localhost"
    port = 5000
    debug = True

    app.run(host=host, port=port, debug=debug)
