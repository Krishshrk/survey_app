import sqlite3

conn = sqlite3.connect('survey.db')
c = conn.cursor()
command="""CREATE TABLE IF NOT EXISTS responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,"""
for i in range(1,11):
    command+=f'''
                plausibility_video{i} INTEGER,
                valence_video{i} INTEGER,
                arousal_video{i} INTEGER,
        '''
command+="""age_group TEXT,
            feedback TEXT)"""
c.execute(command)
conn.commit()
conn.close()

# Save data to SQLite database
conn = sqlite3.connect('survey.db')
c = conn.cursor()
command=""" Drop table responses"""
c.execute(command)

conn.commit()
conn.close()