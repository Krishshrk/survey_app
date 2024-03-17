from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

video_files = ["https://drive.google.com/file/d/1rl7TLaAE9JX0Yu8VeZeQQq2HXwK846jv/preview",
               "https://drive.google.com/file/d/19zN6DYfYvvPX4RFeGPXHfBQjsEH4fex5/preview",
               "https://drive.google.com/file/d/1zXW1r43dG6ren9Sbywgr0ss8IYq9ovlu/preview",
               "https://drive.google.com/file/d/1zO4dS2zYQS_GALvvSc6eR3SOZIWmqJfN/preview",
               "https://drive.google.com/file/d/1XmRUeTYGTGPP07_eqvE40UuLhWmpaVrw/preview",
               "https://drive.google.com/file/d/1583WAPgylFI1T-WIgNnoo4Ns3IBAvMDA/preview",
               "https://drive.google.com/file/d/1z4Z2GrHX3O1tDGNFJ5tVsx2P1axRcWse/preview",
               "https://drive.google.com/file/d/1ExkiezJRUPE7jQSedXLCO9dGEG3Faa9c/preview",
               "https://drive.google.com/file/d/1_jFLoaAFoBHO8wfAGmjFJPkI1dLeaf10/preview",
               "https://drive.google.com/file/d/1X-iqG2NIOQZZdmMfUKsE5JRVW3zWPg5F/preview" ]


# SQLite database initialization
def init_db():
    conn = sqlite3.connect('survey.db')
    c = conn.cursor()
    command="""CREATE TABLE IF NOT EXISTS responses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,"""
    for i in range(1,11):
        command+=f'''
                    plausibility_video{i} TEXT,
                    valence_video{i} TEXT,
                    arousal_video{i} TEXT,
            '''
    command+="""age_group TEXT,
                app_feedback INTEGER,
                feedback_comments TEXT )"""
    c.execute(command)
    conn.commit()
    conn.close()

# Initialize the database
init_db()

# Route to display the survey page
@app.route('/survey')
def survey():
    return render_template('survey.html',video_files=video_files)

# Route to handle form submission from the survey page
@app.route('/submit_survey', methods=['POST'])
def submit_survey():
    # Collect data from the form
    if request.method=='POST':
        plausibility_values = [request.form[f'plausibilityScale{i}'] for i in range(1, 11)]
        valence_values = [request.form[f'valenceScale{i}'] for i in range(1, 11)]
        arousal_values = [request.form[f'arousalScale{i}'] for i in range(1, 11)]
        # Save data to SQLite database
        conn = sqlite3.connect('survey.db')
        c = conn.cursor()
        command=""" Insert into responses ("""
        for i in range(1,11):
            command+=f"""plausibility_video{i}, valence_video{i}, arousal_video{i},"""
        command=command[:-1]+" ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        values=list()
        for i in range(10):
            values.append(plausibility_values[i])
            values.append(valence_values[i])
            values.append(arousal_values[i])
        c.execute(command,tuple(values))
        conn.commit()
        conn.close()

        # Redirect to the additional information page
        return redirect(url_for('additional_info'))

# Route to display the additional information page
@app.route('/additional_info')
def additional_info():
    return render_template('information.html')

# Route to handle form submission from the additional information page
@app.route('/submit_info', methods=['POST'])
def submit_info():
    if request.method=="POST":
        # Collect data from the form
        age_group = request.form['ageGroup']
        app_feedback=request.form['appFeedback']
        feedback = request.form['feedback']

        # Save data to SQLite database
        conn = sqlite3.connect('survey.db')
        c = conn.cursor()
        c.execute('''UPDATE responses SET age_group=?, app_feedback=?, feedback_comments=? WHERE id=(SELECT MAX(id) FROM responses)''',
                (age_group,app_feedback, feedback))
        conn.commit()
        conn.close()

        # Redirect to a thank you page or any other page
        return redirect(url_for('thank_you'))

# Route to display a thank you page
@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True)
