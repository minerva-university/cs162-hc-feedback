# Database Documentation

## Overview
The application uses SQLite with SQLAlchemy ORM to store and manage HC data. The database replaces the previous JSON-based storage system for improved reliability and performance.

## Database Schema

### Tables

1. `cornerstones`
   - `id`: Integer (Primary Key)
   - `name`: String (Unique, Not Null)
   - One-to-many relationship with `hcs`

2. `hcs`
   - `id`: Integer (Primary Key)
   - `name`: String (Not Null)
   - `footnote`: Text (Not Null)
   - `general_example`: Text (Not Null)
   - `cornerstone_id`: Integer (Foreign Key to cornerstones)
   - One-to-many relationships with `guided_reflections` and `common_pitfalls`

3. `guided_reflections`
   - `id`: Integer (Primary Key)
   - `text`: Text (Not Null)
   - `hc_id`: Integer (Foreign Key to hcs)

4. `common_pitfalls`
   - `id`: Integer (Primary Key)
   - `text`: Text (Not Null)
   - `hc_id`: Integer (Foreign Key to hcs)

## Data Flow

1. Initial data is stored in `app/data/hcs.json`
2. On first run, data is loaded from JSON into SQLite database
3. Subsequent runs use cached database data
4. HC data is cached in memory after first retrieval

## Key Files

- `app/models.py`: Database models definitions
- `app/database.py`: Database initialization and population logic
- `app/data/hcs.json`: Initial data source
- `instance/hc_feedback.db`: SQLite database file (auto-generated)

## Usage

### Initialization
The database automatically initializes when the application starts:
```python
with app.app_context():
    init_db()
    if not Cornerstone.query.first():
        populate_data()
```

### Manual Reset
To manually reset the database:
1. Delete the `instance/hc_feedback.db` file
2. Restart the application

### Querying Examples
```python
# Get all cornerstones
cornerstones = Cornerstone.query.all()

# Get specific HC
hc = HC.query.filter_by(name='thesis').first()

# Get HC's guided reflections
reflections = hc.guided_reflections

# Get HC's common pitfalls
pitfalls = hc.common_pitfalls
```

## Caching
- HC data is cached in memory after first retrieval
- Cache is stored in `hc_data_cache` dictionary in `app/ai/main.py`
- Cache format matches the original JSON structure for compatibility

## Error Handling
- Database errors are logged using the application logger
- Failed database operations return appropriate HTTP error codes
- Database transactions use rollback on failure

## Future Improvements
1. Add database migrations support
2. Implement data versioning
3. Add backup/restore functionality
4. Add admin interface for data management
5. Implement proper database connection pooling
