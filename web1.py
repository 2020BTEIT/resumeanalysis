import os
import streamlit as st
import pandas as pd
import base64,random
import time,datetime


from urllib.parse import urlparse
from PIL import Image
import requests  
 
  
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io,random
from streamlit_tags import st_tags
from PIL import Image
import pymysql
from Courses import ds_course,web_course,android_course,ios_course,uiux_course,resume_videos,interview_videos
import pafy
import plotly.express as px
timestr=time.strftime("%Y%m%d-%H%M%S")
qr=qrcode.QRCode(version=1,
   error_correction=qrcode.constants.ERROR_CORRECT_L,
   box_size=10,
   border=14)
from PIL import Image
import cv2
def load_image(img):
 im=Image.open(img)
 return im
def fetch_yt_video(link):
    video = pafy.new(link)
    return video.title

def get_table_download_link(df,filename,text):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  
    
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href

def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)
            print(page)
        text = fake_file_handle.getvalue()

 
    converter.close()
    fake_file_handle.close()
    return text
def common_elements(arr1, arr2):
   
    set1 = set(arr1)
    set2 = set(arr2)

  
    common_set = set1.intersection(set2)

 
    return len(common_set)

def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
     
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def course_recommender(course_list):
    st.subheader("**Courses & Certificates🎓 Recommendations**")
    c = 0
    rec_course = []
    no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 4)
    random.shuffle(course_list)
    for c_name, c_link in course_list:
        c += 1
        st.markdown(f"({c}) [{c_name}]({c_link})")
        rec_course.append(c_name)
        if c == no_of_reco:
            break
    return rec_course
def resume_recommender(course1_list):
    st.subheader("**Resume Bulding Videos**")
    c = 0
    rec1_course = []
    st.markdown('''<h4 style='text-align: left; color: #800080;'> Choose number of 📃️ resume bulding videos: </h4>''',unsafe_allow_html=True)
    no_of_reco1 = st.slider(' ', 1, 4, 2)
    random.shuffle(course1_list)
    for c_link in course1_list:
        c += 1
        st.markdown(f"({c}) ({c_link})")
         
        if c == no_of_reco1:
            break
    return rec1_course
 
def interview_recommender(course2_list):
    st.subheader("**Interview Preparation Videos**")
    c = 0
    rec2_course = []
    st.markdown('''<h4 style='text-align: left; color: #800080;'>  Choose number of 👔️Interview Preparation ✌️ Videos: </h4>''',unsafe_allow_html=True)
    no_of_reco2 = st.slider('🏆️', 1, 4, 2)
    
    for c_link in course2_list:
        c += 1
        st.markdown(f"({c}) ({c_link})")
         
        if c == no_of_reco2:
            break
    return rec2_course
connection = pymysql.connect(host='localhost',user='root',password='',db='sra')
cursor = connection.cursor()

