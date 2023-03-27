import psycopg2
import sqlalchemy
import os

DB_DRIVER = os.environ['DB_DRIVER']
DB_NAME = os.environ['DB_NAME']
DB_USERNAME = os.environ['DB_USERNAME']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_SERVER = os.environ['DB_SERVER']
DB_PORT = os.environ['DB_PORT']


def get_sql_engine():
    return sqlalchemy.create_engine(f'{DB_DRIVER}://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}')


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS project.songs (
            id SERIAL PRIMARY KEY,
            spotify_id VARCHAR(200) NOT NULL,
            name VARCHAR(400) NOT NULL,
            duration INT,
            emotion VARCHAR(50),
            popularity INT,
            explicitness BOOLEAN,
            key INT,
            mode INT,
            danceability DOUBLE PRECISION,
            energy DOUBLE PRECISION,
            loudness DOUBLE PRECISION,
            speechiness DOUBLE PRECISION,
            acousticness DOUBLE PRECISION,
            instrumentalness DOUBLE PRECISION,
            liveness DOUBLE PRECISION,
            valence DOUBLE PRECISION,
            tempo DOUBLE PRECISION
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS project.artists (
            id SERIAL PRIMARY KEY,
            spotify_id VARCHAR(200) NOT NULL,
            name VARCHAR(200) NOT NULL,
            popularity INT
        )
        """,
        """ 
        CREATE TABLE IF NOT EXISTS project.dates (
                id SERIAL PRIMARY KEY,
                start_time timestamp NOT NULL,
                year INT,
                month INT,
                day INT,
                hour INT,
                weekday VARCHAR(10)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS project.genres (
                id SERIAL PRIMARY KEY,
                name VARCHAR(200) NOT NULL,
                cluster VARCHAR(200)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS project.streams (
                id SERIAL PRIMARY KEY,
                song_id INT NOT NULL,
                date_id INT NOT NULL,
                artist_id INT NOT NULL,
                country VARCHAR(50) NOT NULL,
                duration INT,
                skipped BOOLEAN,
                shuffle BOOLEAN,
                reason_start VARCHAR(50),
                reason_end VARCHAR(50),
                CONSTRAINT song_fkey FOREIGN KEY (song_id)
                    REFERENCES project.songs (id),
                CONSTRAINT date_fkey FOREIGN KEY (date_id)
                    REFERENCES project.dates (id),
                CONSTRAINT artist_fkey FOREIGN KEY (artist_id)
                    REFERENCES project.artists (id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS project.streams_genres (
                stream_id INT NOT NULL,
                genre_id INT NOT NULL,
                CONSTRAINT stream_fkey FOREIGN KEY (stream_id)
                    REFERENCES project.streams (id),
                CONSTRAINT genre_fkey FOREIGN KEY (genre_id)
                    REFERENCES project.genres (id),
                CONSTRAINT streams_genre_pkey PRIMARY KEY (stream_id, genre_id)
        )
        """,
    )

    conn = None

    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(
            host=DB_SERVER, database=DB_NAME, user=DB_USERNAME,
            password=DB_PASSWORD, options="-c search_path=dbo,public")
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
