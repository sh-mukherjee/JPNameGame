import pandas as pd
import cutlet
katsu = cutlet.Cutlet()
import streamlit as st

#Read in the CSV file of two-character surnames
df_sur = pd.read_csv('sur_csv.csv')

# Another dataframe of the kanji occuring in these names, with their meanings taken from the list of Jouyou Kanji
df_kanjiref = pd.read_csv('kanjiref_csv.csv')

# app title
st.title("Two-Character Japanese Family Names")

st.subheader('Choose one character each from the lists in the sidebar. If you put them together, do you get a family name that is among the top 1000 family names in Japan? Hit the Submit button and find out!')


char1 = st.sidebar.selectbox(
     "Make a selection for the name's first character",
     df_kanjiref['Choices'].unique())

char2 = st.sidebar.selectbox(
     "Make a selection for the name's second character",
     df_kanjiref['Choices'].unique())

#table = st.sidebar.dataframe(df_kan)

# creating a single-element container
#placeholder = st.empty()

name = char1[2] + char2[2]
roma_name = katsu.romaji(name)

st.write('**YOU HAVE SELECTED:**')
st.subheader(char1)
st.write(' **AND** ')
st.subheader(char2)

if st.button('Submit'):
    if name in df_sur['Surname2'].values:
        st.write('**CORRECT!**') 
        st.subheader(name + ' ' + roma_name)
    else:
        st.write('**TRY AGAIN!**')

'''
(Note that sometimes you may be asked to try again even though you chose two kanji that do make up a
legitimate family name -- it may just not be among the top 1000 family names.)
'''
'''
The kanji selection lists in the sidebar were created as follows:
1. Take all the two-character family names from [The 1,000 most common Japanese family names](https://jref.com/articles/common-japanese-surnames.213/)
2. Take all the characters in this set of names
3. From this set of characters, take all the characters which are also in the [List of jōyō kanji](https://en.wikipedia.org/wiki/List_of_j%C5%8Dy%C5%8D_kanji)

'''