def insert_data(name,email,res_score,timestamp,no_of_pages,reco_field,cand_level,skills,recommended_skills,courses):
    DB_table_name = 'user1'
    insert_sql = "insert into " + DB_table_name + """
    values (0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    rec_values = (name, email, str(res_score), timestamp,str(no_of_pages), reco_field, cand_level, skills,recommended_skills,courses)
    cursor.execute(insert_sql, rec_values)
    connection.commit()

st.set_page_config(
   page_title=" Resume Analyzer",
   page_icon='./Logo/SRA_Logo.ico',
)
def run():
    st.title(" Resume Analyser")
    st.sidebar.markdown("#Select user type")
    activities = ["Normal User", "Admin","Generate QR","Skillsets"]
    choice = st.sidebar.selectbox("Select among the following:", activities)
   
    img = Image.open('./Logo/SRA_Logo.jpg')
    img = img.resize((250,250))
    st.image(img)
 
    db_sql = """CREATE DATABASE IF NOT EXISTS SRA;"""
    cursor.execute(db_sql)

    
    DB_table_name = 'user1'
    table_sql = "CREATE TABLE IF NOT EXISTS " + DB_table_name + """
                    (ID INT NOT NULL AUTO_INCREMENT,
                     Name varchar(100) NOT NULL,
                     Email_ID VARCHAR(50) NOT NULL,
                     resume_score VARCHAR(8) NOT NULL,
                     Timestamp VARCHAR(50) NOT NULL,
                     Page_no VARCHAR(5) NOT NULL,
                     Predicted_Field VARCHAR(25) NOT NULL,
                     User_level VARCHAR(30) NOT NULL,
                     Actual_skills VARCHAR(300) NOT NULL,
                     Recommended_skills VARCHAR(300) NOT NULL,
                     Recommended_courses VARCHAR(600) NOT NULL,
                     PRIMARY KEY (ID));
                    """
    cursor.execute(table_sql)
    
     
     # Python program demonstrating
# Multiple selection in Listbox widget


    

# Define options for the dropdown
     

    if choice == "Generate QR":
      st.subheader("Home")
       
      with st.form(key='myqr_form'):
       raw_text=st.text_area("Text Here")
       submit_button=st.form_submit_button("Generate")
      if submit_button:
       col1,col2=st.columns(2)
       with col1:
        qr.add_data(raw_text)
        qr.make(fit=True)
        img=qr.make_image(fill_color='black',back_color='white')
        img_filename='QR.png'
        path_for_images=os.path.join('image_folder',img_filename)
        img.save(path_for_images)
        final_img=load_image(path_for_images)
        st.image(final_img)
         
        
 

       with col2:
        st.info("Original Text")
        st.write(raw_text)
        

       
         
         
              
    if choice == 'Normal User':
        
        pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
        if pdf_file is not None:
             
            save_image_path = './Uploaded_Resumes/'+pdf_file.name
            with open(save_image_path, "wb") as f:
                f.write(pdf_file.getbuffer())
            show_pdf(save_image_path)
            resume_data = ResumeParser(save_image_path).get_extracted_data()
            if resume_data:
                 
                resume_text = pdf_reader(save_image_path)

                st.header("**Resume Analysis**")
                st.success("Hello, "+ resume_data['name'])
                st.subheader("**Your Basic info**")
                try:
                    st.text('Name: '+resume_data['name'])
                    st.text('Email: ' + resume_data['email'])
                    st.text('Contact: '+'+' + resume_data['mobile_number'])
                    st.text('Resume pages: '+str(resume_data['no_of_pages']))
                except:
                    pass
                
                st.subheader("**Expertise Recommendation💡**")
                 
                keywords = st_tags(label='### Skills that you have',
                text='See our expertise recommendation',
                    value=resume_data['skills'],key = '1')

                
                ds_keyword = ['tensorflow','keras','pytorch','machine learning','deep Learning','flask','streamlit']
                web_keyword = ['react', 'django', 'node jS', 'react js', 'php', 'laravel', 'magento', 'wordpress',
                               'javascript', 'angular js', 'c#', 'flask']
                android_keyword = ['android','android development','flutter','kotlin','xml','kivy']
                ios_keyword = ['ios','ios development','swift','cocoa','cocoa touch','xcode']
                uiux_keyword = ['ux','adobe xd','figma','zeplin','balsamiq','ui','prototyping','wireframes','storyframes','adobe photoshop','photoshop','editing','adobe illustrator','illustrator','adobe after effects','after effects','adobe premier pro','premier pro','adobe indesign','indesign','wireframe','solid','grasp','user research','user experience']
                
                recommended_skills = []
                reco_field = ''
                rec_course = ''
                 
                for i in resume_data['skills']:
                    
                    if i.lower() in ds_keyword:
                        print(i.lower())
                        reco_field = 'Data Science'
                        st.success("** Our analysis says you are looking for Data Science Jobs.**")
                        recommended_skills = ['Data Visualization','Predictive Analysis','Statistical Modeling','Data Mining','Clustering & Classification','Data Analytics','Quantitative Analysis','Web Scraping','ML Algorithms','Keras','Pytorch','Probability','Scikit-learn','Tensorflow',"Flask",'Streamlit']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                        text='Recommended skills generated from System',value=recommended_skills,key = '2')
                        st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                        rec_course = course_recommender(ds_course)
                        break

                     
                    elif i.lower() in web_keyword:
                        print(i.lower())
                        reco_field = 'Web Development'
                        st.success("** Our analysis says you are looking for Web Development Jobs **")
                        recommended_skills = ['React','Django','Node JS','React JS','php','laravel','Magento','wordpress','Javascript','Angular JS','c#','Flask','SDK']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                        text='Recommended skills generated from System',value=recommended_skills,key = '3')
                        st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                        rec_course = course_recommender(web_course)
                        break

                    
                    elif i.lower() in android_keyword:
                        print(i.lower())
                        reco_field = 'Android Development'
                        st.success("** Our analysis says you are looking for Android App Development Jobs **")
                        recommended_skills = ['Android','Android development','Flutter','Kotlin','XML','Java','Kivy','GIT','SDK','SQLite']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                        text='Recommended skills generated from System',value=recommended_skills,key = '4')
                        st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                        rec_course = course_recommender(android_course)
                        break

                     
                    elif i.lower() in ios_keyword:
                        print(i.lower())
                        reco_field = 'IOS Development'
                        st.success("** Our analysis says you are looking for IOS App Development Jobs **")
                        recommended_skills = ['IOS','IOS Development','Swift','Cocoa','Cocoa Touch','Xcode','Objective-C','SQLite','Plist','StoreKit',"UI-Kit",'AV Foundation','Auto-Layout']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                        text='Recommended skills generated from System',value=recommended_skills,key = '5')
                        st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                        rec_course = course_recommender(ios_course)
                        break

                     
                    elif i.lower() in uiux_keyword:
                        print(i.lower())
                        reco_field = 'UI-UX Development'
                        st.success("** Our analysis says you are looking for UI-UX Development Jobs **")
                        recommended_skills = ['UI','User Experience','Adobe XD','Figma','Zeplin','Balsamiq','Prototyping','Wireframes','Storyframes','Adobe Photoshop','Editing','Illustrator','After Effects','Premier Pro','Indesign','Wireframe','Solid','Grasp','User Research']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                        text='Recommended skills generated from System',value=recommended_skills,key = '6')
                        st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                        rec_course = course_recommender(uiux_course)
                        break

                
                ts = time.time()
                cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                timestamp = str(cur_date+'_'+cur_time)
 
                
                resume_score = 0
                options = ['Java', 'CPP', 'Algorithm', 'C','Engineering','Programming','Computer science','System','IOS','IOS Development','Swift','Cocoa','Cocoa Touch','Xcode','Objective-C','SQLite','tensorflow','keras','pytorch','machine learning','deep Learning','flask','streamlit','react', 'django', 'node jS', 'react js', 'php', 'laravel', 'magento', 'wordpress',
                               'javascript', 'angular js', 'c#', 'flask','android','android development','flutter','kotlin','xml','kivy','cocoa','cocoa touch','xcode','Docker','Sql','Coding','Github','Pycharm','Git','Technical','Database','AWS','Algorithms','PHP','XAMPP','PhpMyAdmin','Linux','Ubantu','NodeJs']
                 
# Initialize the options array
 
                while True:
    # Display the current options
                 

    # Prompt the user to enter an element and add it to the options array
                 element = st.text_input("Enter an element to add to the list (or press Enter to stop):",key=f"element_{len(options)}")
                 if element == "":
                    break
                 options.append(element)

# Sort the options array
                sorted_array = sorted(options)

# Create a multiselect dropdown with the options defined above
                selected_options = st.multiselect('Select options:', sorted_array, default=sorted_array)

# Display the selected options
                st.write("Selected options:", selected_options)
        
                 
                num_common_elements = common_elements(selected_options,resume_data['skills'])
                txt="💯️Percentage requirements fulfilled by candidate🏆️: "    
                htmlstr1=f"""<p style='background-color:#E6E6FA;
                                           color: 	#FF1493;
                                           font-size:30px;
                                           border-radius:3px;
                                           line-height:60px;
                                           padding-left:17px;
                                           opacity:0.6'>
                                           {txt}</style>
                                           <br></p>""" 
                st.markdown(htmlstr1,unsafe_allow_html=True) 
                if(len(selected_options)==0):
                 sum=0;
                else:
                 sum="{:.2f}".format((num_common_elements/len(selected_options))*100)
                sum1= (num_common_elements/len(selected_options))*100
                sum2=round(sum1)
                background_color = '	#E6E6FA'  # Green color
                font_size='30px'
# Set the success message and background color
                success_message ='🤩️'+str(sum)+'🔥️'
                styled_message = f'<span style="background-color:{background_color};  font-size:{font_size}; padding: 0.5rem;">{success_message}</span>'
                 
# Display the styled success message
                st.markdown(styled_message, unsafe_allow_html=True)
                st.subheader("**Resume Tips & Ideas💡**")
                resume_score=resume_score+int(sum2);
                if 'POSITION OF RESPONSIBILITY'or 'EXPERIENCE' or 'Experience' or 'Position of Responsibility'  in resume_text:
                    resume_score = resume_score+10
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>[+] Good! You have added Position of responsibility</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add your position of responsibility, it will give your career intension to the Recruiters.</h4>''',unsafe_allow_html=True)

                if 'EDUCATIONAL DETAILS' or 'Educational details' or 'EDUCATION DETAILS' or 'Education details' in resume_text:
                    resume_score = resume_score + 5
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>[+] Good! You have added Educational details.✍/h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add Education details✍. It will represent your educational qualification.</h4>''',unsafe_allow_html=True)

                if 'Hobbies' or 'Interests' or 'HOBBIES' or 'INTERESTS' in resume_text:
                    resume_score = resume_score + 5
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>[+] Good! You have added your Hobbies.⚽</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add Hobbies⚽. It will show your persnality to the Recruiters and give the assurance that you are fit for this role or not.</h4>''',unsafe_allow_html=True)

                if 'Achievements'or 'ACHIEVEMENTS' in resume_text:
                    resume_score = resume_score + 10
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>[+] Good! You have added your Achievements🏅 </h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add Achievements🏅. It will show your what you have done during academics.</h4>''',unsafe_allow_html=True)

                if 'Projects' or 'PROJECTS' in resume_text:
                    resume_score = resume_score + 20
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>[+] Good! You have added your Projects👨‍💻 </h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add Projects👨‍💻. It will show that you have done related the required position or not.</h4>''',unsafe_allow_html=True)

                st.subheader("**Resume Score📝**")
                st.markdown(
                    """
                    <style>
                        .stProgress > div > div > div > div {
                            background-color: #d73b5c;
                        }
                    </style>""",
                    unsafe_allow_html=True,
                )
                my_bar = st.progress(0)
                score = 0
                for percent_complete in range(resume_score):
                    score +=1
                    time.sleep(0.1)
                    my_bar.progress(percent_complete + 1)
                st.success('** Your Resume Writing Score: ' + str(score)+'**')
                st.warning("** Note: This score is calculated based on the content that you have added in your Resume. **")
               #st.balloons
                cand_level = ''
                if resume_score  < 50:
                    cand_level = "Fresher"
                    st.markdown( '''<h4 style='text-align: left; color: #ff0000;'>😃️You are looking fresher.👍️</h4>''',unsafe_allow_html=True)
                elif resume_score <=90:
                    cand_level = "Intermediate"
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>🔥️You are at intermediate level!🔥️</h4>''',unsafe_allow_html=True)
                else:
                    cand_level = "Experienced"
                    st.markdown('''<h4 style='text-align: left; color: #fba171;'>🤑️You are at experienced level!🤑️''',unsafe_allow_html=True)
                  
                insert_data(resume_data['name'], resume_data['email'], str(resume_score), timestamp,
                              str(resume_data['no_of_pages']), reco_field, cand_level, str(resume_data['skills']),
                              str(recommended_skills), str(rec_course))


                rec1_course = resume_recommender(resume_videos)
                rec2_course=interview_recommender(interview_videos)

                connection.commit()
            else:
                st.error('Something went wrong..')
    elif choice=='Admin':
        ## Admin Side
        st.success('Welcome to Admin Login')
        
        ad_user = st.text_input("Username")
        ad_password = st.text_input("Password", type='password')
        if st.button('Login'):
             

            if ad_user == 'harshad' and ad_password == 'harshad':
                st.success("Welcome Harshad")
                # Display Data
               
        
                 
                cursor.execute('''SELECT*FROM user1''')
                data = cursor.fetchall()
                st.header("**User's👨‍💻 Data**")
                df = pd.DataFrame(data, columns=['ID', 'Name', 'Email', 'Resume Score', 'Timestamp', 'Total Page',
                                                 'Predicted Field', 'User Level', 'Actual Skills', 'Recommended Skills',
                                                 'Recommended Course'])
                st.dataframe(df)
                st.markdown(get_table_download_link(df,'User1.csv','Download Report'), unsafe_allow_html=True)
                options=[];
                
                query = 'select * from user1;'
                plot_data = pd.read_sql(query, connection)

                
                labels = plot_data.Predicted_Field.unique()
                print(labels)
                values = plot_data.Predicted_Field.value_counts()
                print(values)
                st.subheader("📈 **Pie-Chart for Predicted Field Recommendations**")
                fig = px.pie(df, values=values, names=labels, title='Predicted Field according to the Skills')
                st.plotly_chart(fig)
            
                
                 
            else:
                st.error("Wrong ID & Password Provided")
       
run()
