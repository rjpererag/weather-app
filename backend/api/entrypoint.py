from .service.api import app


def main() -> None:
    app.run(host='0.0.0.0', port=5001, debug=True)


if __name__ == '__main__':
    main()


# curl -X GET http://localhost:5000/coordinates/paris