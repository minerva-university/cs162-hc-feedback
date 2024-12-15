from app import create_app
import click

app = create_app()

@app.cli.command("init-db")
def init_db_command():
    """Clear existing data and create new tables."""
    from app.utils.database import init_db, populate_data
    with app.app_context():
        init_db()
        populate_data()
    click.echo("Initialized the database.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
