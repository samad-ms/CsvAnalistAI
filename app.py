import streamlit as st
from utils import *

#----------------------------------------------------------------------------------------
def home_tab():
    """ Home Tab """
    st.title("🔍 Welcome to CsvAnalistAI !")
    st.write("""
    
        #### Links:
        - [GitHub Repository](https://github.com/samad-ms/)
        - [LinkedIn Profile](https://www.linkedin.com/in/abdul-samad-86b158243/)
    """)

    st.write("### Welcome Contributions!")
    st.write("We welcome contributions from the community to improve JobInsights. Whether it's adding new features, fixing bugs, or enhancing documentation, every contribution matters!")
#----------------------------------------------------------------------------------------
def chat_with_csv_tab():
    """chat_with_csv Tab"""

    st.title("chat with csv in natural language.")
    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("💡 Tips", expanded=False):
        st.write(
        """
           * workflow guidance !
           * it comes soon..............
        """
        )

    st.write("Please upload your CSV file below.")
    data = st.file_uploader("Upload a CSV" , type="csv")
    user_query = st.text_area("Ask your question..")

    if st.button("Submit Query", type="primary"):
        response = csv_agent(data,user_query)
        st.write(response)
#----------------------------------------------------------------------------------------
def chat_and_visualize_with_csv_tab():
    """chat_and_visualize_with_csv"""

    st.title("Query your Data to Generate Graph")
    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("💡 Tips", expanded=False):
        st.write(
        """
           * workflow guidance !
           * it comes soon..............
        """
        )

    st.subheader("Query your Data to Generate Graph")
    file_uploader = st.file_uploader("Upload your CSV", type="csv")

    if file_uploader is not None:
        path_to_save = "filename1.csv"
        with open(path_to_save, "wb") as f:
            f.write(file_uploader.getvalue())
        if st.button("Are you confused , about what to query for generate, click here to get suggesions",type='secondary'):
            goals=get_suggestions()
            for i,goal in enumerate(goals):
                st.markdown(f"{i+1}. {goal.question}  \n{goal.visualization}.  \n{goal.rationale}")
        
        text_area = st.text_area(label="**Enter Your Query**",placeholder="Ex: What is the relationship between credit_score and account_balance?" ,height=200)
        
        if st.button("Generate Graph",type='primary'):
            if len(text_area) > 0:
                st.info("Your Query: " + text_area)
                
                imgs=auto_visualazier(text_area)
                if imgs==None:
                    st.write("encounter some error")
                else:
                    img1,img2=imgs
                    col1, col2 = st.columns(2)
                    with col1:
                        st.image(img1)
                    with col2:
                        st.image(img2)


#----------------------------------------------------------------------------------------
def Auto_summarizer_tab():
    """ Auto_summarizer_tab """
    st.title("🔍 Summarization of your Data Automatically with visulizations!")
    with st.expander("💡 Tips", expanded=False):
        st.write("""
        many more exciting features to come!
        
        Share your thoughts and ideas to integrate, and also, welcome to contributions and debugging!
        """)


    file_uploader = st.file_uploader("Upload your CSV", type="csv")
    button=st.button('summarize')
    if (file_uploader is not None) and button:
        path_to_save = "filename.csv"
        with open(path_to_save, "wb") as f:
            f.write(file_uploader.getvalue())
        
        goals_and_imgs,summary=auto_summarizer()
        for goal_and_img in goals_and_imgs:
            st.write(goal_and_img[0])
            st.write(goal_and_img[1])
            st.write(goal_and_img[2])
            st.image(goal_and_img[3])
        st.write(decode_json_to_natural_language(summary))
#----------------------------------------------------------------------------------------
if __name__ == "__main__":
    st.set_page_config(page_title="CsvAnalistAI - A Complete CSV Analyst",page_icon='🔍')
    feature_tabs = st.sidebar.radio(
        "Features",
        [":rainbow[**Home**]", "**Chat with CSV**","**Auto Summarizer**", "**Chat and Visualize The CSV**","**Additional features**"],
        captions=["", "Chat with Csv in natural language and get the response in tables and natural language.","Summarize the CSV and get visualization and insight automatically", "suggestion to how to visualize and impact then , get Visualization and insights.",""]
    )

    if feature_tabs == ":rainbow[**Home**]":
        home_tab()
    elif feature_tabs == "**Chat with CSV**":
        chat_with_csv_tab()
    elif feature_tabs == "**Auto Summarizer**":
        Auto_summarizer_tab()
    elif feature_tabs == "**Chat and Visualize The CSV**":
        chat_and_visualize_with_csv_tab()
    elif feature_tabs == "**Additional features**":
        pass

    st.sidebar.markdown("""
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: transparent;
        padding: 10px;
        text-align: left;
        font-size: 15px;
    }
    .footer a {
        text-decoration: none;
        margin-left: 10px;
    }
    </style>
    <div class="footer">
    <a href="https://github.com/samad-ms/JobInsights/issues">Feedback</a>
    <a href="https://github.com/samad-ms/JobInsights">Contributions</a>
    </div>
    """, unsafe_allow_html=True)
#----------------------------------------------------------------------------------------
