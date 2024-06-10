import streamlit as st
import pandas as pd
import base64
from io import BytesIO



# Set page title
st.set_page_config(page_title="Fieldor Report", page_icon=":bar_chart:")

# Initialize session state


# Sidebar navigation
#st.sidebar.title("Navigation")
st.sidebar.markdown('<center><p><h2 style="color: brown; font-family: Helvetica, sans-serif;">BOMBAY INTEGRATED SECURITY (INDIA) LTD</h2></p></center>', unsafe_allow_html=True)
st.sidebar.image("img/logo1.png", caption="")
page = st.sidebar.radio("Go to", [ "Users", "Settings"])
page2 = st.sidebar.radio("Select Report Type", ["Day Report", "Night Report","Daily Visit Summary"])


# Users page
if page == "Users":
    st.title("Fieldor Report")
    # st.write("Manage users, roles, and permissions here.")
    def clear_session_state():
        st.session_state.clear()


    uploaded_file = st.file_uploader("Upload a CSV or EXCEL file", type=["csv", "xlsx"])

    if "df" not in st.session_state:
        st.session_state.df = None

    if st.session_state.df is None:
        if uploaded_file is not None:
            try:
                if uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                    st.session_state.df = pd.read_excel(uploaded_file)
                    #st.write(st.session_state.df)
                else:
                    st.session_state.df = pd.read_csv(uploaded_file, encoding='latin-1')  # Use a suitable encoding

                # Display the loaded DataFrame
                st.write("File uploaded and processed successfully!")
                st.write("Loaded DataFrame:")
                #st.write(st.session_state.df)
                #st.write(st.session_state.df.columns.to_list())
                st.session_state.df.isna().sum()
                # Calculate and assign Earning Differance
                st.write(st.session_state.df.drop(["   Photos", "   Branch", "   Region", "   View Report", "   Site ID"], axis=1, inplace=True))
                # Convert the "VISIT DATE" column to datetime data type
                st.session_state.df["   Visit Date"] = pd.to_datetime(st.session_state.df["   Visit Date"])
                #st.write(st.session_state.df["VISIT DATE"])

                #fetch day,month,year seprate column
                st.session_state.df["VISIT day"]=st.session_state.df["   Visit Date"].apply(lambda x: x.day)
                #st.write(st.session_state.df["VISIT day"])
                st.session_state.df["VISIT month"]=st.session_state.df["   Visit Date"].apply(lambda x: x.month)
                #st.write(st.session_state.df["VISIT month"])
                st.session_state.df["VISIT year"]=st.session_state.df["   Visit Date"].apply(lambda x: x.year)
                #st.write(st.session_state.df["VISIT year"])
                # Convert the "VISIT TIME" column to datetime data type
                st.session_state.df["   Visit Time"] = pd.to_datetime(st.session_state.df["   Visit Time"])
                #st.write(st.session_state.df["VISIT TIME"])
                #fetching houre and min a sepret column
                st.session_state.df["VISIT HOURS"] = st.session_state.df["   Visit Time"].apply(lambda x: x.hour if isinstance(x, pd.Timestamp) else None)
               # st.write(st.session_state.df["VISIT HOURS"])
                #st.session_state.df["VISIT HOURS"] = st.write(st.session_state.df["VISIT TIME"].apply(lambda x: x.hour))
                st.session_state.df["VISIT MIN"] = st.session_state.df["   Visit Time"].apply(lambda x: x.minute if isinstance(x, pd.Timestamp) else None)
                

                

                st.write(st.session_state.df.drop(["   Visit Date","   Visit Time","   Client","   State"], axis=1, inplace=True))
                
                
                if page2=="Day Report":

                    
                    

                    if 'day_data' not in st.session_state:
                        st.session_state.day_data= None
                    if st.session_state.df is not None:
                        if st.session_state.day_data is None:
                            st.session_state.day_data= st.session_state.df[st.session_state.df['VISIT HOURS'].isin([6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])]
                            #st.write(st.session_state.day_data['CONTACT'].unique())  # Display unique values for debugging
                            

                    if 'cross_tab' not in st.session_state:
                        st.session_state.cross_tab = None

                    if st.session_state.day_data is not None:
                           if st.session_state.cross_tab is None:
                                #, st.session_state.day_data['CONTACT']
                                st.session_state.cross_tab = st.session_state.cross_tab = pd.crosstab([st.session_state.day_data['CAD'], st.session_state.day_data['Branch Name'], st.session_state.day_data['   Name']], st.session_state.day_data['VISIT day'], margins=True)


                    if st.button("Download"):
                        
      
                        if st.session_state.cross_tab is not None:
                            #st.write(st.session_state.cross_tab)
                    
                        # Save the Excel file to a BytesIO object
                            excel_io = BytesIO()
                            with pd.ExcelWriter(excel_io, engine='xlsxwriter') as writer:
                                st.session_state.cross_tab.to_excel(writer,  sheet_name='Sheet1')
                                    #index=True,
                            # Encode the BytesIO object to base64
                            excel_base64 = base64.b64encode(excel_io.getvalue()).decode()

                            # Create the download link
                            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{excel_base64}" download="Report.xlsx">Download EXCEL File</a>'
                            st.markdown(href, unsafe_allow_html=True)
                            st.success("Please Click on link for Report Download")
                        else:
                            st.warning("No data to download. Please upload a CSV or Excel file first")
       


                if page2=="Night Report":

                    if 'night_data' not in st.session_state:
                        st.session_state.night_data= None
                    if st.session_state.df is not None:
                        if st.session_state.night_data is None:
                            st.session_state.night_data= st.session_state.df[st.session_state.df['VISIT HOURS'].isin([1,2,3,4,5,21,22,23,00])]
                            #st.write(st.session_state.day_data)
                            

                    if 'cross_tab_night' not in st.session_state:
                        
                        st.session_state.cross_tab_night = None

                    if st.session_state.night_data is not None:
                        if st.session_state.cross_tab_night is None:
                            #, st.session_state.day_data['CONTACT']
                            st.session_state.cross_tab_night = pd.crosstab([st.session_state.night_data['CAD'], st.session_state.night_data['Branch Name'], st.session_state.night_data['   Name']], st.session_state.night_data['VISIT day'], margins=True)

                    if st.button("Download"):
      
                        if st.session_state.cross_tab_night is not None:
                            #st.write(st.session_state.cross_tab_night)
                    
                        # Save the Excel file to a BytesIO object
                            excel_io = BytesIO()
                            with pd.ExcelWriter(excel_io, engine='xlsxwriter') as writer:
                                st.session_state.cross_tab_night.to_excel(writer, index=True, sheet_name='Sheet1')

                            # Encode the BytesIO object to base64
                            excel_base64 = base64.b64encode(excel_io.getvalue()).decode()

                            # Create the download link
                            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{excel_base64}" download="Report.xlsx">Download EXCEL File</a>'
                            st.markdown(href, unsafe_allow_html=True)
                            st.success("Please Click on link for Report Download")
                        else:
                            st.warning("No data to download. Please upload a CSV or Excel file first")


                if page2 == "Daily Visit Summary":
                    if 'df' not in st.session_state:
                        st.session_state.df= None
                    if st.session_state.df is not None:
                        st.session_state.df= st.session_state.df
                                #st.write(st.session_state.day_data)
                                

                    if 'cross_tab_daily' not in st.session_state:
                            
                        st.session_state.cross_tab_daily = None

                    if st.session_state.df is not None:
                        if st.session_state.cross_tab_daily is None:
                                #, st.session_state.day_data['CONTACT']
                            st.session_state.cross_tab_daily = pd.crosstab([st.session_state.df['CAD'], st.session_state.df['Branch Name'], st.session_state.df['   Name']], st.session_state.df['   Report Type'], margins=True)

                    if st.button("Download"):
        
                        if st.session_state.cross_tab_daily is not None:
                            #st.write(st.session_state.cross_tab_daily)
                        
                            # Save the Excel file to a BytesIO object
                            excel_io = BytesIO()
                            with pd.ExcelWriter(excel_io, engine='xlsxwriter') as writer:
                                st.session_state.cross_tab_daily.to_excel(writer, index=True, sheet_name='Sheet1')

                                # Encode the BytesIO object to base64
                            excel_base64 = base64.b64encode(excel_io.getvalue()).decode()

                                # Create the download link
                            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{excel_base64}" download="Report.xlsx">Download EXCEL File</a>'
                            st.markdown(href, unsafe_allow_html=True)
                            st.success("Please Click on link for Report Download")
                        else:
                            st.warning("No data to download. Please upload a CSV or Excel file first")







            except Exception as e:
                st.error("An error occurred: " + str(e))
        # If there is an else block, consider adding it here if needed
    else:
        st.write("DataFrame already loaded:")
        
        if st.button("Download"):
                if page2=="Day Report":
        
                    if st.session_state.cross_tab is not None:
                        #st.write(st.session_state.cross_tab)
                        # Save the Excel file to a BytesIO object
                        excel_io = BytesIO()
                        with pd.ExcelWriter(excel_io, engine='xlsxwriter') as writer:
                            st.session_state.cross_tab.to_excel(writer, index=True, sheet_name='Sheet1')

                        # Encode the BytesIO object to base64
                        excel_base64 = base64.b64encode(excel_io.getvalue()).decode()

                        # Create the download link
                        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{excel_base64}" download="Day_Report.xlsx">Download EXCEL File</a>'
                        st.markdown(href, unsafe_allow_html=True)
                        st.success("Please Click on link for Report Download")
                    else:
                        st.warning("No data to download. Please upload a CSV or Excel file first")

                if page2=="Night Report":
                    if st.session_state.cross_tab_night is not None:
                            #st.write(st.session_state.cross_tab_night)
                    
                        # Save the Excel file to a BytesIO object
                            excel_io = BytesIO()
                            with pd.ExcelWriter(excel_io, engine='xlsxwriter') as writer:
                                st.session_state.cross_tab_night.to_excel(writer, index=True, sheet_name='Sheet1')

                            # Encode the BytesIO object to base64
                            excel_base64 = base64.b64encode(excel_io.getvalue()).decode()

                            # Create the download link
                            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{excel_base64}" download="Night_Report.xlsx">Download EXCEL File</a>'
                            st.markdown(href, unsafe_allow_html=True)
                            st.success("Please Click on link for Report Download")
                    else:
                        st.warning("No data to download. Please upload a CSV or Excel file first")

                if page2=="Daily Visit Summary":
                    if st.session_state.cross_tab_daily is not None:
                            #st.write(st.session_state.cross_tab_daily)
                        
                            # Save the Excel file to a BytesIO object
                            excel_io = BytesIO()
                            with pd.ExcelWriter(excel_io, engine='xlsxwriter') as writer:
                                st.session_state.cross_tab_daily.to_excel(writer, index=True, sheet_name='Sheet1')

                                # Encode the BytesIO object to base64
                            excel_base64 = base64.b64encode(excel_io.getvalue()).decode()

                                # Create the download link
                            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{excel_base64}" download="Daily Visit Summary.xlsx">Download EXCEL File</a>'
                            st.markdown(href, unsafe_allow_html=True)
                            st.success("Please Click on link for Report Download")
                    else:
                        st.warning("No data to download. Please upload a CSV or Excel file first")

                    
    # Add a button to clear the session state
    if st.button("Clear Session State"):
        clear_session_state()

    
       



# Settings page
elif page == "Settings":
    st.title("Admin Dashboard - Settings")
    st.write("Configure application settings here.")
    # Placeholder for application settings components
