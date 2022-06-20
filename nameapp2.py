import pandas as pd
import cutlet
katsu = cutlet.Cutlet()
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

#Read in the CSV file of two-character surnames
df_sur = pd.read_csv('sur_csv.csv')

# Another dataframe of the kanji occuring in these names, with their meanings taken from the list of Jouyou Kanji
df_kanjiref = pd.read_csv('kanjiref_csv.csv')
df_choices = df_kanjiref[['Character','Meaning']]

# app title
st.title("Two-Character Japanese Family Names")

st.subheader('Choose any two rows from the table below using the checkboxes. If you combine the two characters, do you get a family name that is among the top 1000 family names in Japan? Hit the Submit button and find out!')


#char1 = st.sidebar.selectbox(
     #"Make a selection for the name's first character",
     #df_kanjiref['Choices'].unique())

#char2 = st.sidebar.selectbox(
     #"Make a selection for the name's second character",
    # df_kanjiref['Choices'].unique())

#table = st.sidebar.dataframe(df_kan)
#name = char1[2] + char2[2]
# creating a single-element container
#placeholder = st.empty()
# AgGrid(df_kanjiref['Character','Meaning'])

gb = GridOptionsBuilder.from_dataframe(df_choices)
gb.configure_column('Character', headerCheckboxSelection = True) #option to deselect all
#gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
gb.configure_side_bar() #Add a sidebar
gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
gridOptions = gb.build()

grid_response = AgGrid(
    df_choices,
    gridOptions=gridOptions,
    data_return_mode='AS_INPUT', 
    update_mode='MODEL_CHANGED', 
    fit_columns_on_grid_load=True,
    theme='blue', #Add theme color to the table
    enable_enterprise_modules=True,
    height=500, 
    width='50%',
    reload_data=True
)

df_choices = grid_response['data']
selected = grid_response['selected_rows'] 
df = pd.DataFrame(selected) #Pass the selected rows to a new dataframe df

if (len(df.index) < 1) or (len(df.index) > 2):
    st.write('**PLEASE SELECT EXACTLY 2 ITEMS FOR THE SUBMIT BUTTON TO APPEAR**')
elif len(df.index) == 1:
    st.write('**PLEASE SELECT ANOTHER ITEM**')
    #st.dataframe(df)
    AgGrid(df, height=100, width=400)
else:
    st.write('**YOU HAVE SELECTED:**')
    #st.dataframe(df, 200, 100)
    AgGrid(df, height=100, width=400)
    name = df.iat[0,0] + df.iat[1,0]
    name_rev = df.iat[1,0] + df.iat[0,0]
    roma_name = katsu.romaji(name)
    roma_name_rev = katsu.romaji(name_rev)
    if st.button('Submit'):
       if name in df_sur['Surname2'].values:
           st.write('**CORRECT!**') 
           st.subheader(name + ' ' + roma_name)
       elif name_rev in df_sur['Surname2'].values:
           st.write('**CORRECT!**') 
           st.subheader(name_rev + ' ' + roma_name_rev)    
       else:
           st.write('**TRY AGAIN!**')
           '''
           (Sometimes you may be asked to try again even though you chose two kanji that do make up a
           legitimate family name -- it may just not be among the top 1000 family names.)
           '''

#st.write('**YOU HAVE SELECTED:**')
#st.subheader(df.loc[0])
#st.write(' **AND** ')
#st.subheader(df.loc[1])



'''
The selection table was created as follows:
1. Take all the two-character family names from [The 1,000 most common Japanese family names](https://jref.com/articles/common-japanese-surnames.213/)
2. Take all the characters in this set of names
3. From this set of characters, take all the characters which are also in the [List of jōyō kanji](https://en.wikipedia.org/wiki/List_of_j%C5%8Dy%C5%8D_kanji)
4. Source their meanings from the same [List of jōyō kanji](https://en.wikipedia.org/wiki/List_of_j%C5%8Dy%C5%8D_kanji)
NOTE: The [List of jōyō kanji](https://en.wikipedia.org/wiki/List_of_j%C5%8Dy%C5%8D_kanji) may not have all the meanings for kanji with multiple meanings, so the above selection table may have meanings that are not very apt in the context of a family name.

'''
