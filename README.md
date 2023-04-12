# UT Data Science 2022

Main project for the course Data Science implementing learned skill from DPV & DM.

Aim is to analyze the full streaming history of Spotify Users and gain insight on their musical taste and listening behavior.

For the analysis the extended spotify streaming history is required, which can be requested and downloaded from [Spotify](https://www.spotify.com/de/account/privacy/).

## Setup

In order to run the analysis locally you need to set up an SQL Database and generate access keys for the spotify API.

1. Enter the credentials in the `.env.example` file and rename it to `.env`.
2. Put retrieved streaming history .json files into the `/data` directory.
3. Install requirements in a new environment with the command `conda env create -f environment.yml`
4. Run the entire `project.ipynb` Notebook
5. Load SQL Database into template Tableau Project `spotilyze.twb`

## Data Schema

![Data Starschema](schema.png)
