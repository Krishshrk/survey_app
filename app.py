from flask import Flask, render_template, request, redirect, url_for
import psycopg2

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
    
    conn = psycopg2.connect(database="verceldb",  
                            user="default", 
                            password="I2xBTqlk9fPD",  
                            host="ep-black-snow-a4zmdro9-pooler.us-east-1.aws.neon.tech") 
    c = conn.cursor()
    command="""CREATE TABLE IF NOT EXISTS response_details (
                     id SERIAL PRIMARY KEY,"""
    for i in range(1,11):
        command+=f'''
                    plausibility_video{i} TEXT,
                    valence_video{i} TEXT,
                    arousal_video{i} TEXT,
            '''
    command+="""age_group TEXT,
                gender TEXT,
                education TEXT,
                occupation TEXT,
                responsiveness TEXT,
                user_experience TEXT,"""
    for i in range(1,7):
        command+=f'AQ_{i} TEXT,'
    command=command[:-1]+")"
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
        conn = psycopg2.connect(database="verceldb",  
                            user="default", 
                            password="I2xBTqlk9fPD",  
                            host="ep-black-snow-a4zmdro9-pooler.us-east-1.aws.neon.tech")
        c = conn.cursor()
        command=""" Insert into response_details ("""
        for i in range(1,11):
            command+=f"""plausibility_video{i}, valence_video{i}, arousal_video{i},"""
        command=command[:-1]+" ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
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
        age_group=request.form['age']
        gender=request.form['gender']
        education=request.form['education']
        occupation=request.form['occupation']
        responsiveness=request.form['responsiveness']
        user_experience=request.form['user_experience']
        aq1 = request.form['plausible_memory']
        aq2=request.form['arousal_accuracy']
        aq3 = request.form['valence_accuracy']
        aq4= request.form['z_score']
        aq5= request.form['arousing']
        aq6=request.form['exposure']

        # Save data to SQLite database
        conn = psycopg2.connect(database="verceldb",  
                            user="default", 
                            password="I2xBTqlk9fPD",  
                            host="ep-black-snow-a4zmdro9-pooler.us-east-1.aws.neon.tech")
        c = conn.cursor()

        c.execute('''UPDATE response_details SET AQ_1=%s, AQ_2=%s,AQ_3=%s,AQ_4=%s,AQ_5=%s,AQ_6=%s WHERE id=(SELECT MAX(id) FROM response_details)''',
                (aq1,aq2,aq3,aq4,aq5,aq6))
        conn.commit()

        c.execute('''UPDATE response_details SET age_group=%s, gender=%s, education=%s, occupation=%s, responsiveness=%s,user_experience=%s WHERE id=(SELECT MAX(id ) FROM response_details) ''',
                    (age_group,gender,education,occupation,responsiveness,user_experience))
        
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
