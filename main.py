from website1 import create_app

app = create_app()

# automatically reruns server when python changes are made
if __name__ == '__main__':
    app.run(debug=True)